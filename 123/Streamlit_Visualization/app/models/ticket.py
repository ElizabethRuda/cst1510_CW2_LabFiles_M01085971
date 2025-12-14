"""
IT Ticket Model Class
Week 11: OOP Refactoring
"""

from typing import Optional
from datetime import datetime, timedelta


class ITTicket:
    """
    Represents an IT support ticket.
    
    Attributes:
        id: Ticket ID (from database)
        ticket_id: Unique ticket identifier
        title: Ticket subject/title
        priority: Priority level (Critical, High, Medium, Low)
        status: Current status (open, in_progress, resolved, closed)
        category: Ticket category
        created_date: Ticket creation date
        resolved_date: Resolution date (if resolved)
        assigned_to: Assigned staff member
    """
    
    PRIORITY_LEVELS = ["Critical", "High", "Medium", "Low"]
    STATUS_OPTIONS = ["open", "in_progress", "resolved", "closed"]
    
    def __init__(
        self,
        ticket_id: str,
        title: str,
        priority: str = "Medium",
        status: str = "open",
        category: Optional[str] = None,
        created_date: Optional[str] = None,
        resolved_date: Optional[str] = None,
        assigned_to: Optional[str] = None,
        ticket_db_id: Optional[int] = None
    ):
        """
        Initialize an ITTicket object.
        
        Args:
            ticket_id: Unique ticket identifier
            title: Ticket subject/title
            priority: Priority level (default: "Medium")
            status: Current status (default: "open")
            category: Ticket category
            created_date: Creation date (YYYY-MM-DD)
            resolved_date: Resolution date (YYYY-MM-DD)
            assigned_to: Assigned staff member
            ticket_db_id: Optional database ID
        """
        self.id = ticket_db_id
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority if priority in self.PRIORITY_LEVELS else "Medium"
        self.status = status if status in self.STATUS_OPTIONS else "open"
        self.category = category
        self.created_date = created_date or datetime.now().strftime('%Y-%m-%d')
        self.resolved_date = resolved_date
        self.assigned_to = assigned_to
    
    def is_critical(self) -> bool:
        """Check if ticket is critical priority."""
        return self.priority == "Critical"
    
    def is_high_priority(self) -> bool:
        """Check if ticket is high or critical priority."""
        return self.priority in ["Critical", "High"]
    
    def is_open(self) -> bool:
        """Check if ticket is still open."""
        return self.status in ["open", "in_progress"]
    
    def is_resolved(self) -> bool:
        """Check if ticket is resolved."""
        return self.status in ["resolved", "closed"]
    
    def update_status(self, new_status: str) -> bool:
        """
        Update ticket status.
        
        Args:
            new_status: New status value
            
        Returns:
            True if status was updated, False if invalid
        """
        if new_status in self.STATUS_OPTIONS:
            self.status = new_status
            if new_status in ["resolved", "closed"] and not self.resolved_date:
                self.resolved_date = datetime.now().strftime('%Y-%m-%d')
            return True
        return False
    
    def assign(self, staff_member: str) -> None:
        """
        Assign ticket to staff member.
        
        Args:
            staff_member: Staff member username
        """
        self.assigned_to = staff_member
        if self.status == "open":
            self.status = "in_progress"
    
    def resolve(self) -> None:
        """Mark ticket as resolved."""
        self.status = "resolved"
        self.resolved_date = datetime.now().strftime('%Y-%m-%d')
    
    def close(self) -> None:
        """Close the ticket."""
        self.status = "closed"
        if not self.resolved_date:
            self.resolved_date = datetime.now().strftime('%Y-%m-%d')
    
    def get_resolution_time_days(self) -> Optional[int]:
        """
        Get resolution time in days.
        
        Returns:
            Number of days to resolve, or None if not resolved
        """
        if not self.resolved_date:
            return None
        
        try:
            created = datetime.strptime(self.created_date, '%Y-%m-%d')
            resolved = datetime.strptime(self.resolved_date, '%Y-%m-%d')
            return (resolved - created).days
        except ValueError:
            return None
    
    def escalate_priority(self) -> bool:
        """
        Escalate ticket to next priority level.
        
        Returns:
            True if escalated, False if already at maximum
        """
        current_index = self.PRIORITY_LEVELS.index(self.priority)
        if current_index > 0:
            self.priority = self.PRIORITY_LEVELS[current_index - 1]
            return True
        return False
    
    def __str__(self) -> str:
        """String representation of ITTicket."""
        return f"ITTicket(id={self.id}, ticket_id='{self.ticket_id}', title='{self.title}', priority='{self.priority}', status='{self.status}')"
    
    def __repr__(self) -> str:
        """Representation of ITTicket."""
        return self.__str__()
    
    def to_dict(self) -> dict:
        """
        Convert ITTicket to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'title': self.title,
            'priority': self.priority,
            'status': self.status,
            'category': self.category,
            'created_date': self.created_date,
            'resolved_date': self.resolved_date,
            'assigned_to': self.assigned_to
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ITTicket':
        """
        Create ITTicket from dictionary.
        
        Args:
            data: Dictionary with ticket data
            
        Returns:
            ITTicket object
        """
        return cls(
            ticket_id=data.get('ticket_id', ''),
            title=data.get('title', ''),
            priority=data.get('priority', 'Medium'),
            status=data.get('status', 'open'),
            category=data.get('category'),
            created_date=data.get('created_date'),
            resolved_date=data.get('resolved_date'),
            assigned_to=data.get('assigned_to'),
            ticket_db_id=data.get('id')
        )

