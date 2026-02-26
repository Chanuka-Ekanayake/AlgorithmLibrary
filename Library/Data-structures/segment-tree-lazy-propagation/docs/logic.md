# Algorithm Logic: Segment Tree with Lazy Propagation

## 1. The Core Concept

A **Segment Tree** is a binary tree that stores aggregate information (e.g., sum, min, max) about contiguous ranges (segments) of an array. It answers **range queries** in `O(log n)` instead of the `O(n)` you'd need by iterating.

**Lazy Propagation** is the technique that extends the Segment Tree to also handle **range updates** in `O(log n)`. Without it, applying a value to `n` elements naively would cost `O(n log n)`.

---

## 2. Structural Breakdown

### 2.1 The Tree Array

The tree is stored as a flat array of size `4 * n`. For a node at index `i`:
- **Left child** is at index `2i + 1`
- **Right child** is at index `2i + 2`
- The **root** is at index `0`

Each node `tree[i]` stores the **sum** of all elements in its segment.

### 2.2 The Lazy Array

A parallel array `lazy[i]` holds **pending (deferred) updates**. Instead of immediately propagating an update to all child nodes (which is expensive), we "tag" the parent and defer the work until we actually need to look at those children.

---

## 3. Step-by-Step Operations

### 3.1 Build — `O(n)`

We build the tree bottom-up via recursion:
1. If the node covers a single element (`start == end`), store `data[start]`.
2. Otherwise, recursively build the left and right halves, then set the parent's value to the sum of its children.

```text
Array: [2, 4, 5, 7, 8, 9]

              tree[0]=35 [0,5]
             /            \
      tree[1]=11 [0,2]   tree[2]=24 [3,5]
       /         \         /          \
  tree[3]=6[0,1] tree[4]=5[2,2]  tree[5]=15[3,4]  tree[6]=9[5,5]
   /       \                       /       \
tree[7]=2  tree[8]=4          tree[9]=7  tree[10]=8
  [0,0]     [1,1]               [3,3]     [4,4]
```

### 3.2 Range Update with Lazy Propagation — `O(log n)`

To add `val` to every element in `[l, r]`:

1. **No Overlap** (`r < start` or `end < l`): This segment is outside the range. Do nothing.
2. **Full Overlap** (`l <= start` and `end <= r`): This segment is completely inside the range. Update `tree[node]` directly (add `val * segment_length`) and **tag** `lazy[node] += val`. Stop recursing — the children will be updated later.
3. **Partial Overlap**: First **push the lazy tag down** to children, then recurse into both children, and recalculate the parent's stored sum from children.

**Push Down** logic:
```
When lazy[node] != 0:
  child_sum += lazy[node] * child_length
  lazy[child] += lazy[node]
  lazy[node] = 0   # Tag has been passed; clear it
```

### 3.3 Range Query — `O(log n)`

To get the sum of `[l, r]`:

1. **No Overlap**: Return `0`.
2. **Full Overlap**: Return `tree[node]` directly.
3. **Partial Overlap**: **Push the lazy tag down** first (to ensure children are up-to-date), then recurse into both children and return their sum.

---

## 4. Why Lazy Propagation is Brilliant

Consider updating indices `[0, 999]` in an array of 1000 elements. Without laziness, we'd have to visit and update ~1000 leaf nodes. With lazy propagation, we identify a small number of `O(log n)` nodes that **fully cover** the range and update only those, deferring the rest. The deferred work is only done on demand when a future query forces us to look inside a tagged segment.

---

## 5. Edge Cases Handled

* **Point update**: A range update `[i, i]` on a single element — fully supported.
* **Full array query**: `query(0, n-1)` — returns `tree[0]` immediately (full overlap).
* **Overlapping updates**: Multiple consecutive range updates are composed correctly because `lazy[node]` accumulates all pending additions.
* **Out-of-bounds**: `update` and `query` raise `IndexError` for invalid ranges.
