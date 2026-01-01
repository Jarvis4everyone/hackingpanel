"""
Execution Routes
"""
from fastapi import APIRouter, HTTPException, Query
from app.services.execution_service import ExecutionService
from app.models.execution import ExecutionInDB

router = APIRouter(prefix="/api/executions", tags=["Executions"])


@router.get("", response_model=dict)
async def list_executions(limit: int = Query(100, ge=1, le=1000)):
    """Get recent executions"""
    executions = await ExecutionService.get_recent_executions(limit=limit)
    return {
        "total": len(executions),
        "executions": [execution.dict() for execution in executions]
    }


@router.get("/{execution_id}", response_model=ExecutionInDB)
async def get_execution(execution_id: str):
    """Get a specific execution by ID"""
    execution = await ExecutionService.get_execution(execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail=f"Execution '{execution_id}' not found")
    return execution


@router.get("/pc/{pc_id}", response_model=dict)
async def get_pc_executions(pc_id: str, limit: int = Query(50, ge=1, le=500)):
    """Get executions for a specific PC"""
    executions = await ExecutionService.get_pc_executions(pc_id, limit=limit)
    return {
        "pc_id": pc_id,
        "total": len(executions),
        "executions": [execution.dict() for execution in executions]
    }


@router.get("/script/{script_name}", response_model=dict)
async def get_script_executions(script_name: str, limit: int = Query(50, ge=1, le=500)):
    """Get executions for a specific script"""
    executions = await ExecutionService.get_script_executions(script_name, limit=limit)
    return {
        "script_name": script_name,
        "total": len(executions),
        "executions": [execution.dict() for execution in executions]
    }

