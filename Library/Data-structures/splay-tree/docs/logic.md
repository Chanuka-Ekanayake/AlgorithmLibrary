# Splay Tree Logic & Operations

## Core Concept

A **splay tree** is a BST where *every* access operation (search, insert, delete) concludes with a **splay** -- a sequence of rotations that moves the accessed node to the root. This creates an adaptive tree that "remembers" frequently accessed elements.

## The Splay Operation

Splaying rotates a node up to the root through a series of three cases:

### 1. Zig Case
When the node's parent is the root, perform a single rotation:
```
    P                N
   / \      →       / \
  N   C            A   P
 / \                  / \
A   B                B   C
```

### 2. Zig-Zig Case
When the node and its parent are both left (or both right) children:
```
      G                    N
     / \                  / \
    P   D                A   P
   / \          →           / \
  N   C                     B   G
 / \                           / \
A   B                         C   D
```
We rotate grandparent first, then parent. This is **different** from standard AVL-style rebalancing and is crucial for splay tree efficiency.

### 3. Zig-Zag Case
When the node is a left child of a right child (or vice versa):
```
      G                    N
     / \                  / \
    P   D                P   G
     \          →       / \ / \
      N                A B C D
     / \
    B   C
```
We rotate parent first, then grandparent.

## Why Splaying Works

1. **Brings accessed nodes to root** → O(1) next access
2. **Improves balance implicitly** → Frequently accessed subtrees become shallower
3. **No explicit balance invariants** → No color bits or height constraints
4. **Amortized O(log n)** → Individual operations can be O(n), but amortized across many is O(log n)

## Operations

### Search
1. Perform standard BST search for key
2. Splay the node found (or last node examined if not found)
3. Return boolean result

```python
def search(self, key):
    node = self.root
    while node:
        if key == node.key:
            self._splay(node)
            return True
        elif key < node.key:
            node = node.left
        else:
            node = node.right
    return False
```

### Insert
1. Perform standard BST insert
2. Splay the newly inserted node to root
3. Return success/failure (handles duplicates)

```python
def insert(self, key):
    new_node = SplayNode(key)
    # Find insertion position
    # ...
    self._splay(new_node)
    return True
```

### Delete
1. Splay the node to delete to root
2. If only left or right child, promote that child as new root
3. Otherwise, promote max from left subtree as new root, attach right subtree

```python
def delete(self, key):
    self.search(key)  # Splay node to root
    if self.root.key != key:
        return False
    
    left, right = self.root.left, self.root.right
    if not left:
        self.root = right
    elif not right:
        self.root = left
    else:
        # Splay max of left subtree
        self.root = left
        # ... find and splay max ...
        self.root.right = right
    return True
```

## Key Insights

- **No height bounds** unlike RBT (can be O(n) worst-case temporarily)
- **No randomization** unlike Treap (deterministic but adaptive)
- **Cache-friendly** due to recent nodes being at/near root
- **Optimal for skewed access patterns** (e.g., 80% searches are 20% of data)
- **Self-adjusting** → tree shape adapts to workload automatically
