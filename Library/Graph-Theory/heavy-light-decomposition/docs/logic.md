# Logic

Heavy-Light Decomposition splits a rooted tree into chains so that any path from one node to another crosses only a small number of chain boundaries.

## Core Idea

1. Run a DFS to compute subtree sizes.
2. For each node, mark the child with the largest subtree as the heavy child.
3. Follow heavy children to form long chains.
4. Assign each node a position in a linear array.
5. Use a segment tree over that array for range operations.

## Why It Works

A light edge always leads into a subtree that is at most half the size of the current subtree. That means any root-to-node path can cross only $O(\log n)$ light edges.

When a query asks for information on a path between two nodes, the path is broken into a small number of contiguous intervals in the flattened array. Each interval can be processed by the segment tree in logarithmic time.

## Implementation Notes

- `parent[]` stores the tree parent for each node.
- `depth[]` tracks how far a node is from the root.
- `head[]` stores the top node of the current heavy chain.
- `position[]` stores the flattened index used by the segment tree.
- `subtree_size[]` lets subtree queries become a single contiguous range.
