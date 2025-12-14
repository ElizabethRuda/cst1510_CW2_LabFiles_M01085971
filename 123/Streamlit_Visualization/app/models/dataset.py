"""
Dataset Model Class
Week 11: OOP Refactoring
"""

from typing import Optional
from datetime import datetime


class Dataset:
    """
    Represents a dataset in the Intelligence Platform.
    
    Attributes:
        id: Dataset ID (from database)
        name: Dataset name
        source: Data source
        category: Dataset category
        size: Dataset size in MB
        last_updated: Last update date
    """
    
    def __init__(
        self,
        name: str,
        source: Optional[str] = None,
        category: Optional[str] = None,
        size: Optional[int] = None,
        last_updated: Optional[str] = None,
        dataset_id: Optional[int] = None
    ):
        """
        Initialize a Dataset object.
        
        Args:
            name: Dataset name
            source: Data source
            category: Dataset category
            size: Size in MB
            last_updated: Last update date (YYYY-MM-DD)
            dataset_id: Optional database ID
        """
        self.id = dataset_id
        self.name = name
        self.source = source
        self.category = category
        self.size = size or 0
        self.last_updated = last_updated or datetime.now().strftime('%Y-%m-%d')
    
    def is_large(self, threshold_mb: int = 100) -> bool:
        """
        Check if dataset is large.
        
        Args:
            threshold_mb: Size threshold in MB
            
        Returns:
            True if dataset size exceeds threshold
        """
        # Size is stored in bytes, convert threshold to bytes
        threshold_bytes = threshold_mb * 1024 * 1024
        return self.size > threshold_bytes
    
    def update_size(self, new_size: int) -> None:
        """
        Update dataset size.
        
        Args:
            new_size: New size in MB
        """
        self.size = new_size
        self.last_updated = datetime.now().strftime('%Y-%m-%d')
    
    def get_size_gb(self) -> float:
        """
        Get dataset size in GB.
        
        Returns:
            Size in GB
        """
        # Size is stored in bytes, convert to GB
        return self.size / (1024.0 * 1024.0 * 1024.0)
    
    def get_formatted_size(self) -> str:
        """
        Get formatted size string.
        
        Returns:
            Formatted size (e.g., "150 MB" or "1.5 GB")
        """
        if self.size >= 1024:
            return f"{self.get_size_gb():.2f} GB"
        return f"{self.size} MB"
    
    def __str__(self) -> str:
        """String representation of Dataset."""
        return f"Dataset(id={self.id}, name='{self.name}', size={self.get_formatted_size()}, category='{self.category}')"
    
    def __repr__(self) -> str:
        """Representation of Dataset."""
        return self.__str__()
    
    def to_dict(self) -> dict:
        """
        Convert Dataset to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'name': self.name,
            'source': self.source,
            'category': self.category,
            'size': self.size,
            'last_updated': self.last_updated
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Dataset':
        """
        Create Dataset from dictionary.
        
        Args:
            data: Dictionary with dataset data
            
        Returns:
            Dataset object
        """
        return cls(
            name=data.get('name', ''),
            source=data.get('source'),
            category=data.get('category'),
            size=data.get('size', 0),
            last_updated=data.get('last_updated'),
            dataset_id=data.get('id')
        )

