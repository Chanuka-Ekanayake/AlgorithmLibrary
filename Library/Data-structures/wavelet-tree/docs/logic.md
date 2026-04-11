# Algorithm Logic: Wavelet Tree

## 1. The Core Concept

A **Wavelet Tree** is a succinct binary tree built over an array of integers. Unlike a Segment Tree (which indexes by *position*) or a Binary Search Tree (which indexes by *value*), the Wavelet Tree indexes by **both** simultaneously — enabling powerful range queries that neither structure can answer efficiently alone.

The key insight: recursively *split elements by value at the median*, while remembering which elements went left and which went right at each level.

---

## 2. Building the Tree — O(n log V)

Let `V` be the number of distinct values (after coordinate compression).

### 2.1 Coordinate Compression

Before building, all values are remapped to `[0, V-1]` using a sorted unique-value table. This keeps the tree depth at `O(log V)` regardless of the actual integer magnitudes.

```
Original: [15, 3, 7, 3, 15, 7, 7]
Unique:   [3, 7, 15]  → ranks {3→0, 7→1, 15→2}
Compressed: [2, 0, 1, 0, 2, 1, 1]
```

### 2.2 Recursive Split

At each node covering value range `[lo, hi]`:

1. Compute `mid = (lo + hi) / 2`.
2. Scan the array left-to-right:
   - If `value ≤ mid` → send to **left** child.
   - If `value > mid` → send to **right** child.
3. Build a **prefix-left-count array `b[]`**:
   - `b[i]` = how many of the first `i` elements went LEFT.
   - `b` has length `len(array) + 1` with `b[0] = 0`.

```
Node covers values [0, 2], mid = 1
Array at this level: [2, 0, 1, 0, 2, 1, 1]
Goes left (≤1):       N  Y  Y  Y  N  Y  Y
Prefix left count b: [0, 0, 1, 2, 3, 3, 4, 5]
Left child gets:  [0, 1, 0, 1, 1]
Right child gets: [2, 2]
```

4. Recurse into left sub-range `[lo, mid]` and right sub-range `[mid+1, hi]`.

The tree has height `O(log V)` and each level stores `n` prefix entries, giving **O(n log V)** total space.

---

## 3. Index Translation Between Levels — O(1)

The `b[]` array at each node is the key to translating index ranges down the tree in constant time:

**Going LEFT** (elements that satisfy `value ≤ mid`):
```
new_l = b[l]
new_r = b[r + 1] - 1
```

**Going RIGHT** (elements that satisfy `value > mid`):
```
new_l = l - b[l]
new_r = (r + 1) - b[r + 1] - 1
```

This is because `b[i]` tells us exactly how many elements in positions `[0, i-1]` went left — so the offset into the left (or right) child is directly readable.

---

## 4. Queries — O(log V) Each

### 4.1 k-th Smallest in Range `[l, r]`

Walk from root to a leaf:

1. At node `[lo, hi]`, count `left_cnt = b[r+1] - b[l]` (elements in `[l,r]` that went left).
2. If `k ≤ left_cnt` → the answer is in the left subtree; translate `[l, r]` to left child space.
3. Else → the answer is in the right subtree; subtract `left_cnt` from `k`, translate to right child space.
4. At a leaf (`lo == hi`), the current compressed value IS the answer → decompress.

```
Example: arr = [3, 1, 2, 1, 3], k-th smallest in [0,4], k=3
Compressed: [2,0,1,0,2], range [0,2]=0
Step 1 (root, [0,2] mid=1): left_cnt=3, k=3≤3 → go left, k stays 3
Step 2 ([0,1] mid=0): Subarray [0,1,1], left_cnt=2, k=3>2 → go right, k=1
Step 3 ([1,1] leaf): answer = rank[1] = 2
```

### 4.2 Count Elements Less Than `x` in Range `[l, r]`

Walk the tree, accumulating a count:

- If `x ≤ mid + 1` → all right-side answers are ≥ x, go left.
- If `x > mid + 1` → all left-side values are < x, add `left_cnt` to count, go right.

The threshold `x` is coordinate-compressed first (binary search in `O(log V)`).

### 4.3 Range Frequency of Value `x`

```
count(x in [l,r]) = count_less_than(l, r, x+1) - count_less_than(l, r, x)
```

Two `O(log V)` queries → `O(log V)` total.

### 4.4 Median

```
range_median(l, r) = kth_smallest(l, r, (r - l + 2) // 2)
```

---

## 5. Edge Cases Handled

| Case | Handling |
|---|---|
| All elements identical | Tree has depth 1 (single leaf after compression) |
| k = 1 | Returns the minimum of the range — traverses to leftmost leaf |
| k = r − l + 1 | Returns the maximum of the range — traverses to rightmost leaf |
| x not in array | `range_frequency` correctly returns 0 |
| x < all values | `count_less_than` correctly returns 0 |
| x > all values | `count_less_than` correctly returns r − l + 1 |
| Empty subarray | Caught by `_validate_range` before any tree traversal |
