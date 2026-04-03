# Aho-Corasick Algorithm Complexity

Let $Z$ be the sum of the lengths of all patterns in the dictionary, and let $N$ be the length of the input text to search. Let $M$ be the number of matches found.

### Time Complexity

**Trie Construction:** $O(Z)$
- Inserting each pattern takes time proportional to its length. We do this for all patterns.

**Failure Links Construction:** $O(Z)$
- Computing failure links involves a Breadth-First Search (BFS) over the states. Because we have at most $Z$ states, and for each state we might traverse failure links, you might wonder if it takes longer. However, amortized analysis shows that the depth inside the trie bounds the total number of failure links we can traverse. The time to build all failure links is linearly bounded by the number of nodes in the Trie, which is at most $Z + 1$.

**Searching:** $O(N + M)$
- Traversing the input text of length $N$ takes $O(N)$ time. Although we sometimes follow multiple failure links per character, each failure link strictly decreases the depth in the trie, while each successful character match increases the depth by exactly 1.
- Collecting matches at each step takes time proportional to the number of matches $M$. 

**Total Time Complexity:** $O(Z + N + M)$

### Space / Subroutine Complexity

- **Space Complexity:** $O(Z \times |\Sigma|)$, where $|\Sigma|$ is the size of the alphabet. Each node in the trie can have up to $|\Sigma|$ transitions. We also store failure links and output links which require $O(Z)$ space. If implemented using dictionaries for transitions instead of fixed-sized arrays, the space becomes $O(Z)$, effectively reducing overhead for large alphabets.
