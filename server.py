"""
FastAPI WebSocket Server for Remote Script Execution

NOTE: This file is deprecated. Please use run.py instead.
This file now redirects to the modular app structure in app/main.py
"""
import sys
import os

# Redirect to the modular app
if __name__ == "__main__":
    print("=" * 60)
    print("  WARNING: server.py is deprecated!")
    print("  Please use 'python run.py' instead")
    print("=" * 60)
    print()
    
    # Import and run the modular app
    import uvicorn
    from app.config import settings
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
else:
    # If imported, use the modular app
    from app.main import app
