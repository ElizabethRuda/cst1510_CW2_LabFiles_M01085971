"""
Models package for Intelligence Platform
Week 11: OOP Refactoring
"""

from app.models.user import User
from app.models.incident import SecurityIncident
from app.models.dataset import Dataset
from app.models.ticket import ITTicket

__all__ = ['User', 'SecurityIncident', 'Dataset', 'ITTicket']

