# AgentOps Control Tower engineering instructions

## Boundaries

- Keep product code, configuration, tests, and fixtures under this directory.
- Keep `frontend` and `backend` cleanly separated; communicate only over HTTP.
- Require no paid API, external service, authentication system, or cloud database.
- Treat every imported byte as untrusted data. Never evaluate, execute, fetch URLs
  from, or render imported HTML.
- Do not log full tool arguments/responses. Return summaries or explicit redactions.
- Preserve unknown JSON metadata as inert JSON-compatible values.

## Architecture

- `backend/agentops/domain`: versioned Pydantic v2 trace contracts.
- `backend/agentops/ingestion`: bounded JSONL parsing and quarantine.
- `backend/agentops/reconstruction`: deterministic run topology validation.
- `backend/agentops/persistence`: SQLAlchemy models and repositories over SQLite.
- `backend/agentops/services`: orchestration boundaries used by FastAPI.
- `frontend/src`: React, TypeScript, Router, Query, React Flow, and Recharts UI.
- `fixtures`: fictional, redacted JSONL examples; never production data.
- `docs`: architecture, schema, privacy, threat model, and evaluation references.

## Conventions

- Python targets 3.12, uses type hints, Ruff, pytest, Pydantic v2, and SQLAlchemy 2.
- TypeScript is strict. Components expose accessible names and non-chart fallbacks.
- Timestamps are timezone-aware ISO 8601 values normalized to UTC.
- Run ordering is `(sequence_number, timestamp, event_id)` and is deterministic.
- Database access is parameterized through SQLAlchemy repositories.
- Schema or behavior changes require focused tests and documentation updates.
- Cost values are trace-supplied estimates only; no live pricing lookup is allowed.

## Commands and required validation

Backend: `pip install -e '.[dev]'`, `ruff format --check .`, `ruff check .`, `pytest`,
and `uvicorn agentops.main:app --host 127.0.0.1 --port 8000`.

Frontend: `npm ci`, `npm run format:check`, `npm run lint`, `npm run typecheck`,
`npm test -- --run`, and `npm run build`.

Before every PR: run relevant checks, `git diff --check`, verify only intended paths
changed, and confirm seeded data is fictional and redacted.
