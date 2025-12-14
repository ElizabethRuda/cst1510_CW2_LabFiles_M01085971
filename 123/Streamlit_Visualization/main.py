# main.py

from app.data.db import connect_database
from app.data.schema import (
    create_users_table,
    create_cyber_incidents_table,
    create_datasets_metadata_table,
    create_it_tickets_table,
)
from app.data.users import migrate_users_from_file
from app.data.datasets import (
    get_all_datasets,
    create_dataset,
    update_dataset_size,
    delete_dataset,
    load_datasets_from_csv,
)
from app.data.incidents import (
    get_all_incidents,
    create_incident,
    update_incident_status,
    delete_incident,
    load_incidents_from_csv,
)
from app.data.tickets import (
    get_all_tickets,
    create_ticket,
    update_ticket_status,
    delete_ticket,
    load_tickets_from_csv,
)
from app.services.user_service import register_user, login_user


# ---------- HELPER FUNCTIONS ----------

def pause():
    input("\nPress Enter to continue...")


def print_header(title: str):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ---------- INITIAL DATABASE SETUP ----------

def init_database():
    print("Creating tables...")
    conn = connect_database()

    # Create tables
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    print("All tables created successfully!")

    # Migrate users from users.txt
    migrate_users_from_file(conn)

    # Load CSV data (only if tables are empty)
    load_datasets_from_csv(conn)
    load_incidents_from_csv(conn)
    load_tickets_from_csv(conn)

    conn.close()


# ---------- MENUS ----------

def menu_users():
    while True:
        print_header("USER AUTHENTICATION")
        print("[1] Register")
        print("[2] Login")
        print("[3] Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            ok, msg = register_user(username, password)
            print(msg)
            pause()

        elif choice == "2":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            ok, msg = login_user(username, password)
            print(msg)
            pause()

        elif choice == "3":
            break
        else:
            print("Invalid option.")
            pause()


def menu_incidents():
    conn = connect_database()
    try:
        while True:
            print_header("CYBER INCIDENTS")
            print("[1] List incidents")
            print("[2] Add incident")
            print("[3] Update status")
            print("[4] Delete incident")
            print("[5] Back")

            choice = input("Choose: ").strip()

            if choice == "1":
                rows = get_all_incidents(conn)
                print("\nID | Title | Severity | Status | Date")
                print("-" * 60)
                for row in rows:
                    iid, title, sev, status, date = row
                    print(f"{iid} | {title} | {sev} | {status} | {date}")
                pause()

            elif choice == "2":
                title = input("Title: ").strip()
                severity = input("Severity (Low/Medium/High/Critical): ").strip()
                status = "open"
                date = input("Date (YYYY-MM-DD): ").strip()
                create_incident(conn, title, severity, status, date)
                print("Incident added.")
                pause()

            elif choice == "3":
                iid = int(input("Incident ID: "))
                new_status = input("New status: ").strip()
                update_incident_status(conn, iid, new_status)
                print("Status updated.")
                pause()

            elif choice == "4":
                iid = int(input("Incident ID: "))
                delete_incident(conn, iid)
                print("Incident deleted.")
                pause()

            elif choice == "5":
                break
            else:
                print("Invalid option.")
                pause()
    finally:
        conn.close()


def menu_datasets():
    conn = connect_database()
    try:
        while True:
            print_header("DATASETS")
            print("[1] List datasets")
            print("[2] Add dataset")
            print("[3] Update size")
            print("[4] Delete dataset")
            print("[5] Back")

            choice = input("Choose: ").strip()

            if choice == "1":
                rows = get_all_datasets(conn)
                print("\nID | Name | Source | Category | Size")
                print("-" * 60)
                for row in rows:
                    did, name, source, category, size = row
                    print(f"{did} | {name} | {source} | {category} | {size}")
                pause()

            elif choice == "2":
                name = input("Name: ").strip()
                source = input("Source (optional): ").strip() or None
                category = input("Category (optional): ").strip() or None
                size_str = input("Size (optional integer): ").strip()
                size = int(size_str) if size_str else None
                create_dataset(conn, name, source, category, size)
                print("Dataset created.")
                pause()

            elif choice == "3":
                did = int(input("Dataset ID: "))
                size = int(input("New size: "))
                update_dataset_size(conn, did, size)
                print("Size updated.")
                pause()

            elif choice == "4":
                did = int(input("Dataset ID: "))
                delete_dataset(conn, did)
                print("Dataset deleted.")
                pause()

            elif choice == "5":
                break
            else:
                print("Invalid option.")
                pause()
    finally:
        conn.close()


def menu_tickets():
    conn = connect_database()
    try:
        while True:
            print_header("IT TICKETS")
            print("[1] List tickets")
            print("[2] Add ticket")
            print("[3] Update status")
            print("[4] Delete ticket")
            print("[5] Back")

            choice = input("Choose: ").strip()

            if choice == "1":
                rows = get_all_tickets(conn)
                print("\nID | Title | Priority | Status | Created")
                print("-" * 60)
                for row in rows:
                    tid, title, prio, status, created = row
                    print(f"{tid} | {title} | {prio} | {status} | {created}")
                pause()

            elif choice == "2":
                title = input("Title: ").strip()
                priority = input("Priority (low/medium/high/critical): ").strip()
                status = "open"
                created_date = input("Created date (YYYY-MM-DD): ").strip()
                create_ticket(conn, title, priority, status, created_date)
                print("Ticket created.")
                pause()

            elif choice == "3":
                tid = int(input("Ticket ID: "))
                new_status = input("New status: ").strip()
                update_ticket_status(conn, tid, new_status)
                print("Status updated.")
                pause()

            elif choice == "4":
                tid = int(input("Ticket ID: "))
                delete_ticket(conn, tid)
                print("Ticket deleted.")
                pause()

            elif choice == "5":
                break
            else:
                print("Invalid option.")
                pause()
    finally:
        conn.close()


# ---------- MAIN LOOP ----------

def main():
    init_database()

    while True:
        print_header("MULTI-DOMAIN INTELLIGENCE PLATFORM")
        print("[1] Users")
        print("[2] Cyber Incidents")
        print("[3] Datasets")
        print("[4] Tickets")
        print("[5] Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            menu_users()
        elif choice == "2":
            menu_incidents()
        elif choice == "3":
            menu_datasets()
        elif choice == "4":
            menu_tickets()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
            pause()


if __name__ == "__main__":
    main()
