from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class RiskClassification(str, Enum):
    UNACCEPTABLE = "unacceptable"
    HIGH = "high"
    LIMITED = "limited"
    MINIMAL = "minimal"

class ModelType(str, Enum):
    FOUNDATION = "foundation_model"
    CLASSICAL_ML = "classical_ml"
    RULES_BASED = "rules_based"

class AISystem(BaseModel):
    id: str = Field(..., description="Unique ID for the AI System")
    name: str
    owner: str
    business_unit: str
    description: str
    intended_purpose: str
    inputs: List[str]
    outputs: List[str]
    data_sources: List[str]
    model_type: ModelType
    deployment_context: str
    eu_ai_act_risk_classification: RiskClassification
    framework_profiles: List[str] = Field(default_factory=list, description="e.g., NIST-AIRMF, EU-AIACT")
