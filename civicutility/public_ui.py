"""HTML landing surface for the CivicUtility runtime."""


def render_public_lookup_page() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
  <title>CivicUtility v0.1.1</title>
  <style>
    :root{--ink:#18211f;--muted:#52615d;--line:#b8d1c7;--card:#fffaf1;--accent:#0f766e;--bg:#eef8f3}
    body{margin:0;font-family:Aptos,Segoe UI,sans-serif;background:radial-gradient(circle at 10% 10%,#d8fff4,var(--bg) 38%,#fff7e8);color:var(--ink)}
    main{width:min(1080px,calc(100% - 32px));margin:auto;padding:52px 0}
    h1{font:800 clamp(2.3rem,7vw,5rem)/.95 Georgia,serif;margin:.2em 0}
    .eyebrow{font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
    .grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:28px}
    .card{background:rgba(255,250,241,.92);border:1px solid var(--line);border-radius:24px;padding:24px;box-shadow:0 18px 50px rgba(21,62,50,.10)}
    code{background:#e2f5ee;padding:.14rem .36rem;border-radius:.5rem}
    a{color:#0f766e;font-weight:700}
    @media(max-width:800px){.grid{grid-template-columns:1fr}main{padding:34px 0}}
  </style>
</head>
<body>
<main>
  <p class="eyebrow">CivicSuite / CivicUtility</p>
  <h1>Utility customer service without touching billing systems.</h1>
  <p>CivicUtility v0.1.1 helps CSRs answer cited billing-policy questions, view safe read-only account context, draft payment arrangements for review, and prepare service-request handoffs.</p>
  <section class="grid">
    <article class="card"><h2>Ships Today</h2><p>Policy Q&A, CSR-safe account summaries, arrangement drafts, service request intake, and deterministic API endpoints.</p></article>
    <article class="card"><h2>Human Review</h2><p>CSRs approve resident-facing answers, account guidance, and any arrangement language before use.</p></article>
    <article class="card"><h2>Boundary</h2><p>No utility billing, payments, shutoff decisions, rate-engine behavior, live LLM calls, or billing-system write-back ships in v0.1.1.</p></article>
  </section>
  <section class="card" style="margin-top:24px">
    <h2>Architecture</h2>
    <p><strong>Resident / CSR request</strong> → CivicUtility deterministic API → CivicCore foundation. External billing and Civic311 integrations are read/handoff roadmap items, not v0.1.1 write paths.</p>
  </section>
  <p>Dependency: <code>civiccore==0.3.0</code>. Repo: <a href="https://github.com/CivicSuite/civicutility">CivicSuite/civicutility</a>.</p>
</main>
</body>
</html>
"""
