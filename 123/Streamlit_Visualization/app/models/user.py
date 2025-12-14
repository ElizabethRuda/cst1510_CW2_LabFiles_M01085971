"""
User Model Class
Week 11: OOP Refactoring
"""

import bcrypt
from typing import Optional


class User:
    """
    Represents a user in the Intelligence Platform.
    
    Attributes:
        id: User ID (from database)
        username: Unique username
        password_hash: Hashed password (bcrypt)
        role: User role (user, analyst, admin)
    """
    
    def __init__(self, username: str, password_hash: str, role: str = "user", user_id: Optional[int] = None):
        """
        Initialize a User object.
        
        Args:
            username: User's login name
            password_hash: Hashed password
            role: User role (default: "user")
            user_id: Optional database ID
        """
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password as string
        """
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str) -> bool:
        """
        Verify a password against the stored hash.
        
        Args:
            password: Plain text password to verify
            
        Returns:
            True if password matches, False otherwise
        """
        password_bytes = password.encode('utf-8')
        hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role.lower() == "admin"
    
    def is_analyst(self) -> bool:
        """Check if user has analyst role."""
        return self.role.lower() in ["analyst", "admin"]
    
    def __str__(self) -> str:
        """String representation of User."""
        return f"User(id={self.id}, username='{self.username}', role='{self.role}')"
    
    def __repr__(self) -> str:
        """Representation of User."""
        return self.__str__()
    
    def to_dict(self) -> dict:
        """
        Convert User to dictionary.
        
        Returns:
            Dictionary representation of User
        """
        return {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash,
            'role': self.role
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """
        Create User from dictionary.
        
        Args:
            data: Dictionary with user data
            
        Returns:
            User object
        """
        return cls(
            username=data.get('username', ''),
            password_hash=data.get('password_hash', ''),
            role=data.get('role', 'user'),
            user_id=data.get('id')
        )

