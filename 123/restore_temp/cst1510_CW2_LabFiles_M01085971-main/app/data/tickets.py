# app/data/tickets.py

from pathlib import Path
import csv
from app.data.db import DATA_DIR


# ---------- CSV LOADING ----------

def load_tickets_from_csv(conn, csv_path: Path | None = None):
    """
    Load tickets from it_tickets.csv into it_tickets table.
    Expected CSV columns: id, title, priority, status, created_date
    """
    if csv_path is None:
        csv_path = DATA_DIR / "it_tickets.csv"

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM it_tickets")
    count = cursor.fetchone()[0]
    if count > 0:
        return

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get("title")
            priority = row.get("priority")
            status = row.get("status")
            created_date = row.get("created_date")

            cursor.execute(
                """
                INSERT INTO it_tickets (title, priority, status, created_date)
                VALUES (?, ?, ?, ?)
                """,
                (title, priority, status, created_date),
            )

    conn.commit()
    print("✅ Loaded tickets from it_tickets.csv")


# ---------- CRUD FUNCTIONS ----------

def get_all_tickets(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, title, priority, status, created_date
        FROM it_tickets
        ORDER BY id
        """
    )
    return cursor.fetchall()


def create_ticket(conn, title: str, priority: str = "medium",
                  status: str = "open", created_date: str | None = None):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO it_tickets (title, priority, status, created_date)
        VALUES (?, ?, ?, ?)
        """,
        (title, priority, status, created_date),
    )
    conn.commit()
    return cursor.lastrowid


def update_ticket_status(conn, ticket_id: int, new_status: str):
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE it_tickets
        SET status = ?
        WHERE id = ?
        """,
        (new_status, ticket_id),
    )
    conn.commit()


def delete_ticket(conn, ticket_id: int):
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM it_tickets WHERE id = ?",
        (ticket_id,),
    )
    conn.commit()
