from decimal import Decimal

from agentops.domain import EventType
from agentops.evaluation.rules import evaluate_run
from agentops.reconstruction import ReconstructedRun


def _direction(delta: int | float | Decimal, *, lower_is_better: bool = True) -> str:
    if delta == 0:
        return "unchanged"
    improved = delta < 0 if lower_is_better else delta > 0
    return "improvement" if improved else "regression"


def _run_values(run: ReconstructedRun) -> dict:
    return {
        "completed": run.is_complete,
        "event_count": len(run.events),
        "agents": sorted({event.agent_name for event in run.events if event.agent_name}),
        "latency_ms": sum(event.latency_ms or 0 for event in run.events),
        "tokens": sum(
            (event.prompt_tokens or 0) + (event.completion_tokens or 0) for event in run.events
        ),
        "estimated_cost": sum((event.estimated_cost or Decimal(0)) for event in run.events),
        "retries": sum(event.retry_count for event in run.events),
        "tool_failures": sum(event.event_type == EventType.TOOL_FAILED for event in run.events),
        "flags": {flag.rule for flag in evaluate_run(run)},
    }


def compare_runs(baseline: ReconstructedRun, candidate: ReconstructedRun) -> dict:
    before, after = _run_values(baseline), _run_values(candidate)
    dimensions = {}
    for name in (
        "event_count",
        "latency_ms",
        "tokens",
        "estimated_cost",
        "retries",
        "tool_failures",
    ):
        delta = after[name] - before[name]
        dimensions[name] = {
            "baseline": str(before[name]) if isinstance(before[name], Decimal) else before[name],
            "candidate": str(after[name]) if isinstance(after[name], Decimal) else after[name],
            "delta": str(delta) if isinstance(delta, Decimal) else delta,
            "classification": _direction(delta),
        }
    if before["completed"] == after["completed"]:
        completion_class = "unchanged"
    else:
        completion_class = "improvement" if after["completed"] else "regression"
    return {
        "completion": {
            "baseline": before["completed"],
            "candidate": after["completed"],
            "classification": completion_class,
        },
        "dimensions": dimensions,
        "agents_added": sorted(set(after["agents"]) - set(before["agents"])),
        "agents_removed": sorted(set(before["agents"]) - set(after["agents"])),
        "new_flags": sorted(after["flags"] - before["flags"]),
        "resolved_flags": sorted(before["flags"] - after["flags"]),
        "methodology_note": (
            "Deterministic single-run comparison; no statistical significance is implied."
        ),
    }
