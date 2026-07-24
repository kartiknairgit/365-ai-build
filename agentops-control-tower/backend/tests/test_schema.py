from copy import deepcopy

import pytest
from pydantic import ValidationError

from agentops.domain import TraceEvent


def test_schema_preserves_safe_unknown_metadata(event_data: dict) -> None:
    event_data["future_field"] = {"enabled": True}
    event = TraceEvent.model_validate(event_data)
    assert event.__pydantic_extra__ == {"future_field": {"enabled": True}}
    assert event.metadata["tenant"] == "fictional-demo"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schema_version", "2.0"),
        ("status", "mysterious"),
        ("event_type", "unknown_event"),
        ("timestamp", "2026-07-24T01:00:00"),
    ],
)
def test_schema_rejects_unsupported_values(event_data: dict, field: str, value: str) -> None:
    candidate = deepcopy(event_data)
    candidate[field] = value
    with pytest.raises(ValidationError):
        TraceEvent.model_validate(candidate)


def test_completed_human_review_requires_decision(event_data: dict) -> None:
    event_data.update(event_type="human_review_completed", event_id="review-1")
    with pytest.raises(ValidationError, match="human_decision"):
        TraceEvent.model_validate(event_data)
