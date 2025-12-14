from datetime import datetime
from app.data.db import connect_database
from app.data.incidents import (
    get_all_incidents,
    create_incident,
    update_incident_status,
    delete_incident
)


def list_incidents(db_path=None):
    """List all incidents."""
    conn = connect_database(db_path)
    incidents = get_all_incidents(conn)
    conn.close()
    return incidents


def add_incident(title, severity, status="open", db_path=None):
    """Create new incident with automatic timestamp."""
    conn = connect_database(db_path)
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_id = create_incident(conn, title, severity, status, date)
    conn.close()
    return True, f"Incident '{title}' created with ID {new_id}."


def change_incident_status(incident_id, new_status, db_path=None):
    """Update incident status."""
    conn = connect_database(db_path)
    update_incident_status(conn, incident_id, new_status)
    conn.close()
    return True, f"Incident {incident_id} updated."


def remove_incident(incident_id, db_path=None):
    """Delete an incident."""
    conn = connect_database(db_path)
    delete_incident(conn, incident_id)
    conn.close()
    return True, f"Incident {incident_id} deleted."