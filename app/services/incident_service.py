from datetime import datetime
from app.data.incidents import (
    get_all_incidents,
    get_incident_by_id,
    create_incident,
    update_incident_status,
    delete_incident
)


def list_incidents():
    return get_all_incidents()


def add_incident(title, severity, status="open"):
    """Create new incident with automatic timestamp."""
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_id = create_incident(title, severity, status, date)
    return True, f"Incident '{title}' created with ID {new_id}."


def change_incident_status(incident_id, new_status):
    update_incident_status(incident_id, new_status)
    return True, f"Incident {incident_id} updated."


def remove_incident(incident_id):
    delete_incident(incident_id)
    return True, f"Incident {incident_id} deleted."