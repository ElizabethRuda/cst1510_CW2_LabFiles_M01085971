"""
Security Incident Model Class
Week 11: OOP Refactoring
"""

from typing import Optional
from datetime import datetime


class SecurityIncident:
    """
    Represents a cybersecurity incident.
    
    Attributes:
        id: Incident ID (from database)
        title: Incident title/description
        severity: Severity level (Critical, High, Medium, Low)
        status: Current status (open, in_progress, resolved, closed)
        date: Incident date
        reported_by: Username of reporter
    """
    
    SEVERITY_LEVELS = ["Critical", "High", "Medium", "Low"]
    STATUS_OPTIONS = ["open", "in_progress", "resolved", "closed"]
    
    def __init__(
        self,
        title: str,
        severity: str,
        status: str = "open",
        date: Optional[str] = None,
        reported_by: Optional[str] = None,
        incident_id: Optional[int] = None
    ):
        """
        Initialize a SecurityIncident object.
        
        Args:
            title: Incident title/description
            severity: Severity level
            status: Current status (default: "open")
            date: Incident date (YYYY-MM-DD format)
            reported_by: Username of reporter
            incident_id: Optional database ID
        """
        self.id = incident_id
        self.title = title
        self.severity = severity if severity in self.SEVERITY_LEVELS else "Medium"
        self.status = status if status in self.STATUS_OPTIONS else "open"
        self.date = date or datetime.now().strftime('%Y-%m-%d')
        self.reported_by = reported_by
    
    def is_critical(self) -> bool:
        """Check if incident is critical severity."""
        return self.severity == "Critical"
    
    def is_high_priority(self) -> bool:
        """Check if incident is high or critical severity."""
        return self.severity in ["Critical", "High"]
    
    def is_open(self) -> bool:
        """Check if incident is still open."""
        return self.status in ["open", "in_progress"]
    
    def is_resolved(self) -> bool:
        """Check if incident is resolved."""
        return self.status in ["resolved", "closed"]
    
    def update_status(self, new_status: str) -> bool:
        """
        Update incident status.
        
        Args:
            new_status: New status value
            
        Returns:
            True if status was updated, False if invalid
        """
        if new_status in self.STATUS_OPTIONS:
            self.status = new_status
            return True
        return False
    
    def escalate(self) -> bool:
        """
        Escalate incident to next severity level.
        
        Returns:
            True if escalated, False if already at maximum
        """
        current_index = self.SEVERITY_LEVELS.index(self.severity)
        if current_index > 0:
            self.severity = self.SEVERITY_LEVELS[current_index - 1]
            return True
        return False
    
    def resolve(self) -> None:
        """Mark incident as resolved."""
        self.status = "resolved"
    
    def close(self) -> None:
        """Close the incident."""
        self.status = "closed"
    
    def __str__(self) -> str:
        """String representation of SecurityIncident."""
        return f"SecurityIncident(id={self.id}, title='{self.title}', severity='{self.severity}', status='{self.status}')"
    
    def __repr__(self) -> str:
        """Representation of SecurityIncident."""
        return self.__str__()
    
    def to_dict(self) -> dict:
        """
        Convert SecurityIncident to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'title': self.title,
            'severity': self.severity,
            'status': self.status,
            'date': self.date,
            'reported_by': self.reported_by
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SecurityIncident':
        """
        Create SecurityIncident from dictionary.
        
        Args:
            data: Dictionary with incident data
            
        Returns:
            SecurityIncident object
        """
        return cls(
            title=data.get('title', ''),
            severity=data.get('severity', 'Medium'),
            status=data.get('status', 'open'),
            date=data.get('date'),
            reported_by=data.get('reported_by'),
            incident_id=data.get('id')
        )

