"""Service request intake helpers with Civic311 handoff boundaries."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceRequestDraft:
    account_id: str
    issue_type: str
    description: str
    location: str
    civic311_handoff_recommended: bool
    not_work_order: bool
    boundary: str


def prepare_service_request(
    account_id: str, issue_type: str, description: str, location: str
) -> ServiceRequestDraft:
    return ServiceRequestDraft(
        account_id=account_id,
        issue_type=issue_type,
        description=description,
        location=location,
        civic311_handoff_recommended=True,
        not_work_order=True,
        boundary=(
            "Draft intake only: CivicUtility does not dispatch crews, create work orders, "
            "or replace Civic311/public works systems of record."
        ),
    )
