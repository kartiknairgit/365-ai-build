from pathlib import Path

from agentops.ingestion import ingest_jsonl
from agentops.reconstruction import reconstruct_runs

FIXTURES = Path(__file__).parents[2] / "fixtures"


def test_success_fixture_is_complete_and_valid() -> None:
    path = FIXTURES / "successful-research.jsonl"
    with path.open("rb") as stream:
        result = ingest_jsonl(stream, filename=path.name)
    assert (result.valid_count, result.invalid_count) == (7, 0)
    assert reconstruct_runs(result.events)[0].is_complete


def test_degraded_fixture_quarantines_malformed_and_mismatched_records() -> None:
    path = FIXTURES / "degraded-retry-and-quarantine.jsonl"
    with path.open("rb") as stream:
        result = ingest_jsonl(stream, filename=path.name)
    assert (result.valid_count, result.invalid_count) == (5, 2)
    assert {record.error_path for record in result.quarantined} == {
        "$.schema_version",
        "$.status",
    }


def test_failed_fixture_exposes_orphan_and_incomplete_run() -> None:
    path = FIXTURES / "failed-incomplete.jsonl"
    with path.open("rb") as stream:
        result = ingest_jsonl(stream, filename=path.name)
    run = reconstruct_runs(result.events)[0]
    assert {"missing_parent", "incomplete_run"} <= {finding.code for finding in run.findings}
