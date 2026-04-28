"""Read-only utility account context helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class UtilityAccountSnapshot:
    account_id: str
    customer_name: str
    service_address: str
    balance_status: str
    last_bill_summary: str
    restricted_fields_hidden: bool = True
    read_only: bool = True


def summarize_account_context(
    account_id: str,
    customer_name: str,
    service_address: str,
    balance_status: str,
    last_bill_summary: str,
) -> UtilityAccountSnapshot:
    """Return CSR-safe account context without payment instruments or write actions."""

    return UtilityAccountSnapshot(
        account_id=account_id,
        customer_name=customer_name,
        service_address=service_address,
        balance_status=balance_status,
        last_bill_summary=last_bill_summary,
    )
