# Algorithm Logic: Aho-Corasick Multi-Pattern Matching

## 1. The Problem with Repeated Single-Pattern Search

Suppose you are building a **network intrusion-detection system (IDS)**. A packet of N bytes must be scanned against a dictionary of K known attack signatures, each of average length L. Running a single-pattern algorithm like KMP once per signature costs **O(K × N)** time per packet. On a gigabit network, K can be tens of thousands and packets arrive thousands of times per second — this approach is simply too slow.

Aho-Corasick solves this by scanning the text **exactly once**, detecting all K patterns simultaneously in **O(N + Z)** time, where Z is the total number of matches.

---

## 2. Phase 1 — Trie Construction: Building the Prefix Tree

The first step is inserting every pattern into a **trie** (prefix tree).

- Each node represents a prefix shared by one or more patterns.
- Each edge is labelled with a character.
- Nodes at the end of a pattern are **marked** with the pattern's identity.

### Example

Patterns: `["he", "she", "his", "hers"]`

```
root
├── h ──── e* ("he")
│          └── r ──── s* ("hers")
├── s ──── h ──── e* ("she")
└── h ──── i ──── s* ("his")
```

*(Node marked with `*` signals a completed pattern.)*

Construction visits every character of every pattern exactly once: **O(M)** where M = total pattern length.

---

## 3. Phase 2 — Failure Link BFS: Converting the Trie to a DFA

A trie alone is not enough. After a mismatch, a naive approach would restart from the root, potentially missing overlapping matches. The key insight of Aho & Corasick (1975) is the **failure link**.

### What Is a Failure Link?

The **failure link** of node `v` points to the node representing the **longest proper suffix** of `v`'s path-label that is also a **valid prefix** in the trie.

For the example above (patterns: `he`, `she`, `his`, `hers`):

| Node path | Failure link points to |
|-----------|------------------------|
| `root`    | `root` (by definition) |
| `h`       | `root`                 |
| `s`       | `root`                 |
| `he`      | `root` (no suffix of "he" is a trie prefix, except empty) |
| `sh`      | `h`    ("h" is a suffix of "sh" and a trie prefix)        |
| `she`     | `he`   ("he" is a suffix of "she" and a trie prefix)      |
| `his`     | `root`                 |
| `her`     | `root`                 |
| `hers`    | `root`                 |

### BFS Construction

Failure links are computed level-by-level using **Breadth-First Search**:

1. All depth-1 children of root get `fail = root`.
2. For a node `v` reached from parent `p` via character `c`:
   - Walk up `p`'s failure-link chain until a node has a child labelled `c`, or you reach root.
   - `fail(v)` = that child node (or root if none found).
3. **Output link inheritance**: when `fail(v)` has output (i.e., a pattern ends there), copy those outputs into `v.output`. This ensures the search phase only needs to inspect `node.output` — it never needs to chase the failure-link chain during search.

Time: **O(M)** — every node is visited exactly once in the BFS.

---

## 4. Phase 3 — Text Search: One Pass, All Patterns

With the automaton ready, scanning a text of length N is a **single left-to-right pass**:

```
node ← root
for each character c at position i in text:
    while node ≠ root and c not in node.children:
        node ← node.fail          # follow failure link
    if c in node.children:
        node ← node.children[c]
    for each (pattern_idx, pattern) in node.output:
        report match at (i - len(pattern) + 1, i + 1)
```

### Why This Is O(N)

The `while` loop might look expensive, but because `fail` links always move to a **strictly shallower** node, the total number of upward jumps across the entire text is bounded by the total number of downward steps — which is at most N. Amortised over the full text, each character costs **O(1)**.

### Walkthrough: Searching "ushers" for `["he", "she", "his", "hers"]`

| i | char | state  | output (end pos i)  |
|---|------|--------|---------------------|
| 0 | `u`  | root   | —                   |
| 1 | `s`  | `s`    | —                   |
| 2 | `h`  | `sh`   | —                   |
| 3 | `e`  | `she`  | `"she"` [1:4], `"he"` [2:4] (inherited from fail(`she`) = `he`) |
| 4 | `r`  | `her`  | —                   |
| 5 | `s`  | `hers` | `"hers"` [2:6]      |

Three matches found in a single O(N) pass — no restarts, no redundant comparisons.

---

## 5. Output Link (Dictionary Link)

The **output link** is a critical optimisation: at construction time, each node inherits the `output` list of its failure-link node. Without this, finding all matches at a given position would require traversing the failure-link chain at search time — potentially O(depth) per character. With it, we simply read `node.output` once per character: **O(Z)** total for all match reporting.

---

## 6. Why Aho-Corasick Outperforms Alternatives

| Approach              | Preprocessing   | Search per text |
|-----------------------|-----------------|-----------------|
| Naive (K × brute)     | O(1)            | O(K × N × L)   |
| K × KMP               | O(K × L)        | O(K × N)        |
| K × Rabin-Karp        | O(K × L)        | O(K × N) avg   |
| **Aho-Corasick**      | **O(M)**        | **O(N + Z)**    |

For K = 10,000 patterns and N = 1,000,000 bytes, Aho-Corasick is **~10,000× faster** in the search phase.

---

## 7. System Relevance

When the Snort IDS inspects a network packet against 60,000+ signatures, it uses an Aho-Corasick automaton. Building the automaton once at startup and streaming each packet through it once gives **microsecond-per-packet** scan times that would be physically impossible with per-pattern KMP.
