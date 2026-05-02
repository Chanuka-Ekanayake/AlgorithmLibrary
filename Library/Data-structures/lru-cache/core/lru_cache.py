from typing import Any, Dict, Optional
from collections import OrderedDict


class LRUCache:
    """
    Least Recently Used (LRU) Cache implementation using a doubly-linked list and hash map.
    Evicts the least recently used item when capacity is exceeded.
    
    This is a production-grade implementation optimized for system design and optimization scenarios,
    such as CPU caches, database query caches, and distributed system memoization.
    """
    
    def __init__(self, capacity: int):
        """
        Initialize the LRU Cache.
        
        Args:
            capacity: Maximum number of items the cache can hold.
                     Must be positive.
        
        Raises:
            ValueError: If capacity is not positive.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self.capacity: int = capacity
        # OrderedDict maintains insertion order in Python 3.7+
        self.cache: OrderedDict[Any, Any] = OrderedDict()
    
    def get(self, key: Any) -> Optional[Any]:
        """
        Retrieve a value from the cache by key.
        
        Accessing an item marks it as recently used and moves it to the end.
        
        Args:
            key: The key to look up.
        
        Returns:
            The value associated with the key, or None if key not found.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if key not in self.cache:
            return None
        
        # Move the accessed item to the end (mark as recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: Any, value: Any) -> None:
        """
        Insert or update a key-value pair in the cache.
        
        If the key already exists, update its value and mark it as recently used.
        If adding a new key exceeds capacity, evict the least recently used item.
        
        Args:
            key: The key to insert or update.
            value: The value to associate with the key.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # If key exists, update it and move to end
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)
            return
        
        # Add new key-value pair
        self.cache[key] = value
        
        # If capacity exceeded, remove the least recently used item (first item)
        if len(self.cache) > self.capacity:
            # popitem(last=False) removes the first (oldest) item
            self.cache.popitem(last=False)
    
    def delete(self, key: Any) -> bool:
        """
        Delete a key from the cache.
        
        Args:
            key: The key to delete.
        
        Returns:
            True if the key was deleted, False if it didn't exist.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all items from the cache."""
        self.cache.clear()
    
    def size(self) -> int:
        """Return the current number of items in the cache."""
        return len(self.cache)
    
    def is_full(self) -> bool:
        """Check if the cache is at capacity."""
        return len(self.cache) == self.capacity
    
    def get_all_keys(self) -> list:
        """
        Get all keys in the cache in order of recency (oldest to newest).
        
        Returns:
            List of keys ordered by access time (least recent first).
        """
        return list(self.cache.keys())
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary containing cache metrics.
        """
        return {
            "capacity": self.capacity,
            "current_size": len(self.cache),
            "occupancy_rate": len(self.cache) / self.capacity,
            "keys_in_order": list(self.cache.keys())
        }
