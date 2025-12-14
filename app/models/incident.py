# app/models/incident.py

from typing import Optional
from datetime import datetime


class SecurityIncident:
    """Model for security incidents."""
    
    def __init__(self, title: str, severity: str, status: str = "open", 
                 date: Optional[str] = None, incident_id: Optional[int] = None):
        self.id = incident_id
        self.title = title
        self.severity = severity
        self.status = status
        self.date = date or datetime.now().strftime("%Y-%m-%d")
    
    def is_critical(self) -> bool:
        """Check if incident is critical."""
        return self.severity.lower() == "critical"
    
    def is_resolved(self) -> bool:
        """Check if incident is resolved."""
        return self.status.lower() == "resolved"
    
    def to_dict(self) -> dict:
        """Convert incident to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "severity": self.severity,
            "status": self.status,
            "date": self.date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SecurityIncident':
        """Create incident from dictionary."""
        return cls(
            incident_id=data.get("id"),
            title=data["title"],
            severity=data["severity"],
            status=data.get("status", "open"),
            date=data.get("date")
        )
    
    def __repr__(self) -> str:
        return f"SecurityIncident(id={self.id}, title='{self.title}', severity='{self.severity}')"


