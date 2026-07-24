import io
import json

import pytest

from agentops.ingestion import IngestionLimits, ingest_jsonl


def test_ingestion_separates_valid_and_quarantined(event_data: dict) -> None:
    content = json.dumps(event_data).encode() + b"\n{bad json}\n"
    result = ingest_jsonl(io.BytesIO(content), filename="trace.jsonl")
    assert result.valid_count == 1
    assert result.invalid_count == 1
    assert result.quarantined[0].line_number == 2
    assert result.quarantined[0].error_path == "$"


def test_ingestion_reports_validation_path(event_data: dict) -> None:
    event_data.pop("event_id")
    result = ingest_jsonl(
        io.BytesIO((json.dumps(event_data) + "\n").encode()), filename="trace.ndjson"
    )
    assert result.invalid_count == 1
    assert result.quarantined[0].error_path == "$.event_id"


def test_ingestion_enforces_extension_and_size(event_data: dict) -> None:
    data = (json.dumps(event_data) + "\n").encode()
    with pytest.raises(ValueError, match="only"):
        ingest_jsonl(io.BytesIO(data), filename="trace.txt")
    with pytest.raises(ValueError, match="file exceeds"):
        ingest_jsonl(
            io.BytesIO(data),
            filename="trace.jsonl",
            limits=IngestionLimits(max_file_bytes=2),
        )
