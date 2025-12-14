# app/examples/oop_usage_example.py
"""
Example demonstrating OOP usage in the Intelligence Platform.
This shows how to use the model classes and repository pattern.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.models.user import User
from app.models.incident import SecurityIncident
from app.models.dataset import Dataset
from app.models.ticket import ITTicket
from app.repositories.incident_repository import IncidentRepository


def demonstrate_user_model():
    """Demonstrate User model usage."""
    print("\n=== User Model Example ===")
    
    # Create a user
    password = "SecurePass123!"
    hashed = User.hash_password(password)
    user = User("john_doe", hashed, "admin")
    
    print(f"Created user: {user}")
    print(f"Is admin: {user.is_admin()}")
    print(f"Password verification: {user.verify_password(password)}")
    print(f"User dict: {user.to_dict()}")


def demonstrate_incident_model():
    """Demonstrate SecurityIncident model usage."""
    print("\n=== SecurityIncident Model Example ===")
    
    incident = SecurityIncident(
        title="SQL Injection Attempt",
        severity="Critical",
        status="open"
    )
    
    print(f"Created incident: {incident}")
    print(f"Is critical: {incident.is_critical()}")
    print(f"Is resolved: {incident.is_resolved()}")
    print(f"Incident dict: {incident.to_dict()}")


def demonstrate_dataset_model():
    """Demonstrate Dataset model usage."""
    print("\n=== Dataset Model Example ===")
    
    # Size in bytes (150 GB)
    size_bytes = 150 * 1024 * 1024 * 1024
    dataset = Dataset(
        name="Customer Data",
        source="Internal",
        category="Analytics",
        size=size_bytes
    )
    
    print(f"Created dataset: {dataset}")
    print(f"Size in GB: {dataset.get_size_gb():.2f}")
    print(f"Size in MB: {dataset.get_size_mb():.2f}")
    print(f"Is large (>100MB): {dataset.is_large()}")
    print(f"Dataset dict: {dataset.to_dict()}")


def demonstrate_ticket_model():
    """Demonstrate ITTicket model usage."""
    print("\n=== ITTicket Model Example ===")
    
    ticket = ITTicket(
        title="Server Down",
        priority="high",
        status="open"
    )
    
    print(f"Created ticket: {ticket}")
    print(f"Is high priority: {ticket.is_high_priority()}")
    print(f"Is open: {ticket.is_open()}")
    print(f"Ticket dict: {ticket.to_dict()}")


def demonstrate_repository_pattern():
    """Demonstrate repository pattern usage."""
    print("\n=== Repository Pattern Example ===")
    
    # Initialize repository
    db_path = PROJECT_ROOT / "DATA" / "intelligence_platform.db"
    repo = IncidentRepository(db_path=db_path)
    
    # Get all incidents
    incidents = repo.get_all()
    print(f"Total incidents: {len(incidents)}")
    
    if incidents:
        print(f"First incident: {incidents[0]}")
        print(f"Is critical: {incidents[0].is_critical()}")


if __name__ == "__main__":
    print("OOP Usage Examples for Intelligence Platform")
    print("=" * 50)
    
    try:
        demonstrate_user_model()
        demonstrate_incident_model()
        demonstrate_dataset_model()
        demonstrate_ticket_model()
        demonstrate_repository_pattern()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

