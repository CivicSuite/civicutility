from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civicutility.account import summarize_account_context
from civicutility.service_requests import prepare_service_request


metadata = sa.MetaData()

account_context_records = sa.Table(
    "account_context_records",
    metadata,
    sa.Column("snapshot_id", sa.String(36), primary_key=True),
    sa.Column("account_id", sa.String(255), nullable=False),
    sa.Column("customer_name", sa.String(255), nullable=False),
    sa.Column("service_address", sa.String(255), nullable=False),
    sa.Column("balance_status", sa.String(160), nullable=False),
    sa.Column("last_bill_summary", sa.Text(), nullable=False),
    sa.Column("restricted_fields_hidden", sa.Boolean(), nullable=False),
    sa.Column("read_only", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicutility",
)

service_request_records = sa.Table(
    "service_request_records",
    metadata,
    sa.Column("intake_id", sa.String(36), primary_key=True),
    sa.Column("account_id", sa.String(255), nullable=False),
    sa.Column("issue_type", sa.String(160), nullable=False),
    sa.Column("description", sa.Text(), nullable=False),
    sa.Column("location", sa.String(255), nullable=False),
    sa.Column("civic311_handoff_recommended", sa.Boolean(), nullable=False),
    sa.Column("not_work_order", sa.Boolean(), nullable=False),
    sa.Column("boundary", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicutility",
)


@dataclass(frozen=True)
class StoredAccountContext:
    snapshot_id: str
    account_id: str
    customer_name: str
    service_address: str
    balance_status: str
    last_bill_summary: str
    restricted_fields_hidden: bool
    read_only: bool
    created_at: datetime


@dataclass(frozen=True)
class StoredServiceRequest:
    intake_id: str
    account_id: str
    issue_type: str
    description: str
    location: str
    civic311_handoff_recommended: bool
    not_work_order: bool
    boundary: str
    created_at: datetime


class UtilityWorkpaperRepository:
    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"civicutility": None})
        else:
            self.engine = base_engine
            with self.engine.begin() as connection:
                connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civicutility"))
        metadata.create_all(self.engine)

    def create_account_context(
        self,
        *,
        account_id: str,
        customer_name: str,
        service_address: str,
        balance_status: str,
        last_bill_summary: str,
    ) -> StoredAccountContext:
        snapshot = summarize_account_context(
            account_id,
            customer_name,
            service_address,
            balance_status,
            last_bill_summary,
        )
        stored = StoredAccountContext(
            snapshot_id=str(uuid4()),
            account_id=snapshot.account_id,
            customer_name=snapshot.customer_name,
            service_address=snapshot.service_address,
            balance_status=snapshot.balance_status,
            last_bill_summary=snapshot.last_bill_summary,
            restricted_fields_hidden=snapshot.restricted_fields_hidden,
            read_only=snapshot.read_only,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(account_context_records.insert().values(**stored.__dict__))
        return stored

    def get_account_context(self, snapshot_id: str) -> StoredAccountContext | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(account_context_records).where(
                    account_context_records.c.snapshot_id == snapshot_id
                )
            ).mappings().first()
        return None if row is None else StoredAccountContext(**dict(row))

    def create_service_request(
        self, *, account_id: str, issue_type: str, description: str, location: str
    ) -> StoredServiceRequest:
        draft = prepare_service_request(account_id, issue_type, description, location)
        stored = StoredServiceRequest(
            intake_id=str(uuid4()),
            account_id=draft.account_id,
            issue_type=draft.issue_type,
            description=draft.description,
            location=draft.location,
            civic311_handoff_recommended=draft.civic311_handoff_recommended,
            not_work_order=draft.not_work_order,
            boundary=draft.boundary,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(service_request_records.insert().values(**stored.__dict__))
        return stored

    def get_service_request(self, intake_id: str) -> StoredServiceRequest | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(service_request_records).where(
                    service_request_records.c.intake_id == intake_id
                )
            ).mappings().first()
        return None if row is None else StoredServiceRequest(**dict(row))
