"""
Script Models
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Script(BaseModel):
    """Script model for API responses"""
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    name: str
    size: int
    path: Optional[str] = None
    description: Optional[str] = None
    updated_at: Optional[datetime] = None
    parameters: Optional[Dict[str, Dict[str, Any]]] = None  # Script parameters detected from code

