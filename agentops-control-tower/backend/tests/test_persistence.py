import io
import json

from sqlalchemy import func, select

from agentops.ingestion import ingest_jsonl
from agentops.persistence import Database, TraceRepository
from agentops.persistence.tables import EventRecord, ImportBatch, QuarantineRecord


def test_repository_persists_valid_and_quarantined_repeat_safely(
    event_data: dict,
) -> None:
    content = (json.dumps(event_data) + "\n{bad}\n").encode()
    result = ingest_jsonl(io.BytesIO(content), filename="fixture.jsonl")
    database = Database("sqlite://")
    database.initialize()
    repository = TraceRepository(database)

    first_id, first_created = repository.save_import(
        source_name="fixture.jsonl", content=content, result=result
    )
    second_id, second_created = repository.save_import(
        source_name="renamed.jsonl", content=content, result=result
    )

    assert (first_id, first_created) == (second_id, True)
    assert not second_created
    with database.sessions() as session:
        assert session.scalar(select(func.count()).select_from(ImportBatch)) == 1
        assert session.scalar(select(func.count()).select_from(EventRecord)) == 1
        assert session.scalar(select(func.count()).select_from(QuarantineRecord)) == 1
