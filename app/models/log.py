"""
Log Models
"""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Log(BaseModel):
    """Log model for API responses"""
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    pc_id: str
    script_name: str
    execution_id: Optional[str] = None
    log_file_path: Optional[str] = None
    log_content: str
    log_level: str = "INFO"  # INFO, ERROR, WARNING, DEBUG, SUCCESS
    timestamp: Optional[datetime] = None


class LogCreate(BaseModel):
    """Log creation model"""
    pc_id: str
    script_name: str
    execution_id: Optional[str] = None
    log_file_path: Optional[str] = None
    log_content: str
    log_level: str = "INFO"


class LogInDB(Log):
    """Log model with database ID"""
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    id: Optional[str] = Field(default=None, alias="_id")

