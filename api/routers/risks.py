from fastapi import APIRouter, HTTPException
from typing import List
from api.models.risk import Risk, RiskStatus, RiskSeverity

router = APIRouter(prefix="/api/risks", tags=["risks"])

mock_risks_db = [
    Risk(
        id="RSK-001",
        system_id="SYS-001",
        name="Demographic Bias in Scoring",
        description="Model may disproportionately reject applicants based on zip code.",
        severity=RiskSeverity.HIGH,
        status=RiskStatus.OPEN,
        owner="Alice Compliance",
        linked_controls=["NIST-AIRMF GOVERN 1.2"]
    )
]

@router.get("/", response_model=List[Risk])
async def list_risks():
    return mock_risks_db

@router.get("/system/{system_id}", response_model=List[Risk])
async def get_system_risks(system_id: str):
    return [r for r in mock_risks_db if r.system_id == system_id]
