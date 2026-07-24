import os
from typing import Annotated

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from agentops.domain import TraceEvent
from agentops.evaluation import compare_runs, evaluate_run
from agentops.ingestion import IngestionLimits, ingest_bytes
from agentops.metrics import agent_scorecards, operational_metrics
from agentops.persistence import Database, TraceRepository
from agentops.reconstruction import reconstruct_runs

ALLOWED_CONTENT_TYPES = {
    "application/json",
    "application/jsonl",
    "application/x-ndjson",
    "application/octet-stream",
    "text/plain",
}


def create_app(database_url: str | None = None) -> FastAPI:
    database = Database(database_url or os.getenv("AGENTOPS_DATABASE_URL", "sqlite:///agentops.db"))
    database.initialize()
    repository = TraceRepository(database)
    app = FastAPI(
        title="AgentOps Control Tower API",
        description=(
            "Local-only multi-agent trace observability. Imported content is never executed."
        ),
        version="0.1.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["GET", "POST"],
        allow_headers=["content-type"],
    )
    app.state.repository = repository

    @app.exception_handler(ValueError)
    async def value_error_handler(_request, exc: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error": {"code": "invalid_request", "message": str(exc)}},
        )

    @app.exception_handler(HTTPException)
    async def http_error_handler(_request, exc: HTTPException) -> JSONResponse:
        content = (
            exc.detail
            if isinstance(exc.detail, dict) and "error" in exc.detail
            else {"error": {"code": "http_error", "message": str(exc.detail)}}
        )
        return JSONResponse(status_code=exc.status_code, content=content)

    @app.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        return {"status": "healthy", "service": "agentops-control-tower"}

    def load_runs(
        workflow: str | None = None,
        status: str | None = None,
        agent: str | None = None,
    ):
        payloads = repository.list_events(workflow=workflow, status=status, agent=agent)
        return reconstruct_runs([TraceEvent.model_validate(item) for item in payloads])

    @app.post("/api/v1/imports", status_code=201, tags=["imports"])
    async def import_trace(
        file: Annotated[UploadFile, File(description="Bounded JSONL trace")],
    ) -> dict:
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=415,
                detail={
                    "error": {
                        "code": "unsupported_media_type",
                        "message": "Expected JSONL content",
                    }
                },
            )
        limits = IngestionLimits()
        content = await file.read(limits.max_file_bytes + 1)
        if len(content) > limits.max_file_bytes:
            raise ValueError(f"file exceeds {limits.max_file_bytes} byte limit")
        filename = file.filename or "upload.jsonl"
        result = ingest_bytes(content, filename=filename)
        batch_id, created = repository.save_import(
            source_name=filename, content=content, result=result
        )
        return {
            "import_id": batch_id,
            "created": created,
            "valid_count": result.valid_count,
            "invalid_count": result.invalid_count,
            "quarantine": repository.list_quarantine(batch_id),
        }

    @app.get("/api/v1/runs", tags=["runs"])
    def list_runs(
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=25, ge=1, le=100),
        workflow: str | None = None,
        status: str | None = None,
        agent: str | None = None,
    ) -> dict:
        runs = load_runs(workflow, status, agent)
        start = (page - 1) * page_size
        items = [
            {
                "trace_id": run.trace_id,
                "run_id": run.run_id,
                "workflow_name": run.events[0].workflow_name,
                "workflow_version": run.events[0].workflow_version,
                "event_count": len(run.events),
                "is_complete": run.is_complete,
                "finding_count": len(run.findings),
            }
            for run in runs[start : start + page_size]
        ]
        return {"items": items, "page": page, "page_size": page_size, "total": len(runs)}

    def find_run(run_id: str):
        match = next((run for run in load_runs() if run.run_id == run_id), None)
        if match is None:
            raise HTTPException(
                status_code=404,
                detail={"error": {"code": "not_found", "message": "Run not found"}},
            )
        return match

    @app.get("/api/v1/runs/{run_id}", tags=["runs"])
    def get_run(run_id: str) -> dict:
        run = find_run(run_id)
        return {
            "trace_id": run.trace_id,
            "run_id": run.run_id,
            "is_complete": run.is_complete,
            "events": [event.model_dump(mode="json") for event in run.events],
            "findings": [finding.__dict__ for finding in run.findings],
            "evaluation_flags": [flag.__dict__ for flag in evaluate_run(run)],
        }

    @app.get("/api/v1/metrics", tags=["metrics"])
    def metrics() -> dict:
        return operational_metrics(load_runs())

    @app.get("/api/v1/agents", tags=["metrics"])
    def agents() -> list[dict]:
        return agent_scorecards(load_runs())

    @app.get("/api/v1/comparisons", tags=["evaluation"])
    def comparison(baseline_run_id: str, candidate_run_id: str) -> dict:
        return compare_runs(find_run(baseline_run_id), find_run(candidate_run_id))

    return app


app = create_app()
