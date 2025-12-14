"""
Dataset model for data science domain
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Dataset:
    """Dataset metadata model"""
    id: Optional[int] = None
    name: str = ""
    source: Optional[str] = None
    category: Optional[str] = None
    size: int = 0  # size in bytes
    
    def get_size_display(self) -> str:
        """Get human-readable size"""
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.2f} KB"
        elif self.size < 1024 * 1024 * 1024:
            return f"{self.size / (1024 * 1024):.2f} MB"
        else:
            return f"{self.size / (1024 * 1024 * 1024):.2f} GB"

