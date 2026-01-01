"""
Execution Models
"""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Execution(BaseModel):
    """Execution model for API responses"""
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    pc_id: str
    script_name: str
    status: str  # pending, executing, success, failed
    executed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    result: Optional[dict] = None


class ExecutionCreate(BaseModel):
    """Execution creation model"""
    pc_id: str
    script_name: str
    status: str = "pending"


class ExecutionInDB(Execution):
    """Execution model with database ID"""
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    id: Optional[str] = Field(default=None, alias="_id")

