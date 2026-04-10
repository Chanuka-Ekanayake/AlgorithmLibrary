class Color:
    RED   = "RED"
    BLACK = "BLACK"


class RBNode:
    """A single node in the Red-Black Tree."""

    def __init__(self, key, value=None):
        self.key    = key
        self.value  = value if value is not None else key
        self.color  = Color.RED       # New nodes are always inserted RED
        self.left   = None
        self.right  = None
        self.parent = None


class RedBlackTree:
    """
    A self-balancing Binary Search Tree that enforces four structural invariants:
      1. Every node is RED or BLACK.
      2. The root is always BLACK.
      3. No two consecutive RED nodes may appear on any root-to-leaf path.
      4. Every root-to-leaf path contains the same number of BLACK nodes.

    These invariants guarantee O(log n) worst-case time for search, insert, and delete.
    """

    def __init__(self):
        # Sentinel NIL node — all leaves point here; it is always BLACK
        self.NIL  = RBNode(key=None)
        self.NIL.color = Color.BLACK
        self.root = self.NIL

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def insert(self, key, value=None):
        """Insert a key-value pair and restore Red-Black invariants."""
        node        = RBNode(key, value)
        node.left   = self.NIL
        node.right  = self.NIL
        node.parent = self.NIL
        self._bst_insert(node)
        self._fix_insert(node)

    def delete(self, key):
        """Remove the node with the given key and restore Red-Black invariants."""
        target = self._find_node(self.root, key)
        if target is self.NIL:
            return   # Key not present — nothing to do
        self._delete_node(target)

    def search(self, key):
        """Return the value for the given key, or None if not found."""
        node = self._find_node(self.root, key)
        if node is self.NIL:
            return None
        return node.value

    def inorder(self):
        """Return a sorted list of (key, value) pairs via in-order traversal."""
        result = []
        self._inorder(self.root, result)
        return result

    # ------------------------------------------------------------------
    # BST helpers
    # ------------------------------------------------------------------

    def _bst_insert(self, node):
        """Standard BST insert — sets parent/child pointers."""
        parent  = self.NIL
        current = self.root

        while current is not self.NIL:
            parent = current
            if node.key < current.key:
                current = current.left
            elif node.key > current.key:
                current = current.right
            else:
                # Duplicate key — overwrite value
                current.value = node.value
                return

        node.parent = parent

        if parent is self.NIL:
            self.root = node          # Tree was empty
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

    def _find_node(self, node, key):
        """Return the node matching key, or self.NIL if absent."""
        while node is not self.NIL:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return self.NIL

    def _inorder(self, node, result):
        if node is self.NIL:
            return
        self._inorder(node.left, result)
        result.append((node.key, node.value))
        self._inorder(node.right, result)

    # ------------------------------------------------------------------
    # Rotations — core structural primitive; they never change key order
    # ------------------------------------------------------------------

    def _left_rotate(self, x):
        """
        Pivot: x goes down-left, y (x's right child) goes up.
              x                  y
             / \\      =>        / \\
            A   y              x   C
               / \\            / \\
              B   C          A   B
        """
        y         = x.right
        x.right   = y.left

        if y.left is not self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is self.NIL:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left   = x
        x.parent = y

    def _right_rotate(self, y):
        """
        Pivot: y goes down-right, x (y's left child) goes up.
               y                x
              / \\    =>        / \\
             x   C            A   y
            / \\                  / \\
           A   B                B   C
        """
        x         = y.left
        y.left    = x.right

        if x.right is not self.NIL:
            x.right.parent = y

        x.parent = y.parent

        if y.parent is self.NIL:
            self.root = x
        elif y is y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        x.right  = y
        y.parent = x

    # ------------------------------------------------------------------
    # Insert fixup — restores invariants after a RED node is inserted
    # ------------------------------------------------------------------

    def _fix_insert(self, z):
        """
        After BST insertion, z is RED. If z's parent is also RED, we have
        a violation of invariant #3. We fix it with a combination of
        recoloring and rotations, iterating upward until no violation remains.
        """
        while z.parent.color == Color.RED:
            if z.parent is z.parent.parent.left:  # Parent is a LEFT child
                uncle = z.parent.parent.right

                if uncle.color == Color.RED:
                    # Case 1 — Uncle RED: recolor and move violation up
                    z.parent.color         = Color.BLACK
                    uncle.color            = Color.BLACK
                    z.parent.parent.color  = Color.RED
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        # Case 2 — z is a RIGHT child: rotate to make it left
                        z = z.parent
                        self._left_rotate(z)
                    # Case 3 — z is a LEFT child: recolor and right-rotate grandparent
                    z.parent.color        = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self._right_rotate(z.parent.parent)

            else:                                  # Parent is a RIGHT child (mirror)
                uncle = z.parent.parent.left

                if uncle.color == Color.RED:
                    # Case 1 (mirror)
                    z.parent.color        = Color.BLACK
                    uncle.color           = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        # Case 2 (mirror)
                        z = z.parent
                        self._right_rotate(z)
                    # Case 3 (mirror)
                    z.parent.color        = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self._left_rotate(z.parent.parent)

        self.root.color = Color.BLACK   # Invariant #2: root is always BLACK

    # ------------------------------------------------------------------
    # Delete helpers
    # ------------------------------------------------------------------

    def _transplant(self, u, v):
        """Replace subtree rooted at u with subtree rooted at v."""
        if u.parent is self.NIL:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        """Return the leftmost node in the subtree rooted at node."""
        while node.left is not self.NIL:
            node = node.left
        return node

    def _delete_node(self, z):
        """
        Remove node z and restore Red-Black invariants.

        Three structural cases:
          A) z has no left child        → splice out z, replace with right child
          B) z has no right child       → splice out z, replace with left child
          C) z has two children         → replace z's key with its in-order
                                          successor y, then delete y (which
                                          falls into case A or B)
        """
        y              = z
        y_original_color = y.color

        if z.left is self.NIL:              # Case A
            x = z.right
            self._transplant(z, z.right)

        elif z.right is self.NIL:           # Case B
            x = z.left
            self._transplant(z, z.left)

        else:                               # Case C — two children
            y              = self._minimum(z.right)   # in-order successor
            y_original_color = y.color
            x              = y.right

            if y.parent is z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right        = z.right
                y.right.parent = y

            self._transplant(z, y)
            y.left         = z.left
            y.left.parent  = y
            y.color        = z.color

        # If the removed / moved node was BLACK, we may have lost a BLACK
        # node from some root-to-leaf path — fix it.
        if y_original_color == Color.BLACK:
            self._fix_delete(x)

    def _fix_delete(self, x):
        """
        x has one fewer BLACK on its path than required. We push the
        "extra black" up the tree with rotations and recoloring until
        x is RED (absorb it) or x is the root (done).
        """
        while x is not self.root and x.color == Color.BLACK:
            if x is x.parent.left:
                w = x.parent.right       # w is x's sibling

                if w.color == Color.RED:
                    # Case 1 — sibling RED: rotate to make sibling BLACK
                    w.color        = Color.BLACK
                    x.parent.color = Color.RED
                    self._left_rotate(x.parent)
                    w = x.parent.right

                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    # Case 2 — both of sibling's children BLACK: recolor, move up
                    w.color = Color.RED
                    x       = x.parent
                else:
                    if w.right.color == Color.BLACK:
                        # Case 3 — sibling's right child BLACK: rotate sibling
                        w.left.color = Color.BLACK
                        w.color      = Color.RED
                        self._right_rotate(w)
                        w = x.parent.right
                    # Case 4 — sibling's right child RED: rotate parent
                    w.color        = x.parent.color
                    x.parent.color = Color.BLACK
                    w.right.color  = Color.BLACK
                    self._left_rotate(x.parent)
                    x = self.root

            else:                        # Mirror cases (x is right child)
                w = x.parent.left

                if w.color == Color.RED:
                    # Case 1 (mirror)
                    w.color        = Color.BLACK
                    x.parent.color = Color.RED
                    self._right_rotate(x.parent)
                    w = x.parent.left

                if w.right.color == Color.BLACK and w.left.color == Color.BLACK:
                    # Case 2 (mirror)
                    w.color = Color.RED
                    x       = x.parent
                else:
                    if w.left.color == Color.BLACK:
                        # Case 3 (mirror)
                        w.right.color = Color.BLACK
                        w.color       = Color.RED
                        self._left_rotate(w)
                        w = x.parent.left
                    # Case 4 (mirror)
                    w.color        = x.parent.color
                    x.parent.color = Color.BLACK
                    w.left.color   = Color.BLACK
                    self._right_rotate(x.parent)
                    x = self.root

        x.color = Color.BLACK   # Either x is root, or we absorbed the extra black
