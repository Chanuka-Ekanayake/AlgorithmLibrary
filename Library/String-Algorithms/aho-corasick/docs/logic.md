# Aho-Corasick Algorithm Logic

The Aho-Corasick algorithm is designed for fast multiple-pattern matching. It combines a Trie structure with ideas from the Knuth-Morris-Pratt (KMP) string search algorithm. 

The main aspects of the algorithm involve:
1. **Trie Construction:** Building a standard Trie from the dictionary of words to search for.
2. **Failure Links Construction:** Finding maximum length proper suffixes that are also prefixes in the trie.
3. **Searching:** Traversing the trie given an input string, utilizing failure links upon mismatch.

### 1. Trie Construction (Goto Function)

The algorithm begins by constructing a Trie from the set of patterns.
- Starting from a root node, we insert each word character by character.
- If a path for character `c` exists, we follow it; otherwise, we create a new state (node).
- The final node of each pattern contains an output marking it as a match for that specific pattern.

### 2. Failure Links Construction (Failure Function)

This is the core of Aho-Corasick, computed using a Breadth-First Search (BFS).
- The failure link for a state `u` points to another state `v` which represents the longest proper suffix of the string represented by `u` that is also a prefix of some pattern in the Trie.
- Nodes at depth 1 (directly connected to the root) naturally fail to the root.
- For nodes at greater depths:
  - If a transition `Trie[u][char]` exists to `next_state`, we examine the failure link of `u` (let's call it `fail_u`).
  - We look for a transition labeled `char` from `fail_u`. If it exists, the failure link for `next_state` is `Trie[fail_u][char]`.
  - If it doesn't exist, we follow `fail_u`'s failure link repeatedly until we find a match or hit the root.
- **Dictionary Links / Output Merging:** When setting the failure link for a state to `v`, we also copy the output items from `v` to the current state. This handles inner substring matches gracefully (e.g., if we matched "she", we also matched "he", so the node for "she" inherits "he"'s output).

### 3. Searching Text

Given an input string of length $O(N)$:
- Begin at the root state.
- For each character in the string:
  - Try to transition down the Trie using the current character.
  - If no direct transition exists, follow the failure link repeatedly until a transition is found or the root is reached.
  - Check the output list at the resulting state. If it is non-empty, we have found matches ending at the current character position in the text.
