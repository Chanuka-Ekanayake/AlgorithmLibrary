"""
Aho-Corasick Multi-Pattern Matching Algorithm

Builds a finite-state string-matching automaton from a set of patterns in
O(M) time (M = total length of all patterns), then searches a text of length
N reporting every match position in O(N + Z) time (Z = total number of
matches).  This is optimal: you cannot do better than reading each character
of the text once and reporting each match once.

The implementation follows three distinct phases:
  1. Trie construction  — inserts every pattern into a prefix tree.
  2. Failure-link BFS   — builds the automaton's failure (fallback) links.
  3. Text search        — streams the text through the automaton collecting
                          all match positions in a single left-to-right pass.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional, Tuple


class _TrieNode:
    """
    A single node in the Aho-Corasick trie / automaton.

    Attributes:
        children  : Map from character to child node.
        fail      : Failure link — the longest proper suffix of the path to
                    this node that is also a prefix of some pattern.
        output    : List of (pattern_index, pattern) pairs that end at this
                    node, including those inherited through the output links.
        depth     : Depth of this node in the trie (root = 0).
    """

    __slots__ = ("children", "fail", "output", "depth")

    def __init__(self, depth: int = 0) -> None:
        self.children: Dict[str, _TrieNode] = {}
        self.fail: Optional[_TrieNode] = None
        self.output: List[Tuple[int, str]] = []   # (pattern_index, pattern)
        self.depth: int = depth


class AhoCorasick:
    """
    Aho-Corasick multi-pattern string matching automaton.

    Build once with a list of patterns, then call ``search`` as many times
    as needed — each search is a single O(N) pass over the text.

    Example
    -------
    >>> ac = AhoCorasick(["he", "she", "his", "hers"])
    >>> matches = ac.search("ushers")
    >>> for start, end, pattern in matches:
    ...     print(f"  '{pattern}' at [{start}:{end}]")
    'she' at [1:4]
    'he'  at [2:4]
    'hers' at [2:6]

    Attributes
    ----------
    patterns  : Original list of patterns supplied at construction.
    """

    def __init__(self, patterns: List[str]) -> None:
        """
        Construct the Aho-Corasick automaton.

        Parameters
        ----------
        patterns : List of non-empty strings to search for.

        Raises
        ------
        ValueError : If ``patterns`` is empty or contains an empty string.
        """
        if not patterns:
            raise ValueError("At least one pattern must be provided.")
        for i, p in enumerate(patterns):
            if not p:
                raise ValueError(f"Pattern at index {i} is an empty string; "
                                 "empty patterns are not supported.")

        self.patterns: List[str] = list(patterns)
        self._root: _TrieNode = _TrieNode(depth=0)
        self._build_trie()
        self._build_failure_links()

    # ------------------------------------------------------------------
    # Phase 1 — Trie Construction: O(M)
    # ------------------------------------------------------------------

    def _build_trie(self) -> None:
        """
        Insert every pattern into the trie.

        Each character of each pattern follows (or creates) a trie edge.
        When the last character of pattern[i] is reached, that node is
        marked with (i, pattern[i]) so the search phase can recognise
        complete matches.

        Time  : O(M)  where M = sum of all pattern lengths.
        Space : O(M * Σ)  where Σ = alphabet size (bounded by the number
                           of distinct characters seen in patterns).
        """
        for idx, pattern in enumerate(self.patterns):
            node = self._root
            for char in pattern:
                if char not in node.children:
                    node.children[char] = _TrieNode(depth=node.depth + 1)
                node = node.children[char]
            # Mark this node as the end of pattern[idx]
            node.output.append((idx, pattern))

    # ------------------------------------------------------------------
    # Phase 2 — Failure-Link BFS: O(M)
    # ------------------------------------------------------------------

    def _build_failure_links(self) -> None:
        """
        Compute failure (fallback) links for every trie node via BFS.

        The failure link of a node v points to the node representing the
        longest proper suffix of v's path-label that is also a prefix of
        any pattern.  Building these links converts the trie into a
        Deterministic Finite Automaton (DFA) that can process the text
        without ever backing up.

        Algorithm (Aho & Corasick, 1975):
          - Root's children: their failure link = root.
          - For a node v reached from parent p via character c:
              fail(v) = goto(fail(p), c) if that transition exists,
                        root otherwise.
          - Output links: inherit all matches from the failure-link chain
            so the search phase only needs to inspect node.output.

        Time  : O(M)  — single BFS over all trie nodes.
        """
        queue: deque[_TrieNode] = deque()

        # Depth-1 nodes (direct children of root): failure link is root
        for child in self._root.children.values():
            child.fail = self._root
            queue.append(child)

        while queue:
            current = queue.popleft()

            for char, child in current.children.items():
                # Walk up the failure-link chain of 'current' until we find
                # a node that has a child labelled 'char', or we reach root.
                fail_node = current.fail
                while fail_node is not None and char not in fail_node.children:
                    fail_node = fail_node.fail
                child.fail = fail_node.children[char] if fail_node and char in fail_node.children else self._root

                # A node should not point to itself as its failure link
                if child.fail is child:
                    child.fail = self._root

                # Inherit output patterns from the failure-link node
                # so a single node.output lookup yields ALL matches here.
                child.output = child.output + child.fail.output

                queue.append(child)

    # ------------------------------------------------------------------
    # Phase 3 — Text Search: O(N + Z)
    # ------------------------------------------------------------------

    def search(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Search ``text`` for all occurrences of every pattern.

        Each character of the text transitions the automaton to the next
        state in O(1) amortised time.  Whenever a state carries output
        matches, the character position is used to recover the start index.

        Parameters
        ----------
        text : The string to search through.

        Returns
        -------
        List of ``(start, end, pattern)`` tuples in left-to-right order,
        where ``text[start:end] == pattern``.
        The list is sorted by ``end`` position, then by ``start`` position.

        Time  : O(N + Z)  where N = len(text), Z = number of matches.
        Space : O(Z)      for the returned results list.
        """
        results: List[Tuple[int, int, str]] = []
        node = self._root

        for i, char in enumerate(text):
            # Follow failure links until we find a valid transition or reach root
            while node is not self._root and char not in node.children:
                node = node.fail  # type: ignore[assignment]

            if char in node.children:
                node = node.children[char]

            # Collect all patterns that end at position i (inclusive)
            for _idx, pattern in node.output:
                start = i - len(pattern) + 1
                end = i + 1        # exclusive, matches Python slice convention
                results.append((start, end, pattern))

        # Sort by end position; break ties by start position (shortest first)
        results.sort(key=lambda t: (t[1], t[0]))
        return results

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def count_matches(self, text: str) -> int:
        """
        Return the total number of pattern occurrences in ``text``.

        Time: O(N + Z)
        """
        return len(self.search(text))

    def first_match(self, text: str) -> Optional[Tuple[int, int, str]]:
        """
        Return the first ``(start, end, pattern)`` match in ``text``,
        or ``None`` if no pattern is found.

        Time: O(N + Z)  — runs the full search; use ``search`` directly
        if you need all matches anyway.
        """
        results = self.search(text)
        return results[0] if results else None

    def contains_any(self, text: str) -> bool:
        """
        Return ``True`` if any pattern appears in ``text``.

        Short-circuits on the first match found.

        Time: O(N)  — stops at the first match.
        """
        node = self._root
        for char in text:
            while node is not self._root and char not in node.children:
                node = node.fail  # type: ignore[assignment]
            if char in node.children:
                node = node.children[char]
            if node.output:
                return True
        return False
