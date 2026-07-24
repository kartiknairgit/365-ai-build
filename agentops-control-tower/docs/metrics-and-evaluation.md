# Metrics, evaluation, and comparison

Only validated events participate. Rates return zero for empty denominators.

- Completion/failure rate: completed or incomplete reconstructed runs / all runs.
- Median and p95 latency: interpolated distribution of event latency values.
- Tool success: completed tool outcomes / completed plus failed tool outcomes.
- Retry rate: total retries / completed plus failed tool outcomes.
- Human-review rate: runs containing a completed human review / all runs.
- Tokens and estimated cost: sums of trace-supplied values. Cost is an estimate,
  reported in USD for v1 fixtures, can be omitted, and never uses live pricing.

Agent scorecards describe participation and operations only. They are not measures
of intelligence, model quality, or safety.

Deterministic rules flag malformed completion output, missing completion, excessive
retries, tool failures, latency breaches, missing human decisions, invalid handoffs,
orphaned events, token breaches, and unexpected termination. Every flag includes
the event/run evidence and a plain explanation; thresholds are local configuration.

Comparison calculates candidate minus baseline deltas. Lower latency, token, cost,
retry, tool-failure, and event totals are labelled improvements; higher totals are
regressions. Completion gained is an improvement. New/resolved rule names and agent
participation changes are reported. A two-run comparison does not establish
statistical significance.
