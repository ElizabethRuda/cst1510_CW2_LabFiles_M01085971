# app/data/incidents.py

from pathlib import Path
import csv
from app.data.db import DATA_DIR


# ---------- CSV LOADING ----------

def load_incidents_from_csv(conn, csv_path: Path | None = None):
    """
    Load incidents from cyber_incidents.csv into cyber_incidents table.
    Expected CSV columns: id, title, severity, status, date
    """
    if csv_path is None:
        csv_path = DATA_DIR / "cyber_incidents.csv"

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM cyber_incidents")
    count = cursor.fetchone()[0]
    if count > 0:
        return

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get("title")
            severity = row.get("severity")
            status = row.get("status")
            date = row.get("date")

            cursor.execute(
                """
                INSERT INTO cyber_incidents (title, severity, status, date)
                VALUES (?, ?, ?, ?)
                """,
                (title, severity, status, date),
            )

    conn.commit()
    print("✅ Loaded incidents from cyber_incidents.csv")


# ---------- CRUD FUNCTIONS ----------

def get_all_incidents(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, title, severity, status, date
        FROM cyber_incidents
        ORDER BY id
        """
    )
    return cursor.fetchall()


def create_incident(conn, title: str, severity: str,
                    status: str = "open", date: str | None = None):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO cyber_incidents (title, severity, status, date)
        VALUES (?, ?, ?, ?)
        """,
        (title, severity, status, date),
    )
    conn.commit()
    return cursor.lastrowid


def update_incident_status(conn, incident_id: int, new_status: str):
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE cyber_incidents
        SET status = ?
        WHERE id = ?
        """,
        (new_status, incident_id),
    )
    conn.commit()


def delete_incident(conn, incident_id: int):
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE id = ?",
        (incident_id,),
    )
    conn.commit()
