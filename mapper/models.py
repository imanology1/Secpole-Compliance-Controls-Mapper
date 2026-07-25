from pydantic import BaseModel

class Control(BaseModel):
    framework: str
    id: str
    name: str
    description: str

class Mapping(BaseModel):
    source_framework: str
    source_id: str
    target_framework: str
    target_id: str
    relationship: str  # "equivalent", "partial", "related"
