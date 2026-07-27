from fastapi import APIRouter, HTTPException
from typing import List
from api.models.risk import Risk
from api.datastore import store

router = APIRouter(prefix="/api/risks", tags=["risks"])


@router.get("/", response_model=List[Risk])
async def list_risks():
    return store.risks


@router.post("/", response_model=Risk)
async def create_risk(risk: Risk):
    store.risks.append(risk)
    return risk


@router.get("/system/{system_id}", response_model=List[Risk])
async def get_system_risks(system_id: str):
    return store.risks_for_system(system_id)
