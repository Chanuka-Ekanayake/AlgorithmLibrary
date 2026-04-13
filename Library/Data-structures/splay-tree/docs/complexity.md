# Splay Tree Complexity Analysis

## Time Complexity

| Operation | Best | Average | Worst | Amortized |
|-----------|------|---------|-------|-----------|
| Search    | O(1) | O(log n)| O(n)  | O(log n)  |
| Insert    | O(1) | O(log n)| O(n)  | O(log n)  |
| Delete    | O(1) | O(log n)| O(n)  | O(log n)  |

## Explanation

### Best Case: O(1)
- Element is root (already splayed)
- No rotation needed
- Example: searching for the most recently accessed element

### Worst Case: O(n)
- Linear chain structure (e.g., inserting sorted keys)
- Single operation can require O(n) rotations
- Example: accessing the deepest node in an unbalanced tree

### Amortized: O(log n) ✓
The key property of splay trees: **any sequence of m operations takes O(m log n) time**.

**Proof Sketch (Potential Function Analysis):**
- Define potential Φ = Σ rank(v) where rank(v) = log(size of subtree rooted at v)
- Splay operation increases potential by at most 3 * log(n)
- Cost of operation = actual cost + ΔΦ = O(log n) amortized

### Real-World Performance
Splay trees excel when:
- **Temporal locality** exists (recent accesses likely to be accessed again)
- **Access patterns are skewed** (80/20 rule)
- **Cache locality matters** (root near CPU cache after splay)

Example: Accessing element A repeatedly
```
Before: A is at depth 5 → O(5) cost
After:  A is at root    → O(1) cost next time
```

## Space Complexity

| Metric | Complexity |
|--------|-----------|
| Storage | O(n) |
| Pointers | O(n) |
| Height (worst) | O(n) |
| Height (amortized) | O(log n) |

## Comparison with Other Trees

| Property | Splay Tree | Red-Black | Treap | AVL |
|----------|-----------|-----------|--------|-----|
| **Worst-case height** | O(n) | O(log n) | O(n) | O(log n) |
| **Amortized cost** | O(log n) | O(log n) | O(log n)* | - |
| **Balance invariant** | None | Color | Priority | Height |
| **Optimal for skewed access** | ✓ Yes | No | No | No |
| **Cache-friendly** | ✓ Excellent | Good | Good | Fair |
| **Practical speed** | Very fast | Fast | Fast | Balanced |
| **Complexity proof** | Potential | Counting | Probability | Counting |

*Treap uses randomization; splay uses deterministic splaying

## Operation Cost Breakdown

### Single Splay Cost
- **Rotations needed:** O(log n) in average case, O(n) in worst case
- **Per rotation:** O(1)
- **Total splay cost:** O(depth of node)

### Amortized Cost Analysis

For a sequence of operations:
- Operations on root: O(1) each
- Operations on deep nodes: expensive initially, but amortized across future splays

**Example scenario:**
```
Insert 1, 2, 3, 4, 5 into initially empty tree

Sequence:
Insert 1:     Tree: 1           Cost: O(1)
Insert 2:     Tree: 2-1         Cost: O(1) + O(1) splay = O(1)
Insert 3:     Tree: 3-2-1       Cost: O(1) + O(2) splay = O(1)
Insert 4:     Tree: 4-3-2-1     Cost: O(1) + O(3) splay = O(1)
Insert 5:     Tree: 5-4-3-2-1   Cost: O(1) + O(4) splay = O(1)

Total: O(1+1+1+1+1) = O(5) = O(n) for inserts of n elements
Amortized: O(log n) when divided by optimal access patterns
```

## Why Splay Trees Beat Alternatives

1. **Better than AVL/RBT for skewed workloads**
   - AVL/RBT: Every access is O(log n) regardless
   - Splay: Frequently accessed elements approach O(1)

2. **Simpler than AVL (fewer rotations)**
   - AVL: Height/balance-factor maintenance required
   - Splay: Just rotate to root

3. **No randomness like Treap**
   - Deterministic behavior
   - No random seed management
   - Better for embedded/systems code

4. **Cache efficiency**
   - Root is accessed most → stays in L1 cache
   - Reduces memory latency vs. scattered BST access

## Practical Recommendation

**Use Splay Trees when:**
- ✓ Access patterns are skewed (hot/cold data)
- ✓ Temporal locality is high (recent = likely)
- ✓ You need competitive performance for real workloads
- ✓ Simplicity and code size matter

**Use Red-Black Trees when:**
- ✓ Worst-case latency guarantees needed (real-time systems)
- ✓ Access patterns are uniform
- ✓ You need Linux kernel stability

**Use Treaps when:**
- ✓ You want randomized balance
- ✓ Concurrent insertions without central coordination
