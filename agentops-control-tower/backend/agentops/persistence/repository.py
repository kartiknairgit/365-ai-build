import hashlib

from sqlalchemy import select

from agentops.ingestion.jsonl import IngestionResult
from agentops.persistence.database import Database
from agentops.persistence.tables import EventRecord, ImportBatch, QuarantineRecord


class TraceRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def save_import(
        self, *, source_name: str, content: bytes, result: IngestionResult
    ) -> tuple[int, bool]:
        digest = hashlib.sha256(content).hexdigest()
        with self.database.sessions.begin() as session:
            existing = session.scalar(
                select(ImportBatch).where(ImportBatch.content_sha256 == digest)
            )
            if existing:
                return existing.id, False
            batch = ImportBatch(
                source_name=source_name,
                content_sha256=digest,
                valid_count=result.valid_count,
                invalid_count=result.invalid_count,
            )
            session.add(batch)
            session.flush()
            for event in result.events:
                session.add(
                    EventRecord(
                        import_batch_id=batch.id,
                        trace_id=event.trace_id,
                        run_id=event.run_id,
                        event_id=event.event_id,
                        sequence_number=event.sequence_number,
                        timestamp=event.timestamp,
                        event_type=event.event_type.value,
                        status=event.status.value,
                        payload=event.model_dump(mode="json"),
                    )
                )
            for record in result.quarantined:
                session.add(
                    QuarantineRecord(
                        import_batch_id=batch.id,
                        line_number=record.line_number,
                        error_path=record.error_path,
                        reason=record.reason,
                        raw_excerpt=record.raw_excerpt,
                    )
                )
            return batch.id, True

    def list_events(
        self,
        *,
        workflow: str | None = None,
        status: str | None = None,
        agent: str | None = None,
    ) -> list:
        query = select(EventRecord).order_by(
            EventRecord.run_id, EventRecord.sequence_number, EventRecord.event_id
        )
        with self.database.sessions() as session:
            records = list(session.scalars(query))
        events = [record.payload for record in records]
        if workflow:
            events = [event for event in events if event["workflow_name"] == workflow]
        if status:
            events = [event for event in events if event["status"] == status]
        if agent:
            events = [event for event in events if event.get("agent_name") == agent]
        return events

    def list_quarantine(self, batch_id: int) -> list[dict]:
        query = (
            select(QuarantineRecord)
            .where(QuarantineRecord.import_batch_id == batch_id)
            .order_by(QuarantineRecord.line_number)
        )
        with self.database.sessions() as session:
            records = list(session.scalars(query))
        return [
            {
                "line_number": item.line_number,
                "error_path": item.error_path,
                "reason": item.reason,
                "raw_excerpt": item.raw_excerpt,
            }
            for item in records
        ]
