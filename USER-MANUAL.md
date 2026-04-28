# CivicUtility User Manual

## Non-Technical Staff

CivicUtility helps utility customer-service representatives prepare clear, cited answers about billing policies, service rules, payment options, conservation guidance, and service-request intake. It can summarize read-only account context in a CSR-safe way, draft payment-arrangement language for staff review, and prepare service-request handoffs.

Staff remain responsible for every resident-facing answer. CivicUtility does not approve payment arrangements, process payments, modify accounts, issue shutoff or reconnect decisions, dispatch crews, or replace the utility billing system.

## IT / Technical

Install with:

```bash
python -m pip install -e ".[dev]"
python -m uvicorn civicutility.main:app --host 127.0.0.1 --port 8142
```

Runtime dependency: `civiccore==0.3.0`.

Primary endpoints:

- `GET /health` - service and CivicCore version.
- `GET /civicutility` - public sample UI.
- `POST /api/v1/civicutility/policy-answer` - cited policy answer draft.
- `POST /api/v1/civicutility/account-context` - read-only CSR-safe account context.
- `POST /api/v1/civicutility/payment-arrangement-draft` - staff-review arrangement draft.
- `POST /api/v1/civicutility/service-request-intake` - Civic311 handoff-ready intake draft.

## Architecture

![CivicUtility architecture](docs/architecture-civicutility.svg)

CivicUtility is a module on top of CivicCore. v0.1.1 is deterministic and local: no live billing connector, live LLM call, account write, payment processing, or Civic311 write-back is shipped.
