from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from civicutility.main import app, _dispose_workpaper_repository
from civicutility.persistence import UtilityWorkpaperRepository


client = TestClient(app)
ACCOUNT = {
    "account_id": "A-100",
    "customer_name": "Jordan Resident",
    "service_address": "100 Water St",
    "balance_status": "current",
    "last_bill_summary": "Water and sewer service.",
}
SERVICE = {
    "account_id": "A-100",
    "issue_type": "water leak",
    "description": "Leak near meter",
    "location": "100 Water St",
}


def test_repository_persists_account_context_and_service_request(tmp_path: Path) -> None:
    db_path = tmp_path / "civicutility.db"
    repo = UtilityWorkpaperRepository(db_url=f"sqlite+pysqlite:///{db_path.as_posix()}")
    snapshot = repo.create_account_context(**ACCOUNT)
    intake = repo.create_service_request(**SERVICE)
    repo.engine.dispose()

    reloaded = UtilityWorkpaperRepository(db_url=f"sqlite+pysqlite:///{db_path.as_posix()}")
    assert reloaded.get_account_context(snapshot.snapshot_id).read_only is True
    assert reloaded.get_service_request(intake.intake_id).civic311_handoff_recommended is True
    reloaded.engine.dispose()
    db_path.unlink()


def test_utility_persistence_api_round_trip(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civicutility-api.db"
    monkeypatch.setenv(
        "CIVICUTILITY_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}"
    )
    _dispose_workpaper_repository()
    snapshot = client.post("/api/v1/civicutility/account-context", json=ACCOUNT)
    fetched_snapshot = client.get(
        f"/api/v1/civicutility/account-context/{snapshot.json()['snapshot_id']}"
    )
    intake = client.post("/api/v1/civicutility/service-request-intake", json=SERVICE)
    fetched_intake = client.get(
        f"/api/v1/civicutility/service-request-intake/{intake.json()['intake_id']}"
    )
    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICUTILITY_WORKPAPER_DB_URL")

    assert fetched_snapshot.status_code == 200
    assert fetched_snapshot.json()["restricted_fields_hidden"] is True
    assert fetched_intake.status_code == 200
    assert fetched_intake.json()["not_work_order"] is True
    db_path.unlink()


def test_get_account_without_persistence_returns_actionable_503(monkeypatch) -> None:
    monkeypatch.delenv("CIVICUTILITY_WORKPAPER_DB_URL", raising=False)
    _dispose_workpaper_repository()
    response = client.get("/api/v1/civicutility/account-context/example")
    assert response.status_code == 503
    assert "Set CIVICUTILITY_WORKPAPER_DB_URL" in response.json()["detail"]["fix"]


def test_get_service_request_missing_id_returns_actionable_404(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civicutility-missing.db"
    monkeypatch.setenv(
        "CIVICUTILITY_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}"
    )
    _dispose_workpaper_repository()
    response = client.get("/api/v1/civicutility/service-request-intake/missing")
    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICUTILITY_WORKPAPER_DB_URL")

    assert response.status_code == 404
    assert "POST /api/v1/civicutility/service-request-intake" in response.json()["detail"]["fix"]
    db_path.unlink()
