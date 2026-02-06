"""
LSM-Tree MemTable (Log-Structured Merge-Tree Component)
High-throughput in-memory buffer that converts random writes into 
sequential disk I/O through sorted flushing.
"""

import time
from typing import Dict, List, Optional, Tuple

class MemTable:
    """
    In-memory storage for the LSM-Tree.
    Buffers writes until a threshold is reached, then triggers a flush.
    """

    def __init__(self, threshold_size: int = 100):
        """
        Args:
            threshold_size: Max number of keys before the table must be 
                           flushed to persistent storage (SSTable).
        """
        self.table: Dict[str, str] = {}
        self.threshold_size = threshold_size
        self.created_at = time.time()
        self._is_flushing = False

    def put(self, key: str, value: str) -> bool:
        """
        Inserts or updates a key-value pair.
        Returns: True if the MemTable has reached its threshold and 
                 needs to be flushed to an SSTable.
        """
        # LSM-Trees treat deletes as 'Tombstones' (a special value), 
        # but for this component, we focus on the core Put logic.
        self.table[key] = value
        
        # Check if we've reached capacity
        return len(self.table) >= self.threshold_size

    def get(self, key: str) -> Optional[str]:
        """
        Point lookup in memory.
        Complexity: O(1) average.
        """
        return self.table.get(key)

    def flush(self) -> List[Tuple[str, str]]:
        """
        Prepares the data for sequential disk write (SSTable).
        Sorts the keys to ensure the resulting file is a 'Sorted String Table'.
        """
        self._is_flushing = True
        try:
            # Sorting is the 'Merge' part of LSM. 
            # It ensures disk reads remain O(log N).
            sorted_data = sorted(self.table.items())
            
            # In a real system, we'd write to disk here.
            # After flush, the table is cleared for new writes.
            self.table.clear()
            self.created_at = time.time()
            return sorted_data
        finally:
            self._is_flushing = False

    def get_size(self) -> int:
        """Returns the current number of entries."""
        return len(self.table)

    def __repr__(self) -> str:
        return f"<MemTable: {len(self.table)}/{self.threshold_size} entries>"