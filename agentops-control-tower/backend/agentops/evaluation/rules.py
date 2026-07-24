from dataclasses import dataclass
from typing import Literal

from agentops.domain import EventType
from agentops.reconstruction import ReconstructedRun


@dataclass(frozen=True)
class EvaluationConfig:
    max_retries: int = 2
    latency_threshold_ms: int = 30_000
    token_threshold: int = 20_000


DEFAULT_CONFIG = EvaluationConfig()


@dataclass(frozen=True)
class EvaluationFlag:
    rule: str
    severity: Literal["warning", "failure"]
    event_id: str
    explanation: str
    evidence: dict[str, str | int]


def _flag(
    rule: str,
    event_id: str,
    explanation: str,
    evidence: dict[str, str | int],
    severity: Literal["warning", "failure"] = "warning",
) -> EvaluationFlag:
    return EvaluationFlag(rule, severity, event_id, explanation, evidence)


def evaluate_run(
    run: ReconstructedRun, config: EvaluationConfig = DEFAULT_CONFIG
) -> list[EvaluationFlag]:
    flags: list[EvaluationFlag] = []
    for finding in run.findings:
        if finding.code == "missing_parent":
            flags.append(
                _flag(
                    "orphaned_event", finding.event_id, finding.explanation, {"code": finding.code}
                )
            )
        if finding.code == "incomplete_run":
            flags.extend(
                [
                    _flag(
                        "missing_completion",
                        finding.event_id,
                        "The run has no successful completion event.",
                        {"run_id": run.run_id},
                        "failure",
                    ),
                    _flag(
                        "unexpected_workflow_termination",
                        finding.event_id,
                        "The observed event stream ended before successful completion.",
                        {"run_id": run.run_id},
                        "failure",
                    ),
                ]
            )
    by_id = {event.event_id: event for event in run.events}
    for event in run.events:
        if event.event_type == EventType.AGENT_COMPLETED and not event.output_summary:
            flags.append(
                _flag(
                    "malformed_output",
                    event.event_id,
                    "Agent completion has no output summary.",
                    {"event_type": event.event_type.value},
                )
            )
        if event.retry_count > config.max_retries:
            flags.append(
                _flag(
                    "excessive_retries",
                    event.event_id,
                    f"Retry count exceeds configured maximum {config.max_retries}.",
                    {"retry_count": event.retry_count, "threshold": config.max_retries},
                )
            )
        if event.event_type == EventType.TOOL_FAILED:
            flags.append(
                _flag(
                    "tool_failure",
                    event.event_id,
                    "A tool call reported failure.",
                    {"tool_name": event.tool_name or "unknown"},
                    "failure",
                )
            )
        if event.latency_ms is not None and event.latency_ms > config.latency_threshold_ms:
            flags.append(
                _flag(
                    "latency_threshold_breach",
                    event.event_id,
                    "Event latency exceeds the configured threshold.",
                    {"latency_ms": event.latency_ms, "threshold": config.latency_threshold_ms},
                )
            )
        if event.event_type == EventType.HUMAN_REVIEW_REQUESTED and not any(
            candidate.event_type == EventType.HUMAN_REVIEW_COMPLETED for candidate in run.events
        ):
            flags.append(
                _flag(
                    "missing_human_decision",
                    event.event_id,
                    "Human review was requested but no decision was observed.",
                    {"event_type": event.event_type.value},
                )
            )
        if event.event_type == EventType.HANDOFF:
            target = event.metadata.get("target_agent")
            if not isinstance(target, str) or not target.strip():
                flags.append(
                    _flag(
                        "invalid_handoff",
                        event.event_id,
                        "Handoff does not identify a target agent.",
                        {"event_type": event.event_type.value},
                    )
                )
        total_tokens = (event.prompt_tokens or 0) + (event.completion_tokens or 0)
        if total_tokens > config.token_threshold:
            flags.append(
                _flag(
                    "token_threshold_breach",
                    event.event_id,
                    "Event token total exceeds the configured threshold.",
                    {"tokens": total_tokens, "threshold": config.token_threshold},
                )
            )
        if event.parent_event_id and event.parent_event_id not in by_id:
            # Reconstruction findings are canonical; this ensures evidence stays event-local.
            pass
    return sorted(flags, key=lambda item: (item.event_id, item.rule))
