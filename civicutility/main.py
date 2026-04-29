"""FastAPI runtime foundation for CivicUtility."""

import os

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicutility import __version__
from civicutility.account import summarize_account_context
from civicutility.arrangements import draft_payment_arrangement
from civicutility.persistence import (
    StoredAccountContext,
    StoredServiceRequest,
    UtilityWorkpaperRepository,
)
from civicutility.policy import UtilityPolicySource, answer_utility_question
from civicutility.public_ui import render_public_lookup_page
from civicutility.service_requests import prepare_service_request

app = FastAPI(
    title="CivicUtility",
    version=__version__,
    description="Utility customer-service copilot foundation for CivicSuite.",
)

_workpaper_repository: UtilityWorkpaperRepository | None = None
_workpaper_db_url: str | None = None

@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    """Return an empty favicon response so browser QA has a clean console."""

    return Response(status_code=204)

POLICY_SOURCES = [
    UtilityPolicySource(
        "u1",
        "Utility customer service policy",
        "Payment options, conservation tips, service request intake, and billing policy answers",
        "Utility Policy Manual 1",
    )
]


class UtilityQuestionRequest(BaseModel):
    question: str


class AccountContextRequest(BaseModel):
    account_id: str
    customer_name: str
    service_address: str
    balance_status: str
    last_bill_summary: str


class ArrangementRequest(BaseModel):
    account_id: str
    csr_inputs: list[str]


class ServiceRequestIntake(BaseModel):
    account_id: str
    issue_type: str
    description: str
    location: str


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "CivicUtility",
        "version": __version__,
        "status": "utility customer-service foundation",
        "message": (
            "CivicUtility policy Q&A, CSR-safe account context, payment-arrangement drafts, "
            "service-request intake, optional database-backed account/service workpapers, "
            "and public UI foundation are online; utility billing, "
            "payments, shutoff/reconnect decisions, live billing connectors, live LLM calls, "
            "and Civic311 write-back are not implemented yet."
        ),
        "next_step": "Post-v0.1.1 roadmap: billing-system read adapters and Civic311 handoff integration",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "civicutility",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/civicutility", response_class=HTMLResponse)
def public_page() -> str:
    return render_public_lookup_page()


@app.post("/api/v1/civicutility/policy-answer")
def policy_answer(request: UtilityQuestionRequest) -> dict[str, object]:
    return answer_utility_question(request.question, POLICY_SOURCES).__dict__


@app.post("/api/v1/civicutility/account-context")
def account_context(request: AccountContextRequest) -> dict[str, object]:
    if _workpaper_database_url() is not None:
        return _stored_account_response(
            _get_workpaper_repository().create_account_context(**request.model_dump())
        )
    payload = summarize_account_context(**request.model_dump()).__dict__
    payload["snapshot_id"] = None
    return payload


@app.get("/api/v1/civicutility/account-context/{snapshot_id}")
def get_account_context(snapshot_id: str) -> dict[str, object]:
    if _workpaper_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "CivicUtility workpaper persistence is not configured.",
                "fix": "Set CIVICUTILITY_WORKPAPER_DB_URL to retrieve persisted account snapshots.",
            },
        )
    stored = _get_workpaper_repository().get_account_context(snapshot_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Account context record not found.",
                "fix": "Use a snapshot_id returned by POST /api/v1/civicutility/account-context.",
            },
        )
    return _stored_account_response(stored)


@app.post("/api/v1/civicutility/payment-arrangement-draft")
def payment_arrangement(request: ArrangementRequest) -> dict[str, object]:
    return draft_payment_arrangement(request.account_id, request.csr_inputs).__dict__


@app.post("/api/v1/civicutility/service-request-intake")
def service_request(request: ServiceRequestIntake) -> dict[str, object]:
    if _workpaper_database_url() is not None:
        return _stored_service_request_response(
            _get_workpaper_repository().create_service_request(**request.model_dump())
        )
    payload = prepare_service_request(**request.model_dump()).__dict__
    payload["intake_id"] = None
    return payload


@app.get("/api/v1/civicutility/service-request-intake/{intake_id}")
def get_service_request(intake_id: str) -> dict[str, object]:
    if _workpaper_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "CivicUtility workpaper persistence is not configured.",
                "fix": "Set CIVICUTILITY_WORKPAPER_DB_URL to retrieve persisted service-request intakes.",
            },
        )
    stored = _get_workpaper_repository().get_service_request(intake_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Service-request intake record not found.",
                "fix": "Use an intake_id returned by POST /api/v1/civicutility/service-request-intake.",
            },
        )
    return _stored_service_request_response(stored)


def _workpaper_database_url() -> str | None:
    return os.environ.get("CIVICUTILITY_WORKPAPER_DB_URL")


def _get_workpaper_repository() -> UtilityWorkpaperRepository:
    global _workpaper_db_url, _workpaper_repository
    db_url = _workpaper_database_url()
    if db_url is None:
        raise RuntimeError("CIVICUTILITY_WORKPAPER_DB_URL is not configured.")
    if _workpaper_repository is None or db_url != _workpaper_db_url:
        _dispose_workpaper_repository()
        _workpaper_db_url = db_url
        _workpaper_repository = UtilityWorkpaperRepository(db_url=db_url)
    return _workpaper_repository


def _dispose_workpaper_repository() -> None:
    global _workpaper_repository
    if _workpaper_repository is not None:
        _workpaper_repository.engine.dispose()
        _workpaper_repository = None


def _stored_account_response(stored: StoredAccountContext) -> dict[str, object]:
    return {**stored.__dict__, "created_at": stored.created_at.isoformat()}


def _stored_service_request_response(stored: StoredServiceRequest) -> dict[str, object]:
    return {**stored.__dict__, "created_at": stored.created_at.isoformat()}
