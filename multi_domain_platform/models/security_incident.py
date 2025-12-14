"""
Security Incident model for cybersecurity domain
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class SecurityIncident:
    """Security incident model"""
    id: Optional[int] = None
    title: str = ""
    severity: str = "Low"
    status: str = "open"
    date: Optional[str] = None
    
    def __post_init__(self):
        """Validate security incident data"""
        valid_severities = ['Critical', 'High', 'Medium', 'Low']
        if self.severity not in valid_severities:
            self.severity = 'Low'
        
        valid_statuses = ['open', 'in_progress', 'resolved']
        if self.status not in valid_statuses:
            self.status = 'open'

