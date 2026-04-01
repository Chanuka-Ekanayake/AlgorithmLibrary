# Treap Data Structure

## Overview
A Treap (Tree + Heap) is a randomized binary search tree that maintains keys and randomly generated priorities for its nodes. It guarantees that operations like insertion, deletion, and search run in expected $O(\log n)$ time.

Self-balancing algorithms like AVL and Red-Black Trees require intense rotations governed by strict invariants, making them complicated to build and prone to subtle bugs. The Treap eliminates these strict loops by assigning each new node a mathematical random priority value upon creation. Because it ensures nodes strictly abide by the BST rule laterally and the Max-Heap rule vertically, it statistically stays perfectly balanced.

## Core Logic
Each node in a Treap holds two primary dimensions of data governing structural arrangement:
1. **Key:** Used to satisfy the Binary Search Tree (BST) property. For any node $N$, all nodes in its left subtree have keys strictly less than $N$'s key, and all nodes in its right subtree have keys strictly greater.
2. **Priority:** Used to satisfy the Max-Heap property. A node $N$ must have a priority higher than or equal to the priorities of its children. This value is generated continuously at random when every node is initialized.

### Operations
- **Search (`search(key)`):** Because the tree satisfies the BST property, search is exactly the same as in a standard BST: we navigate to the left child if our target key is smaller than the current node's key, and to the right child if it is larger.
- **Insertion (`insert(key, value)`):**
  1. Start by mapping down via traditional BST key comparisons and insert the element as a leaf.
  2. Assign the newly injected node a random priority.
  3. "Bubble up" the node using subtree rotations if its priority is larger than its parent. We rely on standard Left and Right pointer rotations to pull the new node upwards, perfectly preserving the BST invariants until the heap rule is correctly restored.
- **Deletion (`delete(key)`):**
  1. We execute a standard BST layout search for the node using its key.
  2. If the node is a leaf or only has one child, it is safely swapped out.
  3. If it has two children, we observe the priorities of both. We rotate the parent with its higher-priority child, thereby pushing the target node downwards in the tree. We recursively repeat this until it touches the bottom or becomes a single-child parent and can be harmlessly deleted.
