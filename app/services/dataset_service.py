from app.data.db import connect_database
from app.data.datasets import (
    get_all_datasets,
    create_dataset,
    update_dataset_size,
    delete_dataset
)


def list_datasets(db_path=None):
    """Return all datasets."""
    conn = connect_database(db_path)
    datasets = get_all_datasets(conn)
    conn.close()
    return datasets


def add_dataset(name, source=None, category=None, size=None, created_date=None, db_path=None):
    """Create dataset with validation."""
    if not name or name.strip() == "":
        return False, "Dataset name cannot be empty."

    conn = connect_database(db_path)
    new_id = create_dataset(conn, name, source, category, size)
    conn.close()
    return True, f"Dataset '{name}' created with ID {new_id}."


def resize_dataset(dataset_id, new_size, db_path=None):
    """Update dataset size."""
    conn = connect_database(db_path)
    update_dataset_size(conn, dataset_id, new_size)
    conn.close()
    return True, f"Dataset {dataset_id} updated."


def remove_dataset(dataset_id, db_path=None):
    """Delete dataset."""
    conn = connect_database(db_path)
    delete_dataset(conn, dataset_id)
    conn.close()
    return True, f"Dataset {dataset_id} deleted."