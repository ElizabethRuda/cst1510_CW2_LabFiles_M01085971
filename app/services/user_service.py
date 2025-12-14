# app/services/user_service.py

import bcrypt
from app.data.db import connect_database


def register_user(username: str, password: str, role: str = "user"):
    """
    Register a new user in the database with bcrypt password hashing.
    Returns (success: bool, message: str)
    """
    conn = connect_database()
    cursor = conn.cursor()

    # Check if username already exists
    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,),
    )
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return False, f"Error: Username '{username}' already exists."

    # Hash password
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt).decode("utf-8")

    # Insert new user
    cursor.execute(
        """
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
        """,
        (username, hashed, role),
    )
    conn.commit()
    conn.close()
    return True, f"User '{username}' registered successfully!"


def login_user(username: str, password: str):
    """
    Verify user credentials.
    Returns (success: bool, message: str)
    """
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, password_hash, role
        FROM users
        WHERE username = ?
        """,
        (username,),
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return False, "User not found."

    stored_hash = row[1]
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        return True, f"Welcome, {username}!"
    else:
        return False, "Invalid password."
