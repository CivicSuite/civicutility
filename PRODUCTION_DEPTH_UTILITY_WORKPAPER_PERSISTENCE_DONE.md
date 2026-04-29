# CivicUtility Production-Depth Workpaper Persistence

## Summary

CivicUtility now supports optional SQLAlchemy-backed persistence for CSR-safe account snapshots and service-request intake drafts. The feature is controlled by `CIVICUTILITY_WORKPAPER_DB_URL`; when it is absent, existing POST endpoints remain stateless and retrieval endpoints return actionable setup guidance.

## Shipped

- `UtilityWorkpaperRepository` with SQLite/local and schema-aware database support.
- Persisted account context records with `snapshot_id` retrieval.
- Persisted service-request intake records with `intake_id` retrieval.
- API round-trip tests, repository reload tests, and no-config/missing-record error tests.
- Current-facing README, manual, changelog, and landing-page updates.

## Verification

- `python -m pytest --collect-only -q`
- `python -m pytest -q`
- `bash scripts/verify-release.sh`
- Browser QA desktop/mobile for `/docs/index.html`.

## Boundary

CivicUtility persistence is limited to CSR-safe workpapers. It still does not process payments, approve arrangements, modify accounts, decide shutoffs or reconnects, dispatch crews, call live LLMs, or write back to Civic311 or utility billing systems.
