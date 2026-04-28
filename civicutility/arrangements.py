"""Payment-arrangement drafting helpers for CSR review."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentArrangementDraft:
    account_id: str
    proposed_terms: tuple[str, ...]
    csr_review_required: bool
    not_payment_processing: bool
    boundary: str


def draft_payment_arrangement(account_id: str, csr_inputs: list[str]) -> PaymentArrangementDraft:
    terms = tuple(csr_inputs) if csr_inputs else ("Collect current balance and hardship context.",)
    return PaymentArrangementDraft(
        account_id=account_id,
        proposed_terms=terms,
        csr_review_required=True,
        not_payment_processing=True,
        boundary=(
            "Draft only: CivicUtility does not process payments, approve arrangements, "
            "change account status, or replace the utility billing system."
        ),
    )
