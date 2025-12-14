from datetime import datetime
from app.data.tickets import (
    get_all_tickets,
    get_ticket_by_id,
    create_ticket,
    update_ticket_status,
    delete_ticket
)


def list_tickets():
    return get_all_tickets()


def add_ticket(title, priority="medium"):
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_id = create_ticket(title, priority, "open", created_date)
    return True, f"Ticket '{title}' created with ID {new_id}."


def change_ticket_status(ticket_id, new_status):
    update_ticket_status(ticket_id, new_status)
    return True, f"Ticket {ticket_id} updated."


def remove_ticket(ticket_id):
    delete_ticket(ticket_id)
    return True, f"Ticket {ticket_id} deleted."