"""FastAPI runtime foundation for CivicUtility."""

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicutility import __version__
from civicutility.account import summarize_account_context
from civicutility.arrangements import draft_payment_arrangement
from civicutility.policy import UtilityPolicySource, answer_utility_question
from civicutility.public_ui import render_public_lookup_page
from civicutility.service_requests import prepare_service_request

app = FastAPI(
    title="CivicUtility",
    version=__version__,
    description="Utility customer-service copilot foundation for CivicSuite.",
)

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
            "service-request intake, and public UI foundation are online; utility billing, "
            "payments, shutoff/reconnect decisions, live billing connectors, live LLM calls, "
            "and Civic311 write-back are not implemented yet."
        ),
        "next_step": "Post-v0.1.0 roadmap: billing-system read adapters and Civic311 handoff integration",
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
    return summarize_account_context(**request.model_dump()).__dict__


@app.post("/api/v1/civicutility/payment-arrangement-draft")
def payment_arrangement(request: ArrangementRequest) -> dict[str, object]:
    return draft_payment_arrangement(request.account_id, request.csr_inputs).__dict__


@app.post("/api/v1/civicutility/service-request-intake")
def service_request(request: ServiceRequestIntake) -> dict[str, object]:
    return prepare_service_request(**request.model_dump()).__dict__
