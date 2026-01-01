"""
Script Routes
"""
from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional, Dict
from app.services.script_service import ScriptService
from app.services.pc_service import PCService
from app.websocket.connection_manager import manager
from app.models.request import SendScriptRequest, BroadcastScriptRequest
from app.config import settings

router = APIRouter(prefix="/api/scripts", tags=["Scripts"])


@router.get("")
async def list_scripts():
    """List all available scripts from filesystem"""
    scripts = await ScriptService.list_scripts()
    return {
        "total": len(scripts),
        "scripts": [script.dict() for script in scripts]
    }


@router.post("/send")
async def send_script(request: SendScriptRequest):
    """
    Send a script to a specific PC
    
    Request Body (JSON):
    {
        "pc_id": "PC_ID_HERE",
        "script_name": "script_name.py",
        "server_url": "http://server:port" (optional),
        "script_params": {
            "PARAM_NAME": "value"
        } (optional)
    }
    """
    pc_id = request.pc_id
    script_name = request.script_name
    server_url = request.server_url
    params_to_use = request.script_params
    
    # Check if PC is connected
    if not manager.is_connected(pc_id):
        raise HTTPException(status_code=404, detail=f"PC '{pc_id}' is not connected")
    
    # Get script content
    script_content = await ScriptService.get_script_content(script_name)
    if not script_content:
        raise HTTPException(status_code=404, detail=f"Script '{script_name}' not found")
    
    # Use Serverurl from .env if not provided, fallback to default
    server_url = server_url or settings.SERVER_URL or f"http://{settings.HOST}:{settings.PORT}"
    
    # Send script with parameters
    success = await manager.send_script(pc_id, script_name, script_content, server_url, params_to_use)
    
    if success:
        return {
            "status": "success",
            "message": f"Script '{script_name}' sent to PC '{pc_id}'",
            "pc_id": pc_id,
            "script_name": script_name
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to send script")


@router.post("/broadcast")
async def broadcast_script(request: BroadcastScriptRequest):
    """
    Broadcast a script to all connected PCs
    
    Request Body (JSON):
    {
        "script_name": "script_name.py",
        "server_url": "http://server:port" (optional),
        "script_params": {
            "PARAM_NAME": "value"
        } (optional)
    }
    """
    script_name = request.script_name
    server_url = request.server_url
    params_to_use = request.script_params
    
    # Get script content
    script_content = await ScriptService.get_script_content(script_name)
    if not script_content:
        raise HTTPException(status_code=404, detail=f"Script '{script_name}' not found")
    
    # Use Serverurl from .env if not provided, fallback to default
    server_url = server_url or settings.SERVER_URL or f"http://{settings.HOST}:{settings.PORT}"
    
    # Broadcast to all PCs
    connected_pcs = manager.get_connected_pc_ids()
    for pc_id in connected_pcs:
        await manager.send_script(pc_id, script_name, script_content, server_url, params_to_use)
    
    return {
        "status": "success",
        "message": f"Script '{script_name}' broadcasted to {len(connected_pcs)} PC(s)",
        "script_name": script_name,
        "recipients": len(connected_pcs)
    }

