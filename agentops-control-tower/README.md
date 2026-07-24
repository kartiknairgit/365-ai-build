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
