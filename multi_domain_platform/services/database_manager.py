"""
Database Manager service for database operations
"""
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize database manager"""
        if db_path is None:
            project_root = Path(__file__).resolve().parents[2]
            # Check if old database exists in DATA/
            old_db = project_root / "DATA" / "intelligence_platform.db"
            new_db = project_root / "multi_domain_platform" / "database" / "platform.db"
            
            # Use old database if it exists, otherwise use new location
            if old_db.exists():
                db_path = old_db
            else:
                db_path = new_db
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            )
        """)
        
        # Create cyber_incidents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cyber_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                severity TEXT CHECK(severity IN ('Critical','High','Medium','Low')),
                status TEXT CHECK(status IN ('open','in_progress','resolved')),
                date TEXT
            )
        """)
        
        # Create datasets_metadata table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS datasets_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                source TEXT,
                category TEXT,
                size INTEGER DEFAULT 0
            )
        """)
        
        # Create it_tickets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS it_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT CHECK(priority IN ('critical','high','medium','low')),
                status TEXT CHECK(status IN ('open','in_progress','resolved','closed')),
                created_date TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        return sqlite3.connect(str(self.db_path))
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dicts"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected

