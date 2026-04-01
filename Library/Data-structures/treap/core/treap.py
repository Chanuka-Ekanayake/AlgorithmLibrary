import random

class TreapNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value if value is not None else key
        self.priority = random.random()
        self.left = None
        self.right = None

class Treap:
    def __init__(self):
        self.root = None
        
    def _right_rotate(self, y):
        """Perform right rotation on Treap subtree"""
        x = y.left
        y.left = x.right
        x.right = y
        return x
        
    def _left_rotate(self, x):
        """Perform left rotation on Treap subtree"""
        y = x.right
        x.right = y.left
        y.left = x
        return y
        
    def _insert(self, node, key, value):
        # Normal BST insertion
        if not node:
            return TreapNode(key, value)
            
        if key < node.key:
            node.left = self._insert(node.left, key, value)
            # Fix heap property using right rotation if left child has higher priority
            if node.left.priority > node.priority:
                node = self._right_rotate(node)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
            # Fix heap property using left rotation if right child has higher priority
            if node.right.priority > node.priority:
                node = self._left_rotate(node)
        else:
            # If the key already exists, overwrite the value, normalizing None to key
            node.value = value if value is not None else key
            
        return node
        
    def insert(self, key, value=None):
        """Insert a key-value pair into the Treap"""
        self.root = self._insert(self.root, key, value)
        
    def _delete(self, node, key):
        if not node:
            return node
            
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node to delete is found
            
            # If it's a leaf or has one child, replace it
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
                
            # If it has two children, rotate it downwards with the higher priority child
            if node.left.priority > node.right.priority:
                node = self._right_rotate(node)
                node.right = self._delete(node.right, key)
            else:
                node = self._left_rotate(node)
                node.left = self._delete(node.left, key)
                
        return node
        
    def delete(self, key):
        """Remove a key from the Treap"""
        self.root = self._delete(self.root, key)
        
    def search(self, key):
        """Retrieve a value by its key with expected O(log n) performance"""
        current = self.root
        while current:
            if key == current.key:
                return current.value
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None
