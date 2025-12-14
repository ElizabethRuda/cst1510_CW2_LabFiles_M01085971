"""
Incident Repository - OOP wrapper for database operations
Week 11: OOP Refactoring
"""

from typing import List, Optional
from app.models.incident import SecurityIncident
from app.data.db import connect_database
from app.data.incidents import (
    get_all_incidents as db_get_all_incidents,
    create_incident as db_create_incident,
    update_incident_status as db_update_incident_status,
    delete_incident as db_delete_incident
)


class IncidentRepository:
    """Repository for SecurityIncident operations."""
    
    def __init__(self, db_path=None):
        """Initialize repository with database path."""
        self.db_path = db_path
    
    def get_all(self) -> List[SecurityIncident]:
        """
        Get all incidents as SecurityIncident objects.
        
        Returns:
            List of SecurityIncident objects
        """
        conn = connect_database(self.db_path)
        incidents_data = db_get_all_incidents(conn)
        conn.close()
        
        incidents = []
        for row in incidents_data:
            incident = SecurityIncident(
                title=row[1],
                severity=row[2],
                status=row[3],
                date=row[4] if len(row) > 4 else None,
                incident_id=row[0]
            )
            incidents.append(incident)
        
        return incidents
    
    def get_by_id(self, incident_id: int) -> Optional[SecurityIncident]:
        """
        Get incident by ID.
        
        Args:
            incident_id: Incident ID
            
        Returns:
            SecurityIncident object or None
        """
        incidents = self.get_all()
        for incident in incidents:
            if incident.id == incident_id:
                return incident
        return None
    
    def create(self, incident: SecurityIncident) -> int:
        """
        Create new incident in database.
        
        Args:
            incident: SecurityIncident object
            
        Returns:
            ID of created incident
        """
        conn = connect_database(self.db_path)
        incident_id = db_create_incident(
            conn,
            incident.title,
            incident.severity,
            incident.status,
            incident.date
        )
        conn.close()
        return incident_id
    
    def update(self, incident: SecurityIncident) -> bool:
        """
        Update incident in database.
        
        Args:
            incident: SecurityIncident object with updated data
            
        Returns:
            True if updated successfully
        """
        if not incident.id:
            return False
        
        conn = connect_database(self.db_path)
        db_update_incident_status(conn, incident.id, incident.status)
        conn.close()
        return True
    
    def delete(self, incident_id: int) -> bool:
        """
        Delete incident from database.
        
        Args:
            incident_id: Incident ID to delete
            
        Returns:
            True if deleted successfully
        """
        conn = connect_database(self.db_path)
        db_delete_incident(conn, incident_id)
        conn.close()
        return True
    
    def get_critical_incidents(self) -> List[SecurityIncident]:
        """
        Get all critical incidents.
        
        Returns:
            List of critical SecurityIncident objects
        """
        all_incidents = self.get_all()
        return [inc for inc in all_incidents if inc.is_critical()]
    
    def get_open_incidents(self) -> List[SecurityIncident]:
        """
        Get all open incidents.
        
        Returns:
            List of open SecurityIncident objects
        """
        all_incidents = self.get_all()
        return [inc for inc in all_incidents if inc.is_open()]

