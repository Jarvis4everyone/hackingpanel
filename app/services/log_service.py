"""
Log Service - Business logic for script logs management
"""
from typing import List, Optional
from datetime import datetime
from app.database import get_database
from app.models.log import Log, LogCreate, LogInDB
import logging

logger = logging.getLogger(__name__)


class LogService:
    """Service for managing script logs"""
    
    @staticmethod
    async def create_log(log: LogCreate) -> LogInDB:
        """Create a new log entry"""
        db = get_database()
        now = datetime.utcnow()
        
        log_data = {
            "pc_id": log.pc_id,
            "script_name": log.script_name,
            "execution_id": log.execution_id,
            "log_file_path": log.log_file_path,
            "log_content": log.log_content,
            "log_level": log.log_level,
            "timestamp": now
        }
        
        result = await db.logs.insert_one(log_data)
        log_data["_id"] = str(result.inserted_id)
        return LogInDB(**log_data)
    
    @staticmethod
    async def get_log(log_id: str) -> Optional[LogInDB]:
        """Get a log by ID"""
        from bson import ObjectId
        db = get_database()
        log_data = await db.logs.find_one({"_id": ObjectId(log_id)})
        if log_data:
            log_data["_id"] = str(log_data["_id"])
            return LogInDB(**log_data)
        return None
    
    @staticmethod
    async def get_pc_logs(pc_id: str, limit: int = 100) -> List[LogInDB]:
        """Get logs for a specific PC"""
        db = get_database()
        cursor = db.logs.find({"pc_id": pc_id}).sort("timestamp", -1).limit(limit)
        logs = []
        async for log_data in cursor:
            log_data["_id"] = str(log_data["_id"])
            logs.append(LogInDB(**log_data))
        return logs
    
    @staticmethod
    async def get_script_logs(script_name: str, limit: int = 100) -> List[LogInDB]:
        """Get logs for a specific script"""
        db = get_database()
        cursor = db.logs.find({"script_name": script_name}).sort("timestamp", -1).limit(limit)
        logs = []
        async for log_data in cursor:
            log_data["_id"] = str(log_data["_id"])
            logs.append(LogInDB(**log_data))
        return logs
    
    @staticmethod
    async def get_execution_logs(execution_id: str) -> List[LogInDB]:
        """Get logs for a specific execution"""
        db = get_database()
        cursor = db.logs.find({"execution_id": execution_id}).sort("timestamp", 1)
        logs = []
        async for log_data in cursor:
            log_data["_id"] = str(log_data["_id"])
            logs.append(LogInDB(**log_data))
        return logs
    
    @staticmethod
    async def get_recent_logs(limit: int = 200) -> List[LogInDB]:
        """Get recent logs"""
        db = get_database()
        cursor = db.logs.find().sort("timestamp", -1).limit(limit)
        logs = []
        async for log_data in cursor:
            log_data["_id"] = str(log_data["_id"])
            logs.append(LogInDB(**log_data))
        return logs
    
    @staticmethod
    async def search_logs(pc_id: Optional[str] = None, 
                          script_name: Optional[str] = None,
                          log_level: Optional[str] = None,
                          limit: int = 100) -> List[LogInDB]:
        """Search logs with filters"""
        db = get_database()
        query = {}
        
        if pc_id:
            query["pc_id"] = pc_id
        if script_name:
            query["script_name"] = script_name
        if log_level:
            query["log_level"] = log_level
        
        cursor = db.logs.find(query).sort("timestamp", -1).limit(limit)
        logs = []
        async for log_data in cursor:
            log_data["_id"] = str(log_data["_id"])
            logs.append(LogInDB(**log_data))
        return logs

