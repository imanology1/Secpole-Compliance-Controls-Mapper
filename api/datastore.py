"""In-memory data store, seeded from data/seed_company.json.

Replaces the previously-hardcoded mock lists scattered across routers with a
single seeded source of truth. Still in-memory (resets on restart) — batch 3's
goal is a seeded, runnable API, not durable persistence. Swapping this for
SQLite/SQLModel later only touches this module.
"""

import json
import os
from typing import List

from api.models.ai_system import AISystem
from api.models.risk import Risk
from api.models.evidence import Evidence

SEED_PATH = os.environ.get(
    "SECPOL_SEED",
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "seed_company.json"),
)


class DataStore:
    def __init__(self):
        self.company: dict = {}
        self.systems: List[AISystem] = []
        self.risks: List[Risk] = []
        self.evidence: List[Evidence] = []
        self.load_seed()

    def load_seed(self, path: str = SEED_PATH):
        """(Re)load all collections from the seed file. Falls back to empty
        collections if the seed is missing, so the API still boots."""
        self.company, self.systems, self.risks, self.evidence = {}, [], [], []
        if not os.path.exists(path):
            print(f"[datastore] seed not found at {path}; starting empty")
            return
        with open(path) as f:
            data = json.load(f)
        self.company = data.get("company", {})
        self.systems = [AISystem(**s) for s in data.get("systems", [])]
        self.risks = [Risk(**r) for r in data.get("risks", [])]
        self.evidence = [Evidence(**e) for e in data.get("evidence", [])]
        print(f"[datastore] seeded '{self.company.get('name','?')}': "
              f"{len(self.systems)} systems, {len(self.risks)} risks, "
              f"{len(self.evidence)} evidence")

    # --- lookups ---
    def get_system(self, system_id: str):
        return next((s for s in self.systems if s.id == system_id), None)

    def risks_for_system(self, system_id: str):
        return [r for r in self.risks if r.system_id == system_id]

    def evidence_for_system(self, system_id: str):
        return [e for e in self.evidence if e.system_id == system_id]


# Singleton shared by all routers.
store = DataStore()
