# Privacy and threat model

All data is local. Seeded traces are fictional and redacted. The system makes no
provider or pricing calls and logs no full tool arguments or responses by default.

## Untrusted inputs

Controls include extension and media-type checks, a 5 MiB file limit, 10,000-record
limit, per-line and structured-field bounds, safe standard-library JSON parsing,
Pydantic validation, parameterized SQLAlchemy access, React text escaping, bounded
quarantine excerpts, and exact confirmation for destructive reset.

The application performs no shell/dynamic Python execution, unsafe deserialization,
HTML injection, URL fetching, automatic telemetry export, or secret processing.
Quarantined records cannot enter metrics or evaluation.

Residual risks include sensitive information deliberately placed in summaries,
local-machine access to the SQLite volume, browser extensions, resource pressure
within documented limits, and spreadsheet-formula interpretation after a user opens
CSV in third-party software. Operators should use synthetic/redacted data and keep
the local environment access-controlled.
