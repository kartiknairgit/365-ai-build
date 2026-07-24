# AgentOps Control Tower

AgentOps Control Tower is a local-first evaluation and observability prototype for
multi-agent workflow traces. It imports untrusted JSONL, validates and quarantines
bad records, reconstructs runs, and persists safe structured data in SQLite.

It does **not** execute agents, tool calls, arguments, or responses. It does not
guarantee model quality or safety. Deterministic operational signals require human
interpretation, and all seeded traces are fictional.

## Quick start

Requires Python 3.12 and Node.js 20+.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn agentops.main:app --reload
```

```bash
cd frontend
npm ci
npm run dev
```

Or run both services with `docker compose up --build`. The backend health endpoint
is `http://localhost:8000/health`; the frontend is `http://localhost:5173`.

## Validation

```bash
cd backend && ruff format --check . && ruff check . && pytest
cd frontend && npm ci && npm run check
docker compose config
```

See [INSTRUCTIONS.md](INSTRUCTIONS.md) for architecture and durable conventions.

## API overview

- `POST /api/v1/imports` imports a bounded `.jsonl`/`.ndjson` file.
- `GET /api/v1/runs` lists and filters reconstructed runs with pagination.
- `GET /api/v1/runs/{run_id}` returns safe event details and evaluation evidence.
- `GET /api/v1/metrics` returns deterministic operational metrics.
- `GET /api/v1/agents` returns operational, non-intelligence agent scorecards.
- `GET /api/v1/comparisons` compares baseline and candidate runs.
- `GET /api/v1/runs/{run_id}/export.jsonl` exports validated trace events.
- `GET /api/v1/runs/{run_id}/evaluation.csv` and `/audit.md` export audit evidence.
- `POST /api/v1/demo/fixtures/{name}` loads a fixed fictional sample.
- `POST /api/v1/demo/reset` requires the exact phrase `RESET LOCAL DEMO DATA`.

Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

Architecture and security details live in [docs/architecture.md](docs/architecture.md)
and [docs/privacy-threat-model.md](docs/privacy-threat-model.md). Screenshots are not
checked in for this local-only prototype; run the application for the live,
responsive control plane.
