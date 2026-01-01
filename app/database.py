"""
MongoDB Database Connection
"""
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class Database:
    """Database connection manager"""
    
    client: AsyncIOMotorClient = None
    database = None


db = Database()


async def connect_to_mongo():
    """Create database connection"""
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db.database = db.client[settings.MONGODB_DB_NAME]
        
        # Test connection
        await db.client.admin.command('ping')
        logger.info(f"Connected to MongoDB: {settings.MONGODB_DB_NAME}")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        logger.info("Disconnected from MongoDB")


async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # PCs collection indexes
        await db.database.pcs.create_index("pc_id", unique=True)
        await db.database.pcs.create_index("connected")
        await db.database.pcs.create_index("last_seen")
        
        # Executions collection indexes
        await db.database.executions.create_index("pc_id")
        await db.database.executions.create_index("script_name")
        await db.database.executions.create_index("executed_at")
        await db.database.executions.create_index([("pc_id", 1), ("executed_at", -1)])
        
        # Scripts collection indexes
        await db.database.scripts.create_index("name", unique=True)
        
        # Logs collection indexes
        await db.database.logs.create_index("pc_id")
        await db.database.logs.create_index("script_name")
        await db.database.logs.create_index("execution_id")
        await db.database.logs.create_index("timestamp")
        await db.database.logs.create_index([("pc_id", 1), ("timestamp", -1)])
        await db.database.logs.create_index([("script_name", 1), ("timestamp", -1)])
        
        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.warning(f"Error creating indexes: {e}")


def get_database():
    """Get database instance"""
    return db.database

