"""
Authentication Manager service for user authentication
"""
import bcrypt
from typing import Optional, Tuple
from ..models.user import User
from .database_manager import DatabaseManager


class AuthManager:
    """Manages user authentication and authorization"""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        """Initialize auth manager"""
        self.db_manager = db_manager or DatabaseManager()
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against a hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception:
            return False
    
    def register_user(self, username: str, password: str, role: str = "user") -> Tuple[bool, str]:
        """Register a new user"""
        try:
            # Check if user exists
            existing = self.db_manager.execute_query(
                "SELECT id FROM users WHERE username = ?",
                (username,)
            )
            if existing:
                return False, "Username already exists"
            
            # Hash password
            password_hash = self.hash_password(password)
            
            # Insert user
            self.db_manager.execute_update(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            return True, "User registered successfully"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[User]]:
        """Authenticate a user"""
        try:
            users = self.db_manager.execute_query(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )
            if not users:
                return False, None
            
            user_data = users[0]
            if self.verify_password(password, user_data['password_hash']):
                user = User(
                    id=user_data['id'],
                    username=user_data['username'],
                    password_hash=user_data['password_hash'],
                    role=user_data['role']
                )
                return True, user
            else:
                return False, None
        except Exception:
            return False, None

