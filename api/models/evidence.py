from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Evidence(BaseModel):
    id: str = Field(..., description="Unique Evidence ID")
    system_id: str
    control_id: str
    name: str
    description: str
    url: Optional[str] = None
    uploaded_by: str
    uploaded_at: datetime
