# B+ Tree Logic & Mechanics

A **B+ Tree** is an $M$-way search tree that balances high branching factors with efficient data storage. It is designed to work well on block storage devices (such as SSDs and HDDs).

---

## 1. Node Structures

A B+ Tree contains two types of nodes: **Internal Nodes** and **Leaf Nodes**.

```text
               [ 20 | 50 ]  <-- Internal Node (Keys only, guides searches)
              /     |     \
   [ 10 | 15 ]  [ 30 | 45 ]  [ 60 | 75 ]  <-- Internal Nodes (Level 1)
   /    |    \  /    |    \  /    |    \
 [A]   [B]   [C]    ...    [X]   [Y]   [Z]  <-- Leaf Nodes (Keys + Values + Linked List)
  |     |     |             |     |     |
  v     v     v             v     v     v
 [ 5]->[10]->[15] -------> [60]->[70]->[75] (Leaf Linked List)
```

### Internal Nodes
* **Keys:** A sorted list of up to $M - 1$ keys.
* **Children:** A list of up to $M$ pointers to child nodes (either other internal nodes or leaf nodes).
* **Role:** They act as routers. If we search for a key $K$, we find the first key in the internal node greater than $K$. The child pointer at that index leads us to the next level down.

### Leaf Nodes
* **Keys:** A sorted list of up to $M - 1$ keys.
* **Children/Values:** A list of values associated directly with the keys.
* **Next Pointer:** A reference to the sibling leaf node immediately to the right.
* **Role:** They store the actual payload/data.

---

## 2. Dynamic Splits & Balancing

The B+ Tree remains balanced because all insertions start at the leaf level, and nodes split when they exceed capacity, propagating updates upward.

### Leaf Splits
When a leaf node reaches $M$ keys (where $M$ is the order of the tree):
1. **Divide:** Split the keys and values into two equal (or near-equal) halves at `mid = len(keys) // 2`.
2. **Promote:** The first key of the new right-hand leaf node is **copied** and promoted to the parent node.
3. **Link:** Update the sibling pointers to keep the leaf linked list intact:
   `right.next = left.next`
   `left.next = right`

### Internal Splits
When an internal node reaches $M$ keys:
1. **Divide:** Split the keys and child pointers.
2. **Promote:** The key at index `mid` is **moved** out of the node completely and inserted into the parent. (Unlike leaf splits, this key does not remain in the child node, because internal nodes do not hold data).

---

## 3. Search Operations

### Point Lookup
* Start at the root.
* Binary or linear search the keys of the current internal node to find the child pointer matching the target key.
* Repeat down the levels until a leaf node is reached.
* Search the leaf keys. Return the value if found, or `None` if not.

### Range Scan
* Find the leaf node containing the `start_key` using a Point Lookup.
* Traverse the keys in the leaf.
* When the end of the current leaf node is reached, follow the `.next` pointer to load the sibling leaf.
* Continue until a key greater than `end_key` is encountered.
