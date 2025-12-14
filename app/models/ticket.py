# app/models/ticket.py

from typing import Optional
from datetime import datetime


class ITTicket:
    """Model for IT support tickets."""
    
    def __init__(self, title: str, priority: str = "medium", 
                 status: str = "open", created_date: Optional[str] = None, 
                 ticket_id: Optional[int] = None):
        self.id = ticket_id
        self.title = title
        self.priority = priority
        self.status = status
        self.created_date = created_date or datetime.now().strftime("%Y-%m-%d")
    
    def is_high_priority(self) -> bool:
        """Check if ticket is high priority."""
        return self.priority.lower() in ["high", "critical"]
    
    def is_open(self) -> bool:
        """Check if ticket is open."""
        return self.status.lower() == "open"
    
    def to_dict(self) -> dict:
        """Convert ticket to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "status": self.status,
            "created_date": self.created_date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ITTicket':
        """Create ticket from dictionary."""
        return cls(
            ticket_id=data.get("id"),
            title=data["title"],
            priority=data.get("priority", "medium"),
            status=data.get("status", "open"),
            created_date=data.get("created_date")
        )
    
    def __repr__(self) -> str:
        return f"ITTicket(id={self.id}, title='{self.title}', priority='{self.priority}')"


