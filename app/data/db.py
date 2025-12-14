import sqlite3
from pathlib import Path

# Data directory and database path
DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"

# Create DATA directory if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)


def connect_database(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    return conn

# Export paths so other modules can import them
__all__ = ["connect_database", "DATA_DIR", "DB_PATH"]