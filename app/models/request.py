"""
Request Models
"""
from typing import Optional, Dict
from pydantic import BaseModel


class SendScriptRequest(BaseModel):
    """Request model for sending script to PC"""
    pc_id: str
    script_name: str
    server_url: Optional[str] = None
    script_params: Optional[Dict[str, str]] = None  # Script parameters


class BroadcastScriptRequest(BaseModel):
    """Request model for broadcasting script"""
    script_name: str
    server_url: Optional[str] = None
    script_params: Optional[Dict[str, str]] = None  # Script parameters

