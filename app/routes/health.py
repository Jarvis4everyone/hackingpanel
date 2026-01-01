"""
Health Check Routes
"""
from fastapi import APIRouter
from datetime import datetime
from app.websocket.connection_manager import manager
from app.services.pc_service import PCService

router = APIRouter(tags=["Health"])


@router.get("/api/health")
async def health_check():
    """Health check endpoint"""
    connected_count = manager.get_connected_count()
    return {
        "status": "healthy",
        "connected_pcs": connected_count,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/")
async def root():
    """Root endpoint"""
    connected_count = manager.get_connected_count()
    return {
        "message": "Remote Script Server",
        "version": "1.0.0",
        "connected_pcs": connected_count,
        "endpoints": {
            "websocket": "/ws/{pc_id}",
            "list_pcs": "/api/pcs",
            "send_script": "/api/scripts/send",
            "list_scripts": "/api/scripts",
            "executions": "/api/executions"
        }
    }

