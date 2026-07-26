from pydantic import BaseModel, Field

class ControlMapping(BaseModel):
    source_framework: str
    source_id: str
    target_framework: str
    target_id: str
    relationship: str
    justification: str = Field(default="")
