from fastapi.testclient import TestClient

from civicutility import __version__
from civicutility.main import app

client = TestClient(app)


def test_root_reports_honest_current_state():
    payload = client.get("/").json()
    assert payload["name"] == "CivicUtility"
    assert payload["version"] == __version__
    assert "utility billing" in payload["message"]
    assert "not implemented yet" in payload["message"]


def test_health_reports_civiccore_pin():
    assert client.get("/health").json() == {
        "status": "ok",
        "service": "civicutility",
        "version": "0.1.0",
        "civiccore_version": "0.2.0",
    }


def test_public_ui_contains_version_boundaries_and_dependency():
    text = client.get("/civicutility").text
    assert "CivicUtility v0.1.0" in text
    assert "No utility billing" in text
    assert "civiccore==0.2.0" in text


def test_api_endpoints_return_deterministic_payloads():
    assert (
        client.post(
            "/api/v1/civicutility/policy-answer", json={"question": "payment options"}
        ).status_code
        == 200
    )
    assert (
        client.post(
            "/api/v1/civicutility/account-context",
            json={
                "account_id": "A-100",
                "customer_name": "Jordan Resident",
                "service_address": "100 Water St",
                "balance_status": "current",
                "last_bill_summary": "Water and sewer service.",
            },
        ).json()["read_only"]
        is True
    )
    assert (
        client.post(
            "/api/v1/civicutility/payment-arrangement-draft",
            json={"account_id": "A-100", "csr_inputs": ["Three installments"]},
        ).json()["not_payment_processing"]
        is True
    )
    assert (
        client.post(
            "/api/v1/civicutility/service-request-intake",
            json={
                "account_id": "A-100",
                "issue_type": "water leak",
                "description": "Leak near meter",
                "location": "100 Water St",
            },
        ).json()["civic311_handoff_recommended"]
        is True
    )
