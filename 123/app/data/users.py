# app/data/users.py

from pathlib import Path
from app.data.db import DATA_DIR


def migrate_users_from_file(conn, txt_path: Path | None = None):
    """
    Read users from users.txt and insert them into the users table.
    File format per line:
        username,hashed_password,role
     or:
        username,hashed_password
    """
    if txt_path is None:
        txt_path = DATA_DIR / "users.txt"

    if not txt_path.exists():
        print(f"⚠ File not found: {txt_path}")
        print("  No users to migrate.")
        return

    cursor = conn.cursor()
    migrated_count = 0

    with txt_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) < 2:
                continue

            username = parts[0].strip()
            password_hash = parts[1].strip()
            role = parts[2].strip() if len(parts) >= 3 else "user"

            # Insert or ignore if username already exists (UNIQUE)
            cursor.execute(
                """
                INSERT OR IGNORE INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
                """,
                (username, password_hash, role),
            )
            if cursor.rowcount > 0:
                migrated_count += 1

    conn.commit()
    print(f"✅ Migrated {migrated_count} users from users.txt")
