# app/services/__init__.py

from app.services.ai_service import AIService, get_ai_service
from app.services.incident_service import (
    list_incidents,
    add_incident,
    change_incident_status,
    remove_incident
)
from app.services.dataset_service import (
    list_datasets,
    add_dataset,
    resize_dataset,
    remove_dataset
)
from app.services.ticket_service import (
    list_tickets,
    add_ticket,
    change_ticket_status,
    remove_ticket
)
# User service imports - commented out if functions don't exist
# from app.services.user_service import (
#     register_user,
#     authenticate_user,
#     get_user_by_username
# )

__all__ = [
    "AIService",
    "get_ai_service",
    "list_incidents",
    "add_incident",
    "change_incident_status",
    "remove_incident",
    "list_datasets",
    "add_dataset",
    "resize_dataset",
    "remove_dataset",
    "list_tickets",
    "add_ticket",
    "change_ticket_status",
    "remove_ticket",
    # "register_user",
    # "login_user"
]

