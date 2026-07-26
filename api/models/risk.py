from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

class RiskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    MITIGATED = "mitigated"
    ACCEPTED = "accepted"

class RiskSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Risk(BaseModel):
    id: str = Field(..., description="Unique Risk ID")
    system_id: str = Field(..., description="The ID of the AI System this risk applies to")
    name: str
    description: str
    severity: RiskSeverity
    status: RiskStatus
    owner: str
    mitigation_plan: Optional[str] = None
    due_date: Optional[datetime] = None
    linked_controls: List[str] = Field(default_factory=list, description="List of control IDs (e.g. NIST-AIRMF MAP 1.1) that mitigate this risk")
