# app/repositories/incident_repository.py

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
    """Repository for SecurityIncident CRUD operations."""
    
    def __init__(self, db_path=None):
        self.db_path = db_path
    
    def get_all(self) -> List[SecurityIncident]:
        """Get all incidents."""
        conn = connect_database(self.db_path)
        incidents_data = db_get_all_incidents(conn)
        conn.close()
        
        incidents = []
        for row in incidents_data:
            incident = SecurityIncident(
                title=row[1],
                severity=row[2],
                status=row[3],
                date=row[4],
                incident_id=row[0]
            )
            incidents.append(incident)
        return incidents
    
    def create(self, title: str, severity: str, status: str = "open", date: Optional[str] = None) -> SecurityIncident:
        """Create a new incident."""
        conn = connect_database(self.db_path)
        incident_id = db_create_incident(conn, title, severity, status, date)
        conn.close()
        
        return SecurityIncident(
            title=title,
            severity=severity,
            status=status,
            date=date,
            incident_id=incident_id
        )
    
    def update_status(self, incident_id: int, new_status: str) -> bool:
        """Update incident status."""
        conn = connect_database(self.db_path)
        db_update_incident_status(conn, incident_id, new_status)
        conn.close()
        return True
    
    def delete(self, incident_id: int) -> bool:
        """Delete an incident."""
        conn = connect_database(self.db_path)
        db_delete_incident(conn, incident_id)
        conn.close()
        return True


