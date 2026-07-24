from collections import defaultdict
from dataclasses import asdict, dataclass
from decimal import Decimal
from statistics import median

from agentops.domain import EventStatus, EventType
from agentops.reconstruction import ReconstructedRun


def percentile(values: list[int], percentile_value: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = (len(ordered) - 1) * percentile_value
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = index - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def operational_metrics(runs: list[ReconstructedRun]) -> dict:
    events = [event for run in runs for event in run.events]
    latencies = [event.latency_ms for event in events if event.latency_ms is not None]
    tool_events = [
        event
        for event in events
        if event.event_type in {EventType.TOOL_COMPLETED, EventType.TOOL_FAILED}
    ]
    completed_tools = sum(event.event_type == EventType.TOOL_COMPLETED for event in tool_events)
    retries = sum(event.retry_count for event in events)
    reviewed = sum(
        any(event.event_type == EventType.HUMAN_REVIEW_COMPLETED for event in run.events)
        for run in runs
    )
    total = len(runs)
    completed = sum(run.is_complete for run in runs)
    return {
        "total_runs": total,
        "completion_rate": completed / total if total else 0.0,
        "failure_rate": (total - completed) / total if total else 0.0,
        "median_latency_ms": median(latencies) if latencies else 0.0,
        "p95_latency_ms": percentile(latencies, 0.95),
        "tool_call_success_rate": completed_tools / len(tool_events) if tool_events else 0.0,
        "retry_rate": retries / len(tool_events) if tool_events else 0.0,
        "human_review_rate": reviewed / total if total else 0.0,
        "prompt_tokens": sum(event.prompt_tokens or 0 for event in events),
        "completion_tokens": sum(event.completion_tokens or 0 for event in events),
        "estimated_cost": str(sum((event.estimated_cost or Decimal(0)) for event in events)),
        "cost_currency": "USD",
        "cost_is_estimate": True,
    }


@dataclass
class AgentAccumulator:
    participation_count: int = 0
    completed: int = 0
    errors: int = 0
    retries: int = 0
    human_reviews: int = 0
    tool_completed: int = 0
    tool_failed: int = 0


def agent_scorecards(runs: list[ReconstructedRun]) -> list[dict]:
    accumulators: dict[str, AgentAccumulator] = defaultdict(AgentAccumulator)
    latencies: dict[str, list[int]] = defaultdict(list)
    seen_runs: set[tuple[str, str]] = set()
    for run in runs:
        for event in run.events:
            if not event.agent_name:
                continue
            agent = event.agent_name
            run_key = (run.run_id, agent)
            if run_key not in seen_runs:
                accumulators[agent].participation_count += 1
                seen_runs.add(run_key)
            acc = accumulators[agent]
            acc.completed += event.event_type == EventType.AGENT_COMPLETED
            acc.errors += event.status in {EventStatus.FAILED, EventStatus.TIMED_OUT}
            acc.retries += event.retry_count
            acc.human_reviews += event.event_type in {
                EventType.HUMAN_REVIEW_REQUESTED,
                EventType.HUMAN_REVIEW_COMPLETED,
            }
            acc.tool_completed += event.event_type == EventType.TOOL_COMPLETED
            acc.tool_failed += event.event_type == EventType.TOOL_FAILED
            if event.latency_ms is not None:
                latencies[agent].append(event.latency_ms)
    result = []
    for agent, acc in sorted(accumulators.items()):
        values = asdict(acc)
        values["retry_count"] = values.pop("retries")
        tool_total = acc.tool_completed + acc.tool_failed
        values.update(
            agent_name=agent,
            completion_rate=acc.completed / acc.participation_count
            if acc.participation_count
            else 0.0,
            error_rate=acc.errors / acc.participation_count if acc.participation_count else 0.0,
            median_latency_ms=median(latencies[agent]) if latencies[agent] else 0.0,
            tool_success_rate=acc.tool_completed / tool_total if tool_total else 0.0,
            disclaimer="Operational evidence only; not an intelligence or quality score.",
        )
        result.append(values)
    return result
