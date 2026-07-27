# Bug Fixes — Secpol Compliance Control Mapper

This changelog documents corrections applied to the original project.

## 1. Honest coverage calculation (correctness)
`get_coverage` previously measured against only the controls defined in the
local `*_controls.csv` files — a tiny, arbitrary subset (NIST800-53 had 15 rows
vs ~1000 real controls). The percentage looked authoritative but was meaningless.
Now the denominator is the full set of control IDs known for a framework
(defined locally OR referenced anywhere in mappings), and the output additionally
reports `defined_controls` so the gap between "known" and "locally described" is
transparent.

## 2. Missing control definitions for advertised AI-governance frameworks
EU-AIACT, NIST-AIRMF, ISO42001 and GDPR were referenced in thousands of mappings
but had no `_controls.csv`, so lookups rendered as "Unknown (Control details not
loaded)". Added stub control files carrying the real control IDs. These are
clearly marked `[Auto-generated stub]` in the description field — they are NOT
authoritative regulatory text and must be replaced with official wording before
use in any real assessment.

## 3. SOC2 namespace collision
The data produced four separate SOC2 namespaces: SOC2, SOC2TYPE1, SOC2TYPE2,
SOC2TYPE3. Mappings only ever referenced `SOC2`, so the Type files were dead
weight. Consolidated all distinct CC controls (CC1.x–CC7.x, 13 total) into a
single `soc2_controls.csv`, deleted the Type files, and rewrote the 2 stray
mapping rows that referenced `SOC2TYPE*` to `SOC2`. There is now one SOC2 namespace.

## 4. Triplicated framework-name normalization
The `NIST80053 -> NIST800-53` alias logic was copy-pasted as an if/elif ladder in
`cli.py`, `api/routers/systems.py`, and the README. Centralized into a single
module, `mapper/frameworks.py`, with an explicit alias table. Onboarding a
framework whose file slug differs from its mapping name is now a one-line change.

## 5. Duplicate / junk data
Removed `data/data/mappings.csv` (a stale, conflicting nested copy that risked
double-loading) and the macOS `__MACOSX/` resource-fork artifacts.

## 6. Input validation
- The loader now validates required CSV columns and raises a clear error instead
  of failing deep inside pandas. Rows with a blank id are skipped.
- Querying an unknown framework now raises `UnknownFrameworkError` with the list
  of valid frameworks, and the CLI prints a clean message + exit code 1 instead
  of a traceback (or a silently misleading "0% / not found").

## 7. Packaging
`requirements.txt` now includes all runtime deps (fastapi, uvicorn were missing
from the README's stated list) with minimum version floors.

## Note on the batch-1 PCI-DSS finding
The initial analysis flagged "PCI-DSS has zero mappings." That was a false alarm
caused by grepping the wrong token: PCI is present as `PCIDSS` (244 mappings),
plus `PCI_PTS` and `PCI_HSM`. No fix needed.

---

# Batch 2 — New Features

## Multi-hop / transitive mapping (`trace`, `map-transitive`)
`ControlMapper.find_path` (BFS, cycle-safe) and `map_control_transitive` walk
chains of mappings through intermediate frameworks (e.g. via SCF), turning the
existing ~27k relationships into far broader reachable coverage. Each transitive
result carries a hop count and a confidence score = product of edge weights.

## Gap analysis (`gap`)
`ControlMapper.get_gaps` returns the exact source controls with no mapping to a
target framework — the inverse of coverage and the real audit output.

## Weighted coverage
`get_coverage` now also returns `weighted_coverage_percent`, scoring each mapped
control by its strongest edge (equivalent=1.0, partial=0.5, related=0.25) so a
"related"-only mapping no longer counts as full coverage.

## Excel report (`report`)
New `mapper/report.py` builds a formatted .xlsx: a colour-coded N×N coverage
matrix on a Summary sheet, plus one detail sheet per framework pair listing all
mapped controls and all gaps. Requires openpyxl (added to requirements.txt).

---

# Batch 3 — Audit Simulation (seeded API + frontend)

## Fake company seed (data/seed_company.json)
A fictional fintech, "Meridian Financial Services", with 4 AI systems across all
EU AI Act risk tiers (high/limited/minimal), 5 risks, and 4 evidence artifacts.
Fully editable — change the JSON, restart, and the whole pipeline picks it up.

## Seeded data store (api/datastore.py)
Replaced the hardcoded mock lists in the routers with a single in-memory store
seeded from the JSON file. Still resets on restart (durable persistence is a
future step), but now every router reads one seeded source.

## Router changes
- systems + risks routers now read/write the shared store.
- Wired up the previously-unused Evidence model: GET/POST /api/systems/{id}/evidence.
- Added GET /api/systems/{id}/coverage?target=... (per-profile coverage).
- get_system_controls now validates each framework instead of assuming it loads.
- main.py adds GET /api/company and POST /api/reseed (reset state during a demo).

## One-command run (run_demo.sh) + AUDIT_SIMULATION.md
Starts the seeded API (:8000) and Next.js dashboard (:3000) together, with a
documented step-by-step audit walkthrough. Frontend build verified (next build
compiles all 8 pages against the seeded endpoints).
