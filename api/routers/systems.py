from fastapi import APIRouter, HTTPException
from typing import List
from api.models.ai_system import AISystem, RiskClassification, ModelType
from mapper.engine import ControlMapper
from mapper.loader import load_controls, load_mappings
import glob
import os

router = APIRouter(prefix="/api/systems", tags=["systems"])

# In-memory database for mock data
mock_systems_db = [
    AISystem(
        id="SYS-001",
        name="Credit Scoring Bot",
        owner="Alice Compliance",
        business_unit="Finance",
        description="Automated credit decisioning",
        intended_purpose="Determine credit worthiness",
        inputs=["Credit history", "Income"],
        outputs=["Credit Score", "Approval Decision"],
        data_sources=["Internal DB", "Equifax"],
        model_type=ModelType.CLASSICAL_ML,
        deployment_context="customer-facing",
        eu_ai_act_risk_classification=RiskClassification.HIGH,
        framework_profiles=["NIST-AIRMF", "EU-AIACT"]
    )
]

def get_engine():
    controls = []
    for file_path in glob.glob("data/*_controls.csv"):
        framework = os.path.basename(file_path).replace("_controls.csv", "").upper().replace("_", "")
        if framework == "NIST80053": framework = "NIST800-53"
        elif framework == "NIST800171": framework = "NIST800-171"
        elif framework == "NISTCSF": framework = "NIST-CSF"
        controls += load_controls(file_path, framework)
    mappings = load_mappings("data/mappings.csv")
    return ControlMapper(controls, mappings)

mapper_engine = None
try:
    mapper_engine = get_engine()
except Exception as e:
    print(f"Failed to load engine: {e}")

@router.get("/", response_model=List[AISystem])
async def list_systems():
    return mock_systems_db

@router.post("/", response_model=AISystem)
async def create_system(system: AISystem):
    mock_systems_db.append(system)
    return system

@router.get("/{system_id}", response_model=AISystem)
async def get_system(system_id: str):
    for s in mock_systems_db:
        if s.id == system_id:
            return s
    raise HTTPException(status_code=404, detail="System not found")

@router.get("/{system_id}/controls")
async def get_system_controls(system_id: str):
    # This endpoint demonstrates how we fetch controls for the frameworks applied to the system.
    system = await get_system(system_id)
    if not mapper_engine:
        raise HTTPException(status_code=500, detail="Mapping engine not initialized")

    applicable_controls = []
    for framework in system.framework_profiles:
        # Get all base controls for this framework from the engine
        f_controls = [c for c in mapper_engine.controls if c.framework == framework]
        # In a real app, we would cross-check which controls specifically apply based on Risk level/Profile
        # For now, we just return the count and top 5 as a sample
        applicable_controls.append({
            "framework": framework,
            "total_controls": len(f_controls),
            "sample_controls": [{"id": c.id, "name": c.name} for c in f_controls[:5]]
        })
    return {"system_id": system_id, "applicable_frameworks": applicable_controls}
