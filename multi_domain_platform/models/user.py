"""
User model for authentication and authorization
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """User model representing a platform user"""
    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    role: str = "user"
    
    def __post_init__(self):
        """Validate user data"""
        if self.role not in ['user', 'admin', 'analyst']:
            self.role = 'user'

