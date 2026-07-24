from copy import deepcopy

from agentops.domain import TraceEvent
from agentops.reconstruction import reconstruct_runs


def make_event(data: dict, event_id: str, sequence: int, **changes: object) -> TraceEvent:
    candidate = deepcopy(data)
    candidate.update(event_id=event_id, sequence_number=sequence, **changes)
    return TraceEvent.model_validate(candidate)


def test_reconstruction_orders_and_links_events(event_data: dict) -> None:
    parent = make_event(event_data, "parent", 1)
    child = make_event(
        event_data,
        "child",
        2,
        parent_event_id="parent",
        event_type="run_completed",
        status="completed",
    )
    run = reconstruct_runs([child, parent])[0]
    assert [event.event_id for event in run.events] == ["parent", "child"]
    assert run.children == {"parent": ["child"]}
    assert run.is_complete


def test_reconstruction_detects_missing_parent_duplicate_cycle_and_incomplete(
    event_data: dict,
) -> None:
    first = make_event(event_data, "one", 1, parent_event_id="two")
    second = make_event(event_data, "two", 2, parent_event_id="one")
    duplicate = make_event(event_data, "one", 3)
    orphan = make_event(event_data, "orphan", 4, parent_event_id="absent")
    run = reconstruct_runs([first, second, duplicate, orphan])[0]
    codes = {finding.code for finding in run.findings}
    assert {"cycle", "duplicate_event", "missing_parent", "incomplete_run"} <= codes
