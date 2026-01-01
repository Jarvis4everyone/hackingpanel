"""
PC Models
"""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class PC(BaseModel):
    """PC model for API responses"""
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    pc_id: str
    name: Optional[str] = None
    connected: bool = False
    connected_at: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    ip_address: Optional[str] = None
    hostname: Optional[str] = None
    os_info: Optional[dict] = None
    metadata: Optional[dict] = None


class PCInDB(PC):
    """PC model with database ID"""
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    id: Optional[str] = Field(default=None, alias="_id")


class PCConnection(BaseModel):
    """PC connection status"""
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    pc_id: str
    connected: bool
    connected_at: Optional[datetime] = None
    last_seen: Optional[datetime] = None

