"""
IT Ticket model for IT Operations domain
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ITTicket:
    """IT support ticket model"""
    id: Optional[int] = None
    title: str = ""
    priority: str = "low"
    status: str = "open"
    created_date: Optional[str] = None
    
    def __post_init__(self):
        """Validate IT ticket data"""
        valid_priorities = ['critical', 'high', 'medium', 'low']
        if self.priority not in valid_priorities:
            self.priority = 'low'
        
        valid_statuses = ['open', 'in_progress', 'resolved', 'closed']
        if self.status not in valid_statuses:
            self.status = 'open'

