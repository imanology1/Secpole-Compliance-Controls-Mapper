from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import systems, risks
from api.datastore import store

app = FastAPI(
    title="Secpol - AI Compliance OS API",
    description="API for managing AI Systems, Risks, and Compliance Mappings.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(systems.router)
app.include_router(risks.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/company")
def company_info():
    """The seeded organization being audited, with headline counts."""
    return {
        **store.company,
        "counts": {
            "systems": len(store.systems),
            "risks": len(store.risks),
            "evidence": len(store.evidence),
        },
    }


@app.post("/api/reseed")
def reseed():
    """Reset all collections back to the seed file (useful during a demo)."""
    store.load_seed()
    return {"status": "reseeded", "company": store.company.get("name")}
