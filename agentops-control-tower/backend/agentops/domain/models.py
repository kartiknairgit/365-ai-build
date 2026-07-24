from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

MAX_TEXT_LENGTH = 4_000
MAX_STRUCTURED_BYTES = 32_000


class EventType(StrEnum):
    RUN_STARTED = "run_started"
    RUN_COMPLETED = "run_completed"
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    HANDOFF = "handoff"
    TOOL_CALLED = "tool_called"
    TOOL_COMPLETED = "tool_completed"
    TOOL_FAILED = "tool_failed"
    HUMAN_REVIEW_REQUESTED = "human_review_requested"
    HUMAN_REVIEW_COMPLETED = "human_review_completed"
    VALIDATION_FAILED = "validation_failed"
    ERROR = "error"


class EventStatus(StrEnum):
    STARTED = "started"
    COMPLETED = "completed"
    DEGRADED = "degraded"
    FAILED = "failed"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    TIMED_OUT = "timed_out"


class HumanDecision(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"
    CHANGES_REQUESTED = "changes_requested"


class TraceEvent(BaseModel):
    """Schema v1 event. Extra keys are preserved as inert Pydantic extras."""

    model_config = ConfigDict(extra="allow", str_strip_whitespace=True)

    schema_version: str = Field(pattern=r"^1\.0$")
    trace_id: str = Field(min_length=1, max_length=128)
    run_id: str = Field(min_length=1, max_length=128)
    workflow_name: str = Field(min_length=1, max_length=200)
    workflow_version: str = Field(min_length=1, max_length=64)
    event_id: str = Field(min_length=1, max_length=128)
    parent_event_id: str | None = Field(default=None, max_length=128)
    sequence_number: int = Field(ge=0)
    timestamp: datetime
    event_type: EventType
    agent_name: str | None = Field(default=None, max_length=200)
    agent_role: str | None = Field(default=None, max_length=200)
    status: EventStatus
    input_summary: str | None = Field(default=None, max_length=MAX_TEXT_LENGTH)
    output_summary: str | None = Field(default=None, max_length=MAX_TEXT_LENGTH)
    tool_name: str | None = Field(default=None, max_length=200)
    tool_arguments: dict[str, Any] | list[Any] | str | None = None
    tool_response: dict[str, Any] | list[Any] | str | None = None
    latency_ms: int | None = Field(default=None, ge=0, le=86_400_000)
    prompt_tokens: int | None = Field(default=None, ge=0, le=100_000_000)
    completion_tokens: int | None = Field(default=None, ge=0, le=100_000_000)
    estimated_cost: Decimal | None = Field(default=None, ge=0, max_digits=14, decimal_places=6)
    cost_currency: str | None = Field(default=None, pattern=r"^[A-Z]{3}$")
    error_type: str | None = Field(default=None, max_length=200)
    error_message: str | None = Field(default=None, max_length=MAX_TEXT_LENGTH)
    retry_count: int = Field(default=0, ge=0, le=100)
    human_decision: HumanDecision | None = None
    actor_label: str | None = Field(default=None, max_length=200)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("timestamp")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("timestamp must include a timezone")
        return value

    @field_validator("metadata", "tool_arguments", "tool_response")
    @classmethod
    def bound_structured_content(cls, value: Any) -> Any:
        import json

        try:
            encoded = json.dumps(value, ensure_ascii=False, allow_nan=False)
        except (TypeError, ValueError) as exc:
            raise ValueError("value must contain only JSON-compatible data") from exc
        if len(encoded.encode("utf-8")) > MAX_STRUCTURED_BYTES:
            raise ValueError(f"structured value exceeds {MAX_STRUCTURED_BYTES} bytes")
        return value

    @model_validator(mode="after")
    def validate_context(self) -> Self:
        tool_events = {
            EventType.TOOL_CALLED,
            EventType.TOOL_COMPLETED,
            EventType.TOOL_FAILED,
        }
        if self.event_type in tool_events and not self.tool_name:
            raise ValueError("tool_name is required for tool events")
        if self.event_type == EventType.HUMAN_REVIEW_COMPLETED and not self.human_decision:
            raise ValueError("human_decision is required when human review completes")
        if self.estimated_cost is not None and self.cost_currency is None:
            self.cost_currency = "USD"
        return self
