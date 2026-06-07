from typing import List, Tuple, Dict, Any, Optional

class BPlusNode:
    """Represents a node in the B+ Tree. Can be either an internal node or a leaf node."""
    def __init__(self, is_leaf: bool = False):
        self.is_leaf = is_leaf
        self.keys: List[Any] = []
        # For leaf nodes, children[i] stores the value mapped to keys[i].
        # For internal nodes, children[i] stores pointers to child BPlusNodes.
        self.children: List[Any] = []
        self.next: Optional['BPlusNode'] = None  # Pointer to next leaf node (only valid for leaf nodes)

    def __repr__(self) -> str:
        if self.is_leaf:
            return f"LeafNode(keys={self.keys})"
        else:
            return f"InternalNode(keys={self.keys})"


class BPlusTree:
    """A production-ready B+ Tree implementation supporting search, insertion, and range queries."""
    def __init__(self, order: int = 4):
        """
        Initializes the B+ Tree.
        
        :param order: The maximum number of children an internal node can have.
                      For leaf nodes, the maximum number of keys is order - 1.
        """
        if order < 3:
            raise ValueError("B+ Tree order must be at least 3.")
        self.root: BPlusNode = BPlusNode(is_leaf=True)
        self.order: int = order

    def search(self, key: Any) -> Tuple[Optional[Any], int]:
        """
        Searches for a key in the B+ Tree.
        
        :param key: The key to search for.
        :return: A tuple of (value, pages_accessed), where value is None if key is not found.
        """
        pages_accessed = 0
        curr = self.root
        
        # Traverse down to the leaf node
        while not curr.is_leaf:
            pages_accessed += 1
            idx = 0
            while idx < len(curr.keys) and key >= curr.keys[idx]:
                idx += 1
            curr = curr.children[idx]
            
        pages_accessed += 1  # Read the leaf node
        
        # Search the keys in the leaf node
        for idx, k in enumerate(curr.keys):
            if k == key:
                return curr.children[idx], pages_accessed
                
        return None, pages_accessed

    def search_range(self, start_key: Any, end_key: Any) -> Tuple[List[Tuple[Any, Any]], int]:
        """
        Performs a range query, returning all (key, value) pairs within [start_key, end_key].
        
        :param start_key: The lower bound (inclusive).
        :param end_key: The upper bound (inclusive).
        :return: A tuple of (list of (key, value) pairs, pages_accessed).
        """
        pages_accessed = 0
        curr = self.root
        
        # Traverse down to find the starting leaf node
        while not curr.is_leaf:
            pages_accessed += 1
            idx = 0
            while idx < len(curr.keys) and start_key >= curr.keys[idx]:
                idx += 1
            curr = curr.children[idx]
            
        pages_accessed += 1  # Read the starting leaf node
        
        results = []
        done = False
        
        # Traverse the linked list of leaf nodes
        while curr and not done:
            for idx, k in enumerate(curr.keys):
                if start_key <= k <= end_key:
                    results.append((k, curr.children[idx]))
                elif k > end_key:
                    done = True
                    break
            if not done:
                curr = curr.next
                if curr:
                    pages_accessed += 1  # Read the next leaf page
                    
        return results, pages_accessed

    def insert(self, key: Any, value: Any) -> int:
        """
        Inserts a key-value pair into the B+ Tree. If the key already exists, updates its value.
        
        :param key: The key to insert.
        :param value: The value to associate with the key.
        :return: The number of page writes simulated during the operation.
        """
        leaf, path = self._find_leaf_and_path(key)
        
        # Find insertion position
        idx = 0
        while idx < len(leaf.keys) and key > leaf.keys[idx]:
            idx += 1
            
        # Update if key already exists
        if idx < len(leaf.keys) and leaf.keys[idx] == key:
            leaf.children[idx] = value
            return 1  # 1 page write (update)
            
        # Insert key and value
        leaf.keys.insert(idx, key)
        leaf.children.insert(idx, value)
        
        page_writes = 1
        
        # Split leaf if it exceeds capacity
        if len(leaf.keys) >= self.order:
            page_writes += self._split_leaf(leaf, path)
            
        return page_writes

    def _find_leaf_and_path(self, key: Any) -> Tuple[BPlusNode, List[BPlusNode]]:
        """Helper to find the target leaf and track the ancestor path."""
        path = []
        curr = self.root
        while not curr.is_leaf:
            path.append(curr)
            idx = 0
            while idx < len(curr.keys) and key >= curr.keys[idx]:
                idx += 1
            curr = curr.children[idx]
        return curr, path

    def _split_leaf(self, leaf: BPlusNode, path: List[BPlusNode]) -> int:
        """Splits a leaf node and promotes the split key to its parent."""
        mid = len(leaf.keys) // 2
        
        # Create right leaf
        right = BPlusNode(is_leaf=True)
        right.keys = leaf.keys[mid:]
        right.children = leaf.children[mid:]
        
        # Keep left keys and values in leaf
        leaf.keys = leaf.keys[:mid]
        leaf.children = leaf.children[:mid]
        
        # Update leaf links
        right.next = leaf.next
        leaf.next = right
        
        page_writes = 2  # Wrote left and right leaves
        
        # Copy-promote the first key of the right node
        promoted_key = right.keys[0]
        
        if not path:
            # Create a new root
            new_root = BPlusNode(is_leaf=False)
            new_root.keys = [promoted_key]
            new_root.children = [leaf, right]
            self.root = new_root
            page_writes += 1
        else:
            parent = path.pop()
            page_writes += self._insert_into_parent(parent, leaf, right, promoted_key, path)
            
        return page_writes

    def _insert_into_parent(self, parent: BPlusNode, left: BPlusNode, right: BPlusNode, key: Any, path: List[BPlusNode]) -> int:
        """Inserts a promoted key and child pointer into an internal parent node."""
        idx = 0
        while idx < len(parent.keys) and key > parent.keys[idx]:
            idx += 1
            
        parent.keys.insert(idx, key)
        parent.children.insert(idx + 1, right)
        
        page_writes = 1  # Wrote the updated parent
        
        # Split parent if it exceeds capacity
        if len(parent.keys) >= self.order:
            page_writes += self._split_internal(parent, path)
            
        return page_writes

    def _split_internal(self, node: BPlusNode, path: List[BPlusNode]) -> int:
        """Splits an internal node and promotes the split key to its parent."""
        mid = len(node.keys) // 2
        
        # Create new right internal node
        right = BPlusNode(is_leaf=False)
        right.keys = node.keys[mid + 1:]
        right.children = node.children[mid + 1:]
        
        # The key to promote is moved out of the children entirely
        promoted_key = node.keys[mid]
        
        # Keep left keys and children
        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]
        
        page_writes = 2  # Wrote left and right internal nodes
        
        if not path:
            # Create a new root
            new_root = BPlusNode(is_leaf=False)
            new_root.keys = [promoted_key]
            new_root.children = [node, right]
            self.root = new_root
            page_writes += 1
        else:
            parent = path.pop()
            page_writes += self._insert_into_parent(parent, node, right, promoted_key, path)
            
        return page_writes

    def visualize(self) -> str:
        """Returns a formatted string representing the hierarchical structure of the B+ Tree."""
        if not self.root.keys:
            return "Empty Tree"
            
        lines = []
        def _traverse(node: BPlusNode, level: int):
            indent = "    " * level
            if node.is_leaf:
                # Format pairs nicely
                pairs = [f"{k}:{node.children[idx]}" for idx, k in enumerate(node.keys)]
                lines.append(f"{indent}Leaf [Keys/Vals]: [{', '.join(pairs)}]")
            else:
                lines.append(f"{indent}Internal [Keys]: {node.keys}")
                for child in node.children:
                    _traverse(child, level + 1)
                    
        _traverse(self.root, 0)
        return "\n".join(lines)
