# app/models/dataset.py

from typing import Optional


class Dataset:
    """Model for dataset metadata."""
    
    def __init__(self, name: str, source: Optional[str] = None, 
                 category: Optional[str] = None, size: int = 0, dataset_id: Optional[int] = None):
        self.id = dataset_id
        self.name = name
        self.source = source
        self.category = category
        self.size = size  # Size in bytes
    
    def get_size_gb(self) -> float:
        """Get dataset size in GB."""
        return self.size / (1024 * 1024 * 1024)
    
    def get_size_mb(self) -> float:
        """Get dataset size in MB."""
        return self.size / (1024 * 1024)
    
    def is_large(self, threshold_bytes: int = 100 * 1024 * 1024) -> bool:
        """Check if dataset is large (default threshold: 100 MB)."""
        return self.size > threshold_bytes
    
    def to_dict(self) -> dict:
        """Convert dataset to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "source": self.source,
            "category": self.category,
            "size": self.size,
            "size_gb": self.get_size_gb()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Dataset':
        """Create dataset from dictionary."""
        return cls(
            dataset_id=data.get("id"),
            name=data["name"],
            source=data.get("source"),
            category=data.get("category"),
            size=data.get("size", 0)
        )
    
    def __repr__(self) -> str:
        return f"Dataset(id={self.id}, name='{self.name}', size={self.get_size_mb():.2f} MB)"


