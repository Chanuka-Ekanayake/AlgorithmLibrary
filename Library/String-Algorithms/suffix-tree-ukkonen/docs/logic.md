# Suffix Tree - Ukkonen's Algorithm

## 1. Overview

A **Suffix Tree** is a compressed Trie of all the suffixes of a given string. It's one of the most fundamental data structures in string processing, allowing many complex string problems to be solved in linear time. 

**Ukkonen's Algorithm** is an online algorithm that constructs the Suffix Tree for a string of length $N$ in $O(N)$ time and space.

### Key Concepts

- **Compressed Edges**: To save space, each edge stores a pair of indices $(start, end)$ to the original text instead of the actual characters.
- **Suffix Links**: Used to navigate between nodes in $O(1)$ during construction, avoiding re-calculation of already processed suffixes.
- **Active Point**: Represents the current position in the tree where the next character should be inserted. Defined by `(active_node, active_edge, active_length)`.
- **Remaining**: Keeps track of how many suffixes need to be explicitly added in the current phase.

---

## 2. Construction Rules

1.  **Rule 1 (Extension of a Leaf)**: When adding a new character, all leaves automatically extend. This is implemented using a global `current_end` pointer that increment in each phase.
2.  **Rule 2 (Split an Edge)**: When the character being added doesn't exist on the current edge, we split the edge into an internal node and a new leaf.
3.  **Rule 3 (Early Termination)**: If the character already exists on the edge, we simply increment the `active_length` and move to the next phase, as all subsequent suffixes in this phase will also already be in the tree.

---

## 3. Applications

- **Substring Search**: Find if pattern $P$ is in $T$ in $O(|P|)$ time.
- **Longest Repeated Substring**: Find by looking for the internal node with the maximum string depth.
- **Longest Common Substring**: By building a generalized suffix tree of multiple strings.
- **Palindrome Finding**: Linear time algorithms using suffix trees.
- **DNA Sequencing**: Used in mapping short reads to a reference genome.
