from collections import defaultdict
from dataclasses import dataclass, field

from agentops.domain import EventStatus, EventType, TraceEvent


@dataclass(frozen=True)
class StructuralFinding:
    code: str
    event_id: str
    explanation: str


@dataclass
class ReconstructedRun:
    trace_id: str
    run_id: str
    events: list[TraceEvent]
    children: dict[str, list[str]]
    findings: list[StructuralFinding] = field(default_factory=list)
    is_complete: bool = False


def _cycle_members(parents: dict[str, str | None]) -> set[str]:
    cyclic: set[str] = set()
    for start in parents:
        seen: dict[str, int] = {}
        current: str | None = start
        while current in parents:
            if current in seen:
                cyclic.update(list(seen)[seen[current] :])
                break
            seen[current] = len(seen)
            current = parents[current]
    return cyclic


def reconstruct_runs(events: list[TraceEvent]) -> list[ReconstructedRun]:
    grouped: dict[tuple[str, str], list[TraceEvent]] = defaultdict(list)
    for event in events:
        grouped[(event.trace_id, event.run_id)].append(event)

    runs: list[ReconstructedRun] = []
    for (trace_id, run_id), group in sorted(grouped.items()):
        ordered = sorted(
            group, key=lambda event: (event.sequence_number, event.timestamp, event.event_id)
        )
        findings: list[StructuralFinding] = []
        by_id: dict[str, TraceEvent] = {}
        for event in ordered:
            if event.event_id in by_id:
                findings.append(
                    StructuralFinding(
                        "duplicate_event", event.event_id, "Duplicate event ID in run"
                    )
                )
            else:
                by_id[event.event_id] = event

        children: dict[str, list[str]] = defaultdict(list)
        parents: dict[str, str | None] = {}
        for event_id, event in by_id.items():
            parents[event_id] = event.parent_event_id
            if event.parent_event_id:
                if event.parent_event_id not in by_id:
                    findings.append(
                        StructuralFinding(
                            "missing_parent",
                            event_id,
                            f"Parent {event.parent_event_id!r} is absent",
                        )
                    )
                else:
                    children[event.parent_event_id].append(event_id)
        for event_id in sorted(_cycle_members(parents)):
            findings.append(
                StructuralFinding("cycle", event_id, "Parent relationship contains a cycle")
            )

        completion = any(
            event.event_type == EventType.RUN_COMPLETED and event.status == EventStatus.COMPLETED
            for event in ordered
        )
        if not completion:
            findings.append(
                StructuralFinding(
                    "incomplete_run", run_id, "No successfully completed run event is present"
                )
            )
        runs.append(
            ReconstructedRun(
                trace_id=trace_id,
                run_id=run_id,
                events=ordered,
                children={key: sorted(value) for key, value in children.items()},
                findings=findings,
                is_complete=completion,
            )
        )
    return runs
