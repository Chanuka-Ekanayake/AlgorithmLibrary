"""
LRU Cache Optimizer
Implements a Least Recently Used caching strategy with O(1) performance.
Fixed for Strict Type Checking.
"""

from typing import Any, Dict, Optional

class Node:
    """
    A node in the Doubly Linked List.
    """
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

class LRUCache:
    """
    Least Recently Used (LRU) Cache using a Hash Map and Doubly Linked List.
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[Any, Node] = {}
        
        # Sentinel nodes to avoid null checks during list operations
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """Removes a node from the linked list. Safely handles Optional types."""
        prev_node = node.prev
        next_node = node.next
        
        # Explicit checks to satisfy type safety requirements
        if prev_node is not None and next_node is not None:
            prev_node.next = next_node
            next_node.prev = prev_node

    def _add_to_front(self, node: Node) -> None:
        """Inserts a node immediately after the sentinel head (MRU)."""
        temp = self.head.next
        if temp is not None:
            self.head.next = node
            node.prev = self.head
            node.next = temp
            temp.prev = node

    def get(self, key: Any, default: Any = -1) -> Any:
        """Retrieves value and moves node to the front. Returns `default` if key is not found."""
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.value
        return default

    def put(self, key: Any, value: Any) -> None:
        """Inserts/Updates value. Evicts least recently used if over capacity."""
        if key in self.cache:
            # Update existing node value and move it to the front (MRU)
            existing_node = self.cache[key]
            existing_node.value = value
            self._remove(existing_node)
            self._add_to_front(existing_node)
        else:
            # Insert new node for previously unseen key
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)
        
        if len(self.cache) > self.capacity:
            # The 'Least Recently Used' node is always tail.prev
            lru_node = self.tail.prev
            
            # Type guard: Ensure lru_node is a valid Node before accessing .key
            if lru_node is not None and lru_node is not self.head:
                self._remove(lru_node)
                # Safeguard against deleting the None-key from sentinel head
                if lru_node.key in self.cache:
                    del self.cache[lru_node.key]

    def current_size(self) -> int:
        return len(self.cache)