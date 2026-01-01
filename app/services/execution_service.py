"""
Execution Service - Business logic for script execution tracking
"""
from typing import List, Optional
from datetime import datetime
from app.database import get_database
from app.models.execution import Execution, ExecutionCreate, ExecutionInDB
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


class ExecutionService:
    """Service for managing script executions"""
    
    @staticmethod
    async def create_execution(execution: ExecutionCreate) -> ExecutionInDB:
        """Create a new execution record"""
        db = get_database()
        now = datetime.utcnow()
        
        execution_data = {
            "pc_id": execution.pc_id,
            "script_name": execution.script_name,
            "status": execution.status,
            "executed_at": now,
            "completed_at": None,
            "error_message": None,
            "result": None
        }
        
        result = await db.executions.insert_one(execution_data)
        execution_data["_id"] = result.inserted_id
        execution_data["_id"] = str(execution_data["_id"])
        return ExecutionInDB(**execution_data)
    
    @staticmethod
    async def update_execution_status(execution_id: str, status: str, 
                                      error_message: Optional[str] = None,
                                      result: Optional[dict] = None) -> Optional[ExecutionInDB]:
        """Update execution status"""
        db = get_database()
        now = datetime.utcnow()
        
        update_data = {
            "status": status,
            "last_updated": now
        }
        
        if status in ["success", "failed"]:
            update_data["completed_at"] = now
        
        if error_message:
            update_data["error_message"] = error_message
        
        if result:
            update_data["result"] = result
        
        result = await db.executions.find_one_and_update(
            {"_id": ObjectId(execution_id)},
            {"$set": update_data},
            return_document=True
        )
        
        if result:
            result["_id"] = str(result["_id"])
            return ExecutionInDB(**result)
        return None
    
    @staticmethod
    async def get_execution(execution_id: str) -> Optional[ExecutionInDB]:
        """Get an execution by ID"""
        db = get_database()
        execution_data = await db.executions.find_one({"_id": ObjectId(execution_id)})
        if execution_data:
            execution_data["_id"] = str(execution_data["_id"])
            return ExecutionInDB(**execution_data)
        return None
    
    @staticmethod
    async def get_pc_executions(pc_id: str, limit: int = 50) -> List[ExecutionInDB]:
        """Get executions for a specific PC"""
        db = get_database()
        cursor = db.executions.find({"pc_id": pc_id}).sort("executed_at", -1).limit(limit)
        executions = []
        async for execution_data in cursor:
            execution_data["_id"] = str(execution_data["_id"])
            executions.append(ExecutionInDB(**execution_data))
        return executions
    
    @staticmethod
    async def get_script_executions(script_name: str, limit: int = 50) -> List[ExecutionInDB]:
        """Get executions for a specific script"""
        db = get_database()
        cursor = db.executions.find({"script_name": script_name}).sort("executed_at", -1).limit(limit)
        executions = []
        async for execution_data in cursor:
            execution_data["_id"] = str(execution_data["_id"])
            executions.append(ExecutionInDB(**execution_data))
        return executions
    
    @staticmethod
    async def get_recent_executions(limit: int = 100) -> List[ExecutionInDB]:
        """Get recent executions"""
        db = get_database()
        cursor = db.executions.find().sort("executed_at", -1).limit(limit)
        executions = []
        async for execution_data in cursor:
            execution_data["_id"] = str(execution_data["_id"])
            executions.append(ExecutionInDB(**execution_data))
        return executions

