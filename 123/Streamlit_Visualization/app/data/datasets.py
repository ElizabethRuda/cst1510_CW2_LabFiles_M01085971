# app/data/datasets.py

from pathlib import Path
import csv
from app.data.db import DATA_DIR


# ---------- CSV LOADING ----------

def load_datasets_from_csv(conn, csv_path: Path | None = None):
    """
    Load datasets from datasets_metadata.csv into datasets_metadata table.
    Expected CSV columns: id, name, source, category, size
    """
    if csv_path is None:
        csv_path = DATA_DIR / "datasets_metadata.csv"

    cursor = conn.cursor()

    # If table already has rows, do not duplicate
    cursor.execute("SELECT COUNT(*) FROM datasets_metadata")
    count = cursor.fetchone()[0]
    if count > 0:
        return

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name")
            source = row.get("source")
            category = row.get("category")
            size_str = row.get("size")
            size = int(size_str) if size_str else None

            cursor.execute(
                """
                INSERT INTO datasets_metadata (name, source, category, size)
                VALUES (?, ?, ?, ?)
                """,
                (name, source, category, size),
            )

    conn.commit()
    print("✅ Loaded datasets from datasets_metadata.csv")


# ---------- CRUD FUNCTIONS ----------

def get_all_datasets(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, name, source, category, size
        FROM datasets_metadata
        ORDER BY id
        """
    )
    return cursor.fetchall()


def create_dataset(conn, name: str, source: str | None = None,
                   category: str | None = None, size: int | None = None):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO datasets_metadata (name, source, category, size)
        VALUES (?, ?, ?, ?)
        """,
        (name, source, category, size),
    )
    conn.commit()
    return cursor.lastrowid


def update_dataset_size(conn, dataset_id: int, new_size: int):
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE datasets_metadata
        SET size = ?
        WHERE id = ?
        """,
        (new_size, dataset_id),
    )
    conn.commit()


def delete_dataset(conn, dataset_id: int):
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM datasets_metadata WHERE id = ?",
        (dataset_id,),
    )
    conn.commit()
