"""
Database initialization and utilities
"""
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from multi_domain_platform.services.database_manager import DatabaseManager


def get_db_manager() -> DatabaseManager:
    """Get database manager instance"""
    db_path = Path(__file__).parent / "platform.db"
    return DatabaseManager(db_path=str(db_path))


def init_database():
    """Initialize database schema"""
    db_manager = get_db_manager()
    # Database is initialized in DatabaseManager.__init__
    return db_manager

