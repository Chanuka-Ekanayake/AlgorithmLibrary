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
- **Overall Space Complexity:** $O(n)$ where $n$ is tracked uniformly with allocated array states.
- **Call-Stack Depth:** Both Insertion and Deletion lean on recursive frames up to depth height $h$, giving average auxiliary overhead of $O(\log n)$, strictly bounded identically to memory requirements.
