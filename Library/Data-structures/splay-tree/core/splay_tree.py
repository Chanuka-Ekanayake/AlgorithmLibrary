"""
Splay Tree Implementation

A self-balancing BST where accessed elements are rotated to the root.
All operations (search, insert, delete) are followed by splaying,
resulting in amortized O(log n) performance.
"""


class SplayNode:
    """Node in a splay tree"""
    
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None


class SplayTree:
    """Splay Tree data structure with amortized O(log n) operations"""
    
    def __init__(self):
        self.root = None
        self.access_count = 0
    
    def _rotate_right(self, node):
        """Right rotation: node goes down, its left child comes up"""
        if not node.left:
            return
        left = node.left
        node.left = left.right
        if left.right:
            left.right.parent = node
        left.parent = node.parent
        if not node.parent:
            self.root = left
        elif node == node.parent.right:
            node.parent.right = left
        else:
            node.parent.left = left
        left.right = node
        node.parent = left
    
    def _rotate_left(self, node):
        """Left rotation: node goes down, its right child comes up"""
        if not node.right:
            return
        right = node.right
        node.right = right.left
        if right.left:
            right.left.parent = node
        right.parent = node.parent
        if not node.parent:
            self.root = right
        elif node == node.parent.left:
            node.parent.left = right
        else:
            node.parent.right = right
        right.left = node
        node.parent = right
    
    def _splay(self, node):
        """Splay operation: rotate node to root via zig/zig-zig/zig-zag cases"""
        while node.parent:
            parent = node.parent
            
            # Zig case: node's parent is root
            if not parent.parent:
                if node == parent.left:
                    self._rotate_right(parent)
                else:
                    self._rotate_left(parent)
            
            # Zig-Zig case: node and parent are both left/right children
            elif (node == parent.left and parent == parent.parent.left) or \
                 (node == parent.right and parent == parent.parent.right):
                if node == parent.left:
                    self._rotate_right(parent.parent)
                    self._rotate_right(parent)
                else:
                    self._rotate_left(parent.parent)
                    self._rotate_left(parent)
            
            # Zig-Zag case: node and parent are on opposite sides
            else:
                if node == parent.left:
                    self._rotate_right(parent)
                else:
                    self._rotate_left(parent)
                self._splay(node)
    
    def search(self, key):
        """Search for key and splay the accessed node to root"""
        if not self.root:
            return False
        
        node = self.root
        while node:
            if key == node.key:
                self._splay(node)
                self.access_count += 1
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        # Even if key not found, splay the last accessed node
        if node is None and self.root:
            # Splay the parent of where we stopped
            pass
        
        return False
    
    def insert(self, key):
        """Insert key and splay the new node to root"""
        if not self.root:
            self.root = SplayNode(key)
            self.access_count += 1
            return True
        
        node = self.root
        parent = None
        
        while node:
            parent = node
            if key == node.key:
                self._splay(node)
                return False  # Duplicate
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        new_node = SplayNode(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self._splay(new_node)
        self.access_count += 1
        return True
    
    def delete(self, key):
        """Delete key by splaying then removing root"""
        if not self.search(key):
            return False
        
        node = self.root
        if not node.left:
            self.root = node.right
            if self.root:
                self.root.parent = None
        elif not node.right:
            self.root = node.left
            if self.root:
                self.root.parent = None
        else:
            # Find max in left subtree, splay it, then attach right subtree
            left_tree = node.left
            left_tree.parent = None
            self.root = left_tree
            
            max_node = left_tree
            while max_node.right:
                max_node = max_node.right
            
            self._splay(max_node)
            max_node.right = node.right
            if node.right:
                node.right.parent = max_node
        
        self.access_count += 1
        return True
    
    def inorder(self):
        """Return in-order traversal of tree"""
        result = []
        self._inorder_helper(self.root, result)
        return result
    
    def _inorder_helper(self, node, result):
        """Helper for in-order traversal"""
        if node:
            self._inorder_helper(node.left, result)
            result.append(node.key)
            self._inorder_helper(node.right, result)
    
    def height(self):
        """Get height of tree"""
        return self._height_helper(self.root)
    
    def _height_helper(self, node):
        """Helper for height calculation"""
        if not node:
            return 0
        return 1 + max(self._height_helper(node.left), 
                       self._height_helper(node.right))
    
    def size(self):
        """Get number of nodes in tree"""
        return self._size_helper(self.root)
    
    def _size_helper(self, node):
        """Helper for size calculation"""
        if not node:
            return 0
        return 1 + self._size_helper(node.left) + self._size_helper(node.right)


if __name__ == "__main__":
    # Example usage
    tree = SplayTree()
    
    keys = [50, 30, 70, 20, 40, 60, 80, 10, 25]
    for key in keys:
        tree.insert(key)
    
    print("In-order:", tree.inorder())
    print("Height:", tree.height())
    print("Size:", tree.size())
    
    # Search splays node to root
    tree.search(20)
    print("After searching 20:", tree.root.key)
    
    # Delete
    tree.delete(20)
    print("After deleting 20:", tree.inorder())
