"""
Example: Using OOP Classes in Intelligence Platform
Week 11: OOP Refactoring Demonstration
"""

from app.models.user import User
from app.models.incident import SecurityIncident
from app.models.dataset import Dataset
from app.models.ticket import ITTicket
from app.repositories.incident_repository import IncidentRepository


def example_user_operations():
    """Example of User class usage."""
    print("=== User Operations ===")
    
    # Create user with hashed password
    password = "SecurePass123!"
    password_hash = User.hash_password(password)
    user = User("alice", password_hash, "analyst")
    
    print(f"Created: {user}")
    print(f"Is admin: {user.is_admin()}")
    print(f"Is analyst: {user.is_analyst()}")
    print(f"Password verified: {user.verify_password(password)}")
    print(f"Password verified (wrong): {user.verify_password('wrong')}")
    print()


def example_incident_operations():
    """Example of SecurityIncident class usage."""
    print("=== Security Incident Operations ===")
    
    # Create incident
    incident = SecurityIncident(
        title="Phishing Attack Detected",
        severity="High",
        status="open",
        date="2024-12-13",
        reported_by="alice"
    )
    
    print(f"Created: {incident}")
    print(f"Is critical: {incident.is_critical()}")
    print(f"Is high priority: {incident.is_high_priority()}")
    print(f"Is open: {incident.is_open()}")
    
    # Update status
    incident.update_status("in_progress")
    print(f"After update: {incident.status}")
    
    # Escalate
    incident.escalate()
    print(f"After escalation: {incident.severity}")
    
    # Resolve
    incident.resolve()
    print(f"After resolution: {incident.status}")
    print()


def example_dataset_operations():
    """Example of Dataset class usage."""
    print("=== Dataset Operations ===")
    
    # Create dataset
    dataset = Dataset(
        name="Security Logs 2024",
        source="Network Sensors",
        category="Security",
        size=500  # MB
    )
    
    print(f"Created: {dataset}")
    print(f"Size: {dataset.get_formatted_size()}")
    print(f"Size in GB: {dataset.get_size_gb():.2f} GB")
    print(f"Is large (>100MB): {dataset.is_large(100)}")
    
    # Update size
    dataset.update_size(1500)
    print(f"After update: {dataset.get_formatted_size()}")
    print()


def example_ticket_operations():
    """Example of ITTicket class usage."""
    print("=== IT Ticket Operations ===")
    
    # Create ticket
    ticket = ITTicket(
        ticket_id="TICKET-1001",
        title="Network connectivity issue",
        priority="Medium",
        status="open",
        category="Network",
        assigned_to=None
    )
    
    print(f"Created: {ticket}")
    print(f"Is critical: {ticket.is_critical()}")
    print(f"Is open: {ticket.is_open()}")
    
    # Assign and update status
    ticket.assign("bob")
    print(f"After assignment: {ticket.assigned_to}, status: {ticket.status}")
    
    # Resolve
    ticket.resolve()
    print(f"After resolution: {ticket.status}, resolved_date: {ticket.resolved_date}")
    print(f"Resolution time: {ticket.get_resolution_time_days()} days")
    print()


def example_repository_usage():
    """Example of Repository pattern usage."""
    print("=== Repository Pattern ===")
    
    # Create repository
    repo = IncidentRepository()
    
    # Get all incidents as objects
    incidents = repo.get_all()
    print(f"Total incidents: {len(incidents)}")
    
    # Filter using OOP methods
    critical = [inc for inc in incidents if inc.is_critical()]
    open_incidents = [inc for inc in incidents if inc.is_open()]
    
    print(f"Critical incidents: {len(critical)}")
    print(f"Open incidents: {len(open_incidents)}")
    
    # Work with individual incident
    if incidents:
        incident = incidents[0]
        print(f"First incident: {incident}")
        print(f"Can escalate: {incident.escalate()}")
        print(f"After escalation: {incident.severity}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("OOP Classes Usage Examples")
    print("=" * 60)
    print()
    
    example_user_operations()
    example_incident_operations()
    example_dataset_operations()
    example_ticket_operations()
    example_repository_usage()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)

