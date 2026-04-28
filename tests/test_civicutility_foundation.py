from civicutility import __version__
from civicutility.account import summarize_account_context
from civicutility.arrangements import draft_payment_arrangement
from civicutility.policy import UtilityPolicySource, answer_utility_question
from civicutility.service_requests import prepare_service_request


def test_version_is_release_version():
    assert __version__ == "0.1.0"


def test_policy_answer_is_cited_and_boundary_limited():
    result = answer_utility_question(
        "what payment options exist",
        [UtilityPolicySource("u1", "Payment policy", "payment options", "Utility Manual 2")],
    )
    assert result.citations == ("Utility Manual 2",)
    assert result.csr_review_required is True
    assert "not a utility billing system" in result.boundary


def test_account_context_is_read_only_and_hides_restricted_fields():
    snapshot = summarize_account_context(
        "A-100",
        "Jordan Resident",
        "100 Water St",
        "current",
        "Last bill included water and sewer service.",
    )
    assert snapshot.read_only is True
    assert snapshot.restricted_fields_hidden is True


def test_payment_arrangement_draft_does_not_process_payments():
    draft = draft_payment_arrangement("A-100", ["Split balance across three billing cycles."])
    assert draft.csr_review_required is True
    assert draft.not_payment_processing is True
    assert "does not process payments" in draft.boundary


def test_service_request_intake_recommends_civic311_handoff():
    draft = prepare_service_request("A-100", "water leak", "Leak near meter", "100 Water St")
    assert draft.civic311_handoff_recommended is True
    assert draft.not_work_order is True
    assert "does not dispatch crews" in draft.boundary
