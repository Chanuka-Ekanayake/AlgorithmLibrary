# Treap Complexity

## Algorithmic Properties
A Treap achieves balancing purely on probabilistic properties.

## Time Complexity
- **Time Complexity Expected:**
  - **Search:** $O(\log n)$
  - **Insert:** $O(\log n)$
  - **Delete:** $O(\log n)$

- **Time Complexity Worst-Case (Math Bound):**
  - **Search:** $O(n)$
  - **Insert:** $O(n)$
  - **Delete:** $O(n)$

*Wait! Why $O(n)$?*
A treap's performance relies heavily on random variables structuring the hierarchy evenly. The worst-case computational timeline arises only when randomly assigned priorities cause elements to degrade into a skewed linear linked list (e.g., sequentially larger keys mysteriously drawing exponentially smaller random constraints). Because priorities are strictly randomized uniformly, the probability of encountering structurally skewed layouts scales to insignificance when dealing with larger $n$. Expected time remains strictly pinned against logarithmic margins.

## Space Complexity
- **Overall Space Complexity:** $O(n)$, where $n$ is the number of nodes stored in the treap.
- **Call-Stack Depth:** Both insertion and deletion use recursion up to the tree height $h$. In expectation, $h = O(\log n)$, giving expected auxiliary stack space $O(\log n)$, but in the worst case a highly skewed treap can have $h = O(n)$.
