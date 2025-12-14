from datetime import datetime
from app.data.db import connect_database
from app.data.tickets import (
    get_all_tickets,
    create_ticket,
    update_ticket_status,
    delete_ticket
)


def list_tickets(db_path=None):
    """List all tickets."""
    conn = connect_database(db_path)
    tickets = get_all_tickets(conn)
    conn.close()
    return tickets


def add_ticket(title, priority="medium", db_path=None):
    """Create new ticket with automatic timestamp."""
    conn = connect_database(db_path)
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_id = create_ticket(conn, title, priority, "open", created_date)
    conn.close()
    return True, f"Ticket '{title}' created with ID {new_id}."


def change_ticket_status(ticket_id, new_status, db_path=None):
    """Update ticket status."""
    conn = connect_database(db_path)
    update_ticket_status(conn, ticket_id, new_status)
    conn.close()
    return True, f"Ticket {ticket_id} updated."


def remove_ticket(ticket_id, db_path=None):
    """Delete a ticket."""
    conn = connect_database(db_path)
    delete_ticket(conn, ticket_id)
    conn.close()
    return True, f"Ticket {ticket_id} deleted."