# Complexity

| Operation | Complexity | Explanation |
|---|---|---|
| Build | $O(n)$ | One DFS to compute subtree sizes and one decomposition pass to assign positions. |
| Path Query | $O(\log^2 n)$ | A path is split into at most $O(\log n)$ chain segments and each segment query is $O(\log n)$. |
| Path Update | $O(\log^2 n)$ | Same chain traversal as path query, but with range updates. |
| Subtree Query | $O(\log n)$ | Each subtree is contiguous in the flattened order. |
| Subtree Update | $O(\log n)$ | One range update on the subtree interval. |
| Space | $O(n)$ | Arrays for the decomposition plus a lazy segment tree. |
