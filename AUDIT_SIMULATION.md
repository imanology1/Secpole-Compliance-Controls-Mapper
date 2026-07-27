# Audit Simulation — Meridian Financial Services

This is a self-contained way to exercise Secpol end to end as if auditing a real
organization. Everything is fictional and lives in `data/seed_company.json` —
edit that file to change the company, then restart (or `POST /api/reseed`).

## The fake company

**Meridian Financial Services** — a consumer fintech (EU/Ireland HQ) running four
AI systems spanning every EU AI Act risk tier:

| System | Risk tier | Why |
|---|---|---|
| CreditLens Scoring Engine | **high** | Credit scoring = Annex III high-risk |
| SentinelAML Transaction Monitor | **high** | AML decisioning on individuals |
| Aria Support Assistant | **limited** | Generative chatbot → transparency duties |
| FraudGuard Realtime | **minimal** | Payment fraud scoring |

Plus 5 risks (open/in-progress/mitigated) and 4 evidence artifacts linked to
specific controls — enough to walk a coverage + gap + evidence review.

## Run it

```bash
./run_demo.sh
```

This installs deps, starts the seeded API on :8000 and the Next.js dashboard on
:3000. Then open:

- Dashboard: http://localhost:3000
- API docs (Swagger): http://localhost:8000/docs
- Company summary: http://localhost:8000/api/company

To run only the backend:

```bash
uvicorn api.main:app --reload --port 8000
```

## A sample audit walkthrough

1. **Inventory** — `GET /api/systems/` — confirm all four systems and their
   EU AI Act classifications are recorded (Article 9/Annex IV documentation duty).
2. **Per-system controls** — `GET /api/systems/SYS-001/controls` — which
   frameworks apply to CreditLens and how many controls each carries.
3. **Coverage** — `GET /api/systems/SYS-001/coverage?target=SCF` — how well each
   of the system's framework profiles maps onto the SCF meta-framework.
4. **Gaps (CLI)** — `python cli.py gap --source-framework EU-AIACT --target-framework SOC2`
   — where an EU AI Act obligation has no SOC2 equivalent to lean on.
5. **Evidence** — `GET /api/systems/SYS-001/evidence` — what proof exists, and
   for which controls. Note RSK-002 ("no human review on declines") is **open**
   with no evidence — a finding.
6. **Report** — `python cli.py report --frameworks "EU-AIACT,NIST-AIRMF,ISO27001,SOC2" --output meridian_audit.xlsx`
   — hand-off workbook with the coverage matrix and per-pair gaps.
7. **Reset** — `curl -X POST http://localhost:8000/api/reseed` — restore the
   seed after poking at POST endpoints.

## Editing the company

`data/seed_company.json` has three arrays — `systems`, `risks`, `evidence` — plus
a `company` block. Field shapes match the pydantic models in `api/models/`. Add a
system, set its `framework_profiles`, restart, and the whole pipeline (controls,
coverage, gaps, report) picks it up with no code changes.

> Note: the AI-governance frameworks (EU-AIACT, NIST-AIRMF, ISO42001, GDPR) use
> **auto-generated stub control descriptions** (see FIXES.md). Coverage/gap
> mechanics are real, but the control *text* is placeholder until replaced with
> authoritative wording — don't treat this as a real compliance assessment.
