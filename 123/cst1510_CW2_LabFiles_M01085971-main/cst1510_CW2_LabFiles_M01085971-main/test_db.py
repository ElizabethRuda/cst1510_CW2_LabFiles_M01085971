import sqlite3
from pathlib import Path

DB_PATH = (Path(__file__).resolve().parent / "DATA" / "intelligence_platform.db")

print(f"DEBUG: Using database: {DB_PATH}")

conn = sqlite3.connect(str(DB_PATH))
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("\nTables in your database:")
if not tables:
    print(" - (none)")
else:
    for t in tables:
        print(" -", t[0])

conn.close()

from app.data.db import connect_database
from app.data.datasets import get_all_datasets, create_dataset
from app.data.incidents import get_all_incidents, create_incident
from app.data.tickets import get_all_tickets, create_ticket

conn = connect_database()

print("\n=== TEST: DATASETS ===")
print("All datasets:", get_all_datasets())
new_did = create_dataset("Test Dataset", "system", "test", 123, "2024-12-01")
print("Created dataset with id:", new_did)

print("\n=== TEST: INCIDENTS ===")
print("All incidents:", get_all_incidents())
new_iid = create_incident("Test Incident", "High", "open", "2024-12-01")
print("Created incident id:", new_iid)

print("\n=== TEST: TICKETS ===")
print("All tickets:", get_all_tickets())
new_tid = create_ticket("Test Ticket", "medium", "open", "2024-12-01")
print("Created ticket id:", new_tid)