"""
Log Routes - Script logs management
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.services.log_service import LogService
from app.models.log import LogCreate, LogInDB
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/logs", tags=["Logs"])


@router.post("", response_model=LogInDB)
async def create_log(log: LogCreate):
    """Create a new log entry"""
    try:
        log_entry = await LogService.create_log(log)
        return log_entry
    except Exception as e:
        logger.error(f"Error creating log: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating log: {str(e)}")


@router.get("", response_model=dict)
async def get_logs(
    limit: int = Query(200, ge=1, le=1000, description="Number of logs to retrieve"),
    pc_id: Optional[str] = Query(None, description="Filter by PC ID"),
    script_name: Optional[str] = Query(None, description="Filter by script name"),
    log_level: Optional[str] = Query(None, description="Filter by log level")
):
    """Get logs with optional filters"""
    try:
        if pc_id or script_name or log_level:
            logs = await LogService.search_logs(
                pc_id=pc_id,
                script_name=script_name,
                log_level=log_level,
                limit=limit
            )
        else:
            logs = await LogService.get_recent_logs(limit=limit)
        
        return {
            "total": len(logs),
            "logs": [log.dict() for log in logs]
        }
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting logs: {str(e)}")


@router.get("/{log_id}", response_model=LogInDB)
async def get_log(log_id: str):
    """Get a specific log by ID"""
    log_entry = await LogService.get_log(log_id)
    if not log_entry:
        raise HTTPException(status_code=404, detail=f"Log '{log_id}' not found")
    return log_entry


@router.get("/pc/{pc_id}", response_model=dict)
async def get_pc_logs(
    pc_id: str,
    limit: int = Query(100, ge=1, le=500, description="Number of logs to retrieve")
):
    """Get logs for a specific PC"""
    try:
        logs = await LogService.get_pc_logs(pc_id, limit=limit)
        return {
            "pc_id": pc_id,
            "total": len(logs),
            "logs": [log.dict() for log in logs]
        }
    except Exception as e:
        logger.error(f"Error getting PC logs: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting PC logs: {str(e)}")


@router.get("/script/{script_name}", response_model=dict)
async def get_script_logs(
    script_name: str,
    limit: int = Query(100, ge=1, le=500, description="Number of logs to retrieve")
):
    """Get logs for a specific script"""
    try:
        logs = await LogService.get_script_logs(script_name, limit=limit)
        return {
            "script_name": script_name,
            "total": len(logs),
            "logs": [log.dict() for log in logs]
        }
    except Exception as e:
        logger.error(f"Error getting script logs: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting script logs: {str(e)}")


@router.get("/execution/{execution_id}", response_model=dict)
async def get_execution_logs(execution_id: str):
    """Get logs for a specific execution"""
    try:
        logs = await LogService.get_execution_logs(execution_id)
        return {
            "execution_id": execution_id,
            "total": len(logs),
            "logs": [log.dict() for log in logs]
        }
    except Exception as e:
        logger.error(f"Error getting execution logs: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting execution logs: {str(e)}")

