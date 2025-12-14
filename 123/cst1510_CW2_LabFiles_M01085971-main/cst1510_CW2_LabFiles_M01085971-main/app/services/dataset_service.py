from app.data.datasets import (
    get_all_datasets,
    get_dataset_by_id,
    create_dataset,
    update_dataset_size,
    delete_dataset
)


def list_datasets():
    """Return all datasets."""
    return get_all_datasets()


def add_dataset(name, source=None, category=None, size=None, created_date=None):
    """Create dataset with validation."""
    if not name or name.strip() == "":
        return False, "Dataset name cannot be empty."

    new_id = create_dataset(name, source, category, size, created_date)
    return True, f"Dataset '{name}' created with ID {new_id}."


def resize_dataset(dataset_id, new_size):
    """Update dataset size."""
    update_dataset_size(dataset_id, new_size)
    return True, f"Dataset {dataset_id} updated."


def remove_dataset(dataset_id):
    """Delete dataset."""
    delete_dataset(dataset_id)
    return True, f"Dataset {dataset_id} deleted."