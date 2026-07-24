# Architecture

The browser sends JSONL over local HTTP to FastAPI. A bounded parser produces
validated Pydantic events and quarantined line diagnostics. Valid events pass to
deterministic reconstruction and SQLAlchemy repositories backed by SQLite.
Metrics, scorecards, rules, comparisons, and exports read only validated events.
React Query consumes the REST API; Recharts and React Flow provide visual views.

The frontend never connects directly to SQLite. The backend never runs an agent,
tool, uploaded argument, response, URL, HTML, or code. Docker Compose packages two
separate services and a local volume; no external service is required.

## Known limitations and future work

- This is a single-user prototype without authentication or concurrent-write tuning.
- Schema v1 supports one explicit version and USD fixture estimates.
- SQLite filtering should move fully into SQL for larger local datasets.
- Comparisons are deterministic pairs, not statistical experiments.
- Route-level bundle splitting, richer graph diff overlays, and combined timeline
  filter controls are good v1.1 work.
