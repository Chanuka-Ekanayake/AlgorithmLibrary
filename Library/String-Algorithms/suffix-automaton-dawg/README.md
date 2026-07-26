# Suffix Automaton (Directed Acyclic Word Graph - DAWG)

A Suffix Automaton (also known as a Directed Acyclic Word Graph or DAWG) is a powerful data structure that represents all substrings of a given string in a highly compressed form. It is extremely efficient for tasks such as finding the longest common substring of multiple strings, counting the number of occurrences of a pattern, and finding the first occurrence of a pattern.

## Overview

A suffix automaton for a string $S$ of length $n$ is a finite state automaton that accepts all suffixes of $S$. Remarkably, it can be constructed in linear time $O(n)$ and requires linear space $O(n|\Sigma|)$ or $O(n \log|\Sigma|)$ depending on the implementation of the transition map. The size of the automaton is bounded by $2n - 1$ states and $3n - 4$ transitions.

## Features
*   **Linear Time Construction:** Builds the automaton in time proportional to the length of the string.
*   **Substring Search:** Can check if a pattern is a substring of the original string in time proportional to the length of the pattern $O(|P|)$, independent of the length of the original string.
*   **Highly Compressed:** Efficient representation using at most $2n - 1$ states.

## Complexity
- **Time Complexity (Build):** $O(n)$
- **Time Complexity (Search):** $O(|P|)$ where $P$ is the pattern to search.
- **Space Complexity:** $O(n \times |\Sigma|)$ where $\Sigma$ is the alphabet size.
