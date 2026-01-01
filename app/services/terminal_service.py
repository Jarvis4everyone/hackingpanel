"""
Terminal Service - Manage PowerShell terminal sessions
"""
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class TerminalService:
    """Service for managing terminal sessions"""
    
    def __init__(self):
        # Store active terminal sessions
        # Format: {pc_id: session_id}
        self.active_sessions: Dict[str, str] = {}
        # Store session metadata
        # Format: {session_id: {"pc_id": str, "started_at": datetime, "status": str}}
        self.session_metadata: Dict[str, dict] = {}
    
    def create_session(self, pc_id: str, session_id: str) -> bool:
        """
        Create a new terminal session for a PC
        
        Args:
            pc_id: ID of the PC
            session_id: Unique session ID
        
        Returns:
            True if session created successfully
        """
        # Stop any existing session for this PC
        if pc_id in self.active_sessions:
            old_session_id = self.active_sessions[pc_id]
            self.end_session(old_session_id)
        
        self.active_sessions[pc_id] = session_id
        from datetime import datetime
        self.session_metadata[session_id] = {
            "pc_id": pc_id,
            "started_at": datetime.utcnow().isoformat(),
            "status": "active"
        }
        
        logger.info(f"Terminal session created: {session_id} for PC {pc_id}")
        return True
    
    def end_session(self, session_id: str) -> bool:
        """
        End a terminal session
        
        Args:
            session_id: Session ID to end
        
        Returns:
            True if session ended successfully
        """
        if session_id in self.session_metadata:
            pc_id = self.session_metadata[session_id].get("pc_id")
            if pc_id and pc_id in self.active_sessions:
                if self.active_sessions[pc_id] == session_id:
                    del self.active_sessions[pc_id]
            
            self.session_metadata[session_id]["status"] = "ended"
            logger.info(f"Terminal session ended: {session_id}")
            return True
        
        return False
    
    def get_session(self, pc_id: str) -> Optional[str]:
        """
        Get active session ID for a PC
        
        Args:
            pc_id: PC ID
        
        Returns:
            Session ID if active, None otherwise
        """
        return self.active_sessions.get(pc_id)
    
    def is_session_active(self, session_id: str) -> bool:
        """
        Check if a session is active
        
        Args:
            session_id: Session ID
        
        Returns:
            True if session is active
        """
        return session_id in self.session_metadata and \
               self.session_metadata[session_id].get("status") == "active"
    
    def get_session_info(self, session_id: str) -> Optional[dict]:
        """
        Get session information
        
        Args:
            session_id: Session ID
        
        Returns:
            Session metadata or None
        """
        return self.session_metadata.get(session_id)


# Global terminal service instance
terminal_service = TerminalService()

