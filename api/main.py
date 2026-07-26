from fastapi import FastAPI
from api.routers import systems, risks

app = FastAPI(
    title="Secpol - AI Compliance OS API",
    description="API for managing AI Systems, Risks, and Compliance Mappings.",
    version="1.0.0"
)

app.include_router(systems.router)
app.include_router(risks.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
