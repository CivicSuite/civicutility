CivicUtility

CivicUtility v0.1.0 ships utility customer-service copilot foundations: cited utility-policy Q&A, CSR-safe read-only account context, payment-arrangement draft support, service-request intake, FastAPI runtime, public sample UI, docs, tests, browser QA, and release gates.

It is not a utility billing system, payment processor, rate engine, shutoff/reconnect workflow, system of record, live LLM runtime, live billing connector, or Civic311 write-back integration.

Install:
python -m pip install -e ".[dev]"
python -m uvicorn civicutility.main:app --host 127.0.0.1 --port 8142

CivicUtility v0.1.0 is pinned to civiccore==0.2.0.

Apache 2.0 code. CC BY 4.0 docs.
