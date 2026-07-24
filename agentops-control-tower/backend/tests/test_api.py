from pathlib import Path

from fastapi.testclient import TestClient

from agentops.main import create_app

FIXTURES = Path(__file__).parents[2] / "fixtures"


def client(tmp_path: Path) -> TestClient:
    return TestClient(create_app(f"sqlite:///{tmp_path / 'api.db'}"))


def import_fixture(api: TestClient, name: str) -> dict:
    path = FIXTURES / name
    with path.open("rb") as stream:
        response = api.post(
            "/api/v1/imports",
            files={"file": (name, stream, "application/x-ndjson")},
        )
    assert response.status_code == 201
    return response.json()


def test_import_list_filter_detail_and_metrics(tmp_path: Path) -> None:
    api = client(tmp_path)
    outcome = import_fixture(api, "successful-research.jsonl")
    assert outcome["valid_count"] == 7
    assert outcome["invalid_count"] == 0

    runs = api.get("/api/v1/runs", params={"workflow": "fictional-research-brief"})
    assert runs.status_code == 200
    assert runs.json()["total"] == 1
    run_id = runs.json()["items"][0]["run_id"]
    detail = api.get(f"/api/v1/runs/{run_id}")
    assert detail.status_code == 200
    assert len(detail.json()["events"]) == 7
    assert api.get("/api/v1/metrics").json()["completion_rate"] == 1
    assert api.get("/api/v1/agents").json()


def test_quarantine_repeat_safe_import_and_errors(tmp_path: Path) -> None:
    api = client(tmp_path)
    first = import_fixture(api, "degraded-retry-and-quarantine.jsonl")
    second = import_fixture(api, "degraded-retry-and-quarantine.jsonl")
    assert first["invalid_count"] == 2
    assert len(first["quarantine"]) == 2
    assert second["created"] is False
    assert api.get("/api/v1/runs/absent").status_code == 404


def test_comparison_endpoint(tmp_path: Path) -> None:
    api = client(tmp_path)
    import_fixture(api, "successful-research.jsonl")
    import_fixture(api, "failed-incomplete.jsonl")
    response = api.get(
        "/api/v1/comparisons",
        params={
            "baseline_run_id": "report-failed-incomplete",
            "candidate_run_id": "research-v1-success",
        },
    )
    assert response.status_code == 200
    assert response.json()["completion"]["classification"] == "improvement"
