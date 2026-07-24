# Trace schema v1.0

Each JSONL line is one event object. Required identity and ordering fields are
`schema_version`, `trace_id`, `run_id`, `workflow_name`, `workflow_version`,
`event_id`, `sequence_number`, `timestamp`, `event_type`, and `status`.

Optional fields describe parents, agents, summaries, tools, latency, tokens,
estimated cost, errors, retries, human decisions, actors, and inert metadata.
Timestamps require an explicit timezone. Text and structured values are bounded.
Cost is trace-supplied, explicitly estimated, defaults to USD when present without
a currency, and is never populated from a live pricing source.

Imports accept only `.jsonl` or `.ndjson`, parse line-by-line under byte and record
limits, and quarantine invalid records with line, error path, reason, and a bounded
excerpt. Quarantined values are never included in reconstructed runs or metrics.

Run order is `(sequence_number, timestamp, event_id)`. Reconstruction reports
duplicate IDs, absent parents, parent cycles, and missing successful completion
without executing or modifying event content.
