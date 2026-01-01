"""
File Service - Handle file downloads from PCs
"""
import os
import uuid
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
from app.config import PROJECT_ROOT, settings
import logging

logger = logging.getLogger(__name__)

# Downloads directory
DOWNLOADS_DIR = PROJECT_ROOT / "downloads"
DOWNLOADS_DIR.mkdir(exist_ok=True)

# Max file size: 100 MB
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB in bytes


class FileService:
    """Service for managing downloaded files"""
    
    @staticmethod
    def get_downloads_dir() -> Path:
        """Get the downloads directory path"""
        return DOWNLOADS_DIR
    
    @staticmethod
    async def save_file(pc_id: str, file_path: str, file_content: bytes, file_name: Optional[str] = None) -> Dict:
        """
        Save a file downloaded from a PC
        
        Args:
            pc_id: ID of the PC that sent the file
            file_path: Original path of the file on the PC
            file_content: File content as bytes
            file_name: Optional custom file name (defaults to original filename)
        
        Returns:
            Dict with file info including saved_path, file_id, size, etc.
        """
        # Check file size
        file_size = len(file_content)
        if file_size > MAX_FILE_SIZE:
            raise ValueError(f"File size ({file_size} bytes) exceeds maximum allowed size ({MAX_FILE_SIZE} bytes)")
        
        # Create PC-specific directory
        pc_dir = DOWNLOADS_DIR / pc_id
        pc_dir.mkdir(exist_ok=True)
        
        # Generate file ID and determine filename
        file_id = str(uuid.uuid4())
        if not file_name:
            # Extract filename from path
            file_name = Path(file_path).name or f"file_{file_id}"
        
        # Sanitize filename
        safe_filename = "".join(c for c in file_name if c.isalnum() or c in "._- ")
        if not safe_filename:
            safe_filename = f"file_{file_id}"
        
        # Add timestamp to avoid conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{safe_filename}"
        
        # Full path to save file
        saved_path = pc_dir / safe_filename
        
        # Write file
        with open(saved_path, 'wb') as f:
            f.write(file_content)
        
        # Store metadata in JSON file
        import json
        metadata_file = saved_path.with_suffix(saved_path.suffix + '.meta.json')
        file_info = {
            "file_id": file_id,
            "pc_id": pc_id,
            "original_path": file_path,
            "saved_path": str(saved_path),
            "file_name": safe_filename,
            "size": file_size,
            "size_mb": round(file_size / (1024 * 1024), 2),
            "downloaded_at": datetime.utcnow().isoformat()
        }
        try:
            with open(metadata_file, 'w') as f:
                json.dump(file_info, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save file metadata: {e}")
        
        logger.info(f"File saved: {saved_path} ({file_size} bytes) from PC {pc_id}")
        return file_info
    
    @staticmethod
    def get_file(file_id: str, pc_id: str) -> Optional[Path]:
        """Get file path by file_id and pc_id"""
        pc_dir = DOWNLOADS_DIR / pc_id
        if not pc_dir.exists():
            return None
        
        # Search for file by checking metadata files
        import json
        for file_path in pc_dir.iterdir():
            if file_path.is_file() and file_path.suffix != '.meta.json':
                # Check metadata file
                metadata_file = file_path.with_suffix(file_path.suffix + '.meta.json')
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                            if metadata.get("file_id") == file_id:
                                return file_path
                    except Exception:
                        continue
                # Fallback: check if file_id is in filename
                elif file_id in file_path.name:
                    return file_path
        
        return None
    
    @staticmethod
    def list_files(pc_id: Optional[str] = None) -> List[Dict]:
        """
        List all downloaded files, optionally filtered by PC ID
        
        Args:
            pc_id: Optional PC ID to filter files
        
        Returns:
            List of file info dictionaries
        """
        files = []
        import json
        
        if pc_id:
            # List files for specific PC
            pc_dir = DOWNLOADS_DIR / pc_id
            if pc_dir.exists():
                for file_path in pc_dir.iterdir():
                    if file_path.is_file() and not file_path.name.endswith('.meta.json'):
                        stat = file_path.stat()
                        # Try to load metadata
                        metadata_file = file_path.with_suffix(file_path.suffix + '.meta.json')
                        file_info = {
                            "file_id": file_path.stem,  # Default to stem
                            "pc_id": pc_id,
                            "file_name": file_path.name,
                            "saved_path": str(file_path),
                            "original_path": file_path.name,  # Default to filename
                            "size": stat.st_size,
                            "size_mb": round(stat.st_size / (1024 * 1024), 2),
                            "downloaded_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
                        }
                        
                        if metadata_file.exists():
                            try:
                                with open(metadata_file, 'r') as f:
                                    metadata = json.load(f)
                                    file_info.update({
                                        "file_id": metadata.get("file_id", file_path.stem),
                                        "original_path": metadata.get("original_path", file_path.name)
                                    })
                            except Exception:
                                pass
                        
                        files.append(file_info)
        else:
            # List files from all PCs
            if DOWNLOADS_DIR.exists():
                for pc_dir in DOWNLOADS_DIR.iterdir():
                    if pc_dir.is_dir():
                        for file_path in pc_dir.iterdir():
                            if file_path.is_file() and not file_path.name.endswith('.meta.json'):
                                stat = file_path.stat()
                                # Try to load metadata
                                metadata_file = file_path.with_suffix(file_path.suffix + '.meta.json')
                                file_info = {
                                    "file_id": file_path.stem,
                                    "pc_id": pc_dir.name,
                                    "file_name": file_path.name,
                                    "saved_path": str(file_path),
                                    "original_path": file_path.name,
                                    "size": stat.st_size,
                                    "size_mb": round(stat.st_size / (1024 * 1024), 2),
                                    "downloaded_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
                                }
                                
                                if metadata_file.exists():
                                    try:
                                        with open(metadata_file, 'r') as f:
                                            metadata = json.load(f)
                                            file_info.update({
                                                "file_id": metadata.get("file_id", file_path.stem),
                                                "original_path": metadata.get("original_path", file_path.name)
                                            })
                                    except Exception:
                                        pass
                                
                                files.append(file_info)
        
        # Sort by downloaded_at (newest first)
        files.sort(key=lambda x: x.get("downloaded_at", ""), reverse=True)
        return files
    
    @staticmethod
    def delete_file(file_id: str, pc_id: str) -> bool:
        """Delete a downloaded file and its metadata"""
        file_path = FileService.get_file(file_id, pc_id)
        if file_path and file_path.exists():
            file_path.unlink()
            # Also delete metadata file if it exists
            metadata_file = file_path.with_suffix(file_path.suffix + '.meta.json')
            if metadata_file.exists():
                try:
                    metadata_file.unlink()
                except Exception as e:
                    logger.warning(f"Could not delete metadata file: {e}")
            logger.info(f"File deleted: {file_path}")
            return True
        return False
    
    @staticmethod
    def get_total_size() -> int:
        """Get total size of all downloaded files in bytes"""
        total = 0
        if DOWNLOADS_DIR.exists():
            for pc_dir in DOWNLOADS_DIR.iterdir():
                if pc_dir.is_dir():
                    for file_path in pc_dir.iterdir():
                        if file_path.is_file() and not file_path.name.endswith('.meta.json'):
                            total += file_path.stat().st_size
        return total

