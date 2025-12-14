# app/models/user.py

import bcrypt
from typing import Optional


class User:
    """User model for authentication and role management."""
    
    def __init__(self, username: str, password_hash: str, role: str = "user", user_id: Optional[int] = None):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash."""
        password_bytes = password.encode('utf-8')
        hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role.lower() == "admin"
    
    def is_analyst(self) -> bool:
        """Check if user has analyst role."""
        return self.role.lower() == "analyst"
    
    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary."""
        return cls(
            user_id=data.get("id"),
            username=data["username"],
            password_hash=data.get("password_hash", ""),
            role=data.get("role", "user")
        )
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, username='{self.username}', role='{self.role}')"


