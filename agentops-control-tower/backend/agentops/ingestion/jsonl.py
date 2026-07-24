import io
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import BinaryIO

from pydantic import ValidationError

from agentops.domain import TraceEvent


@dataclass(frozen=True)
class IngestionLimits:
    max_file_bytes: int = 5 * 1024 * 1024
    max_records: int = 10_000
    max_line_bytes: int = 128 * 1024


DEFAULT_LIMITS = IngestionLimits()


@dataclass(frozen=True)
class QuarantinedRecord:
    line_number: int
    error_path: str
    reason: str
    raw_excerpt: str


@dataclass
class IngestionResult:
    events: list[TraceEvent] = field(default_factory=list)
    quarantined: list[QuarantinedRecord] = field(default_factory=list)

    @property
    def valid_count(self) -> int:
        return len(self.events)

    @property
    def invalid_count(self) -> int:
        return len(self.quarantined)


def _quarantine(line_number: int, path: str, reason: str, raw: bytes) -> QuarantinedRecord:
    return QuarantinedRecord(
        line_number=line_number,
        error_path=path,
        reason=reason[:1_000],
        raw_excerpt=raw[:500].decode("utf-8", errors="replace"),
    )


def ingest_jsonl(
    source: BinaryIO,
    *,
    filename: str,
    limits: IngestionLimits = DEFAULT_LIMITS,
) -> IngestionResult:
    """Parse bounded JSONL without evaluating or dereferencing any imported value."""
    if Path(filename).suffix.lower() not in {".jsonl", ".ndjson"}:
        raise ValueError("only .jsonl and .ndjson files are accepted")

    result = IngestionResult()
    total_bytes = 0
    for line_number, raw in enumerate(source, start=1):
        total_bytes += len(raw)
        if total_bytes > limits.max_file_bytes:
            raise ValueError(f"file exceeds {limits.max_file_bytes} byte limit")
        if line_number > limits.max_records:
            raise ValueError(f"file exceeds {limits.max_records} record limit")
        if len(raw) > limits.max_line_bytes:
            result.quarantined.append(_quarantine(line_number, "$", "line exceeds byte limit", raw))
            continue
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            result.quarantined.append(_quarantine(line_number, "$", f"invalid JSON: {exc}", raw))
            continue
        if not isinstance(value, dict):
            result.quarantined.append(
                _quarantine(line_number, "$", "record must be a JSON object", raw)
            )
            continue
        try:
            result.events.append(TraceEvent.model_validate(value))
        except ValidationError as exc:
            first = exc.errors(include_url=False)[0]
            path = "$." + ".".join(str(part) for part in first["loc"])
            result.quarantined.append(_quarantine(line_number, path, str(first["msg"]), raw))
    return result


def ingest_bytes(data: bytes, *, filename: str) -> IngestionResult:
    return ingest_jsonl(io.BytesIO(data), filename=filename)
