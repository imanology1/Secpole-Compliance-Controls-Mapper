from fastapi import APIRouter, HTTPException
from typing import List
from api.models.ai_system import AISystem
from api.models.evidence import Evidence
from api.datastore import store
from mapper.engine import ControlMapper, UnknownFrameworkError
from mapper.loader import load_controls, load_mappings
from mapper.frameworks import discover_control_files

router = APIRouter(prefix="/api/systems", tags=["systems"])


def get_engine():
    controls = []
    for file_path, framework in discover_control_files("data"):
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
    return store.systems


@router.post("/", response_model=AISystem)
async def create_system(system: AISystem):
    store.systems.append(system)
    return system


@router.get("/{system_id}", response_model=AISystem)
async def get_system(system_id: str):
    s = store.get_system(system_id)
    if s is None:
        raise HTTPException(status_code=404, detail="System not found")
    return s


@router.get("/{system_id}/controls")
async def get_system_controls(system_id: str):
    """Return the applicable controls for each framework profile on the system."""
    system = await get_system(system_id)
    if not mapper_engine:
        raise HTTPException(status_code=500, detail="Mapping engine not initialized")

    applicable = []
    for framework in system.framework_profiles:
        try:
            mapper_engine._require_framework(framework)
        except UnknownFrameworkError:
            applicable.append({
                "framework": framework,
                "total_controls": 0,
                "sample_controls": [],
                "note": "Framework not present in loaded data",
            })
            continue
        f_controls = [c for c in mapper_engine.controls if c.framework == framework]
        applicable.append({
            "framework": framework,
            "total_controls": len(f_controls),
            "sample_controls": [{"id": c.id, "name": c.name} for c in f_controls[:5]],
        })
    return {"system_id": system_id, "applicable_frameworks": applicable}


@router.get("/{system_id}/evidence", response_model=List[Evidence])
async def get_system_evidence(system_id: str):
    await get_system(system_id)  # 404 if missing
    return store.evidence_for_system(system_id)


@router.post("/{system_id}/evidence", response_model=Evidence)
async def add_system_evidence(system_id: str, evidence: Evidence):
    await get_system(system_id)
    store.evidence.append(evidence)
    return evidence


@router.get("/{system_id}/coverage")
async def get_system_coverage(system_id: str, target: str):
    """Coverage of each of the system's framework profiles against a target framework."""
    system = await get_system(system_id)
    if not mapper_engine:
        raise HTTPException(status_code=500, detail="Mapping engine not initialized")
    out = []
    for fw in system.framework_profiles:
        try:
            out.append(mapper_engine.get_coverage(fw, target))
        except UnknownFrameworkError as e:
            out.append({"source_framework": fw, "target_framework": target, "error": str(e)})
    return {"system_id": system_id, "coverage": out}
