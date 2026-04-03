# Aho-Corasick Algorithm

The Aho-Corasick string matching algorithm is a highly efficient dictionary-matching algorithm that locates elements of a finite set of strings (the "dictionary") within an input text. It matches all patterns simultaneously, making it exceptionally fast when searching a large text against many patterns.

The algorithm constructs a finite state machine (specifically, a trie with additional "failure" links) that resembles a DFA (Deterministic Finite Automaton). These failure links allow fast transitions between failed string matches (e.g., if a search for "ab" fails, it gracefully falls back to check "b" rather than starting over).

> **Related implementation:** This repository also includes another Aho-Corasick implementation in [`Library/String-Algorithms/aho-corasick-multi-pattern-matcher/`](../aho-corasick-multi-pattern-matcher/). This directory documents the implementation described below; if you are comparing alternatives in the repo, review the other directory as well to choose the API/features/intended usage that best matches your needs.
## Folder Structure

- `core/`: Contains the Python implementation of the Aho-Corasick Algorithm.
- `docs/`: Contains detailed explanations of the algorithm's internal logic and space/time complexities.
- `test-project/`: Contains an interactive test application to visualize and test the algorithm in a real-world scenario.
