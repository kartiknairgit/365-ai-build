from typing import Any

import pytest


@pytest.fixture
def event_data() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "trace_id": "trace-demo",
        "run_id": "run-demo",
        "workflow_name": "research-brief",
        "workflow_version": "1.0.0",
        "event_id": "event-1",
        "parent_event_id": None,
        "sequence_number": 1,
        "timestamp": "2026-07-24T01:00:00Z",
        "event_type": "run_started",
        "status": "started",
        "metadata": {"tenant": "fictional-demo"},
    }
