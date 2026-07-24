from copy import deepcopy

from agentops.domain import TraceEvent
from agentops.evaluation import EvaluationConfig, compare_runs, evaluate_run
from agentops.metrics import agent_scorecards, operational_metrics
from agentops.reconstruction import reconstruct_runs


def event(data: dict, event_id: str, sequence: int, **changes: object) -> TraceEvent:
    candidate = deepcopy(data)
    candidate.update(event_id=event_id, sequence_number=sequence, **changes)
    return TraceEvent.model_validate(candidate)


def test_metrics_and_scorecards_are_deterministic(event_data: dict) -> None:
    events = [
        event(event_data, "start", 1, agent_name="planner", latency_ms=10),
        event(
            event_data,
            "tool",
            2,
            agent_name="planner",
            event_type="tool_completed",
            tool_name="local",
            status="completed",
            latency_ms=20,
            retry_count=1,
        ),
        event(
            event_data,
            "done",
            3,
            event_type="run_completed",
            status="completed",
            prompt_tokens=100,
            completion_tokens=20,
            estimated_cost="0.001",
        ),
    ]
    runs = reconstruct_runs(events)
    metrics = operational_metrics(runs)
    assert metrics["completion_rate"] == 1
    assert metrics["tool_call_success_rate"] == 1
    assert metrics["estimated_cost"] == "0.001"
    card = agent_scorecards(runs)[0]
    assert card["participation_count"] == 1
    assert card["retry_count"] == 1
    assert "not an intelligence" in card["disclaimer"]


def test_evaluation_flags_explain_evidence(event_data: dict) -> None:
    events = [
        event(
            event_data,
            "handoff",
            1,
            event_type="handoff",
            latency_ms=100,
            retry_count=3,
        ),
        event(
            event_data,
            "tool-fail",
            2,
            event_type="tool_failed",
            tool_name="local",
            status="failed",
        ),
        event(event_data, "review", 3, event_type="human_review_requested", status="pending"),
    ]
    flags = evaluate_run(
        reconstruct_runs(events)[0],
        EvaluationConfig(max_retries=2, latency_threshold_ms=50),
    )
    rules = {flag.rule for flag in flags}
    assert {
        "excessive_retries",
        "tool_failure",
        "invalid_handoff",
        "missing_human_decision",
        "missing_completion",
        "unexpected_workflow_termination",
    } <= rules
    assert all(flag.evidence and flag.explanation for flag in flags)


def test_comparison_labels_regressions_and_resolved_flags(event_data: dict) -> None:
    failed = reconstruct_runs(
        [
            event(
                event_data,
                "fail",
                1,
                event_type="tool_failed",
                tool_name="local",
                status="failed",
                latency_ms=100,
            )
        ]
    )[0]
    completed = reconstruct_runs(
        [
            event(
                event_data,
                "done",
                1,
                event_type="run_completed",
                status="completed",
                latency_ms=50,
            )
        ]
    )[0]
    comparison = compare_runs(failed, completed)
    assert comparison["completion"]["classification"] == "improvement"
    assert comparison["dimensions"]["latency_ms"]["classification"] == "improvement"
    assert "tool_failure" in comparison["resolved_flags"]
