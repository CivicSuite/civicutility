# Changelog

## [0.1.1] - 2026-04-28

### Changed

- Dependency-alignment release: moved CivicUtility to `civiccore==0.3.0` while preserving the existing v0.1.0 runtime foundation behavior.
- Updated CI, verification gates, package metadata, docs, runtime tests, landing page, and public UI labels for the v0.1.1 release.
- Added optional SQLAlchemy-backed CSR-safe account context and service-request workpaper persistence behind `CIVICUTILITY_WORKPAPER_DB_URL`, with retrieval endpoints and actionable setup errors.

## [0.1.0] - 2026-04-27

### Added

- CivicUtility runtime foundation with FastAPI health, root, public UI, and deterministic API endpoints.
- Utility-policy Q&A, CSR-safe account context, payment-arrangement drafts, and service-request intake helpers.
- Professional docs, browser QA artifacts, GitHub community templates, placeholder-import gate, release gate, and package build.
