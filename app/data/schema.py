from app.data.db import connect_database

# USERS TABLE
def create_users_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()


# CYBER INCIDENTS TABLE
def create_cyber_incidents_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            date TEXT
        )
    """)
    conn.commit()


# DATASETS METADATA TABLE
def create_datasets_metadata_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            source TEXT,
            category TEXT,
            size INTEGER
        )
    """)
    conn.commit()


# IT TICKETS TABLE
def create_it_tickets_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            created_date TEXT
        )
    """)
    conn.commit()


# MAIN FUNCTION: CREATE ALL TABLES
def create_all_tables():
    conn = connect_database()   # Open connection only once here
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    conn.close()
    print(" All tables created successfully!")

print("Creating tables...")

if __name__ == "__main__":
    create_all_tables()