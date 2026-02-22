"""
Suffix Array + LCP Array
Constructs the Suffix Array in O(N log N) using the prefix-doubling
(Manber & Myers) technique, then builds the LCP Array in O(N) using
Kasai's algorithm. Together they power O(M log N) substring search
(and O(N log N) construction), longest-repeated-substring detection,
and more.
"""

from typing import List, Tuple


class SuffixArray:
    """
    Builds and queries a Suffix Array with an accompanying LCP Array
    for a given input string.

    Attributes:
        text (str):        The original input string (sentinel '$' appended internally).
        sa   (List[int]):  Suffix Array — sa[i] is the starting index of the i-th
                           lexicographically smallest suffix.
        lcp  (List[int]):  LCP Array  — lcp[i] is the length of the longest common
                           prefix between sa[i-1] and sa[i] (lcp[0] = 0 by definition).
    """

    def __init__(self, text: str) -> None:
        # Append a sentinel character smaller than any printable character
        # so that every suffix is unique and the sort is unambiguous.
        self.original = text
        self.text = text + "$"
        self.sa = self._build_suffix_array()
        self.lcp = self._build_lcp_array()

    # ------------------------------------------------------------------
    # Phase 1 — Suffix Array Construction: O(N log N)
    # ------------------------------------------------------------------

    def _build_suffix_array(self) -> List[int]:
        """
        Constructs the Suffix Array using the Prefix-Doubling algorithm.

        The idea:
          - Round 0: rank each suffix by its first character alone.
          - Round k: sort suffixes by pairs of ranks from round k-1,
            effectively doubling the comparison window each iteration.
          - After ceil(log2 N) rounds every pair of ranks is unique,
            giving the final sorted order in O(N log N) total time.
        """
        s = self.text
        n = len(s)

        # Initial ranks based on character ordinal values
        sa = list(range(n))
        rank = [ord(c) for c in s]
        tmp = [0] * n

        gap = 1
        while gap < n:
            # Comparator: sort by (rank[i], rank[i+gap]) pairs
            def sort_key(i: int) -> Tuple[int, int]:
                return (rank[i], rank[i + gap] if i + gap < n else -1)

            sa.sort(key=sort_key)

            # Re-assign integer ranks based on sorted order
            tmp[sa[0]] = 0
            for i in range(1, n):
                prev, curr = sa[i - 1], sa[i]
                tmp[curr] = tmp[prev]
                if sort_key(curr) != sort_key(prev):
                    tmp[curr] += 1

            rank = tmp[:]
            if rank[sa[-1]] == n - 1:
                # All ranks are distinct; sorting is complete
                break
            gap <<= 1

        return sa

    # ------------------------------------------------------------------
    # Phase 2 — LCP Array Construction: O(N) — Kasai's Algorithm
    # ------------------------------------------------------------------

    def _build_lcp_array(self) -> List[int]:
        """
        Builds the LCP (Longest Common Prefix) array using Kasai's algorithm.

        Key insight:
          If suffix starting at position p has LCP = h with its predecessor
          in the suffix array, then the suffix starting at position p+1
          has LCP >= h-1 with *its* predecessor. This lets us process
          suffixes in text order and carry forward the LCP count,
          guaranteeing only O(N) character comparisons overall.
        """
        s = self.text
        n = len(s)
        sa = self.sa

        # Inverse suffix array: rank[i] = position of suffix i in sa
        rank = [0] * n
        for i, suf in enumerate(sa):
            rank[suf] = i

        lcp = [0] * n
        h = 0  # current LCP length carried forward

        for i in range(n):
            if rank[i] > 0:
                j = sa[rank[i] - 1]   # predecessor suffix in sorted order
                # Extend the common prefix
                while i + h < n and j + h < n and s[i + h] == s[j + h]:
                    h += 1
                lcp[rank[i]] = h
                # By Kasai's lemma, h can only decrease by 1 across iterations
                if h > 0:
                    h -= 1

        return lcp

    # ------------------------------------------------------------------
    # Query API
    # ------------------------------------------------------------------

    def search(self, pattern: str) -> List[int]:
        """
        Finds all starting positions of 'pattern' in the original text
        using binary search on the Suffix Array.

        Time Complexity: O(M log N)  where M = len(pattern), N = len(text)

        Returns:
            Sorted list of starting indices where the pattern occurs.
        """
        m = len(pattern)
        if m == 0:
            # For an empty pattern, return an empty list to avoid undefined
            # behavior in the binary search logic and to mirror the behavior
            # of other matchers (e.g., KMP) that handle this case explicitly.
            return []
        n = len(self.sa)

        def _compare(sa_idx: int) -> int:
            """Returns -1, 0, or +1 by comparing pattern against suffix[sa_idx]."""
            suffix = self.text[sa_idx: sa_idx + m]
            if suffix < pattern:
                return -1
            elif suffix > pattern:
                return 1
            return 0

        # Binary search for the left boundary
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if _compare(self.sa[mid]) < 0:
                lo = mid + 1
            else:
                hi = mid
        left = lo

        # Binary search for the right boundary
        lo, hi = left, n
        while lo < hi:
            mid = (lo + hi) // 2
            if _compare(self.sa[mid]) == 0:
                lo = mid + 1
            else:
                hi = mid
        right = lo

        return sorted(self.sa[i] for i in range(left, right))

    def longest_repeated_substring(self) -> str:
        """
        Returns the longest substring that appears at least twice.
        Uses the LCP array: the maximum LCP value gives the length.

        Time Complexity: O(N)
        """
        if not self.lcp:
            return ""
        max_lcp = max(self.lcp)
        if max_lcp == 0:
            return ""
        idx = self.lcp.index(max_lcp)
        return self.original[self.sa[idx]: self.sa[idx] + max_lcp]

    def longest_common_substring(self, other: str) -> str:
        """
        Returns the longest common substring between the original text
        and 'other' by concatenating them with a unique separator and
        building a joint suffix array.

        Time Complexity: O((N+M) log(N+M))
        """
        # Choose a separator character that does not appear in either string
        # to avoid corrupting the joint suffix array construction.
        separator = None
        for candidate in ("\0", "\x01", "\x02", "\x03", "\uFFFF"):
            if candidate not in self.original and candidate not in other:
                separator = candidate
                break
        if separator is None:
            raise ValueError("Unable to find a separator character not present in the input strings.")
        combined = self.original + separator + other
        joint = SuffixArray(combined)

        n = len(self.original)
        best_len = 0
        best_start = 0

        for i in range(1, len(joint.sa)):
            # LCP between consecutive suffixes in the joint array
            lcp_val = joint.lcp[i]
            prev_sa = joint.sa[i - 1]
            curr_sa = joint.sa[i]

            # One suffix must come from 'self' and the other from 'other'
            # to avoid counting a repeated substring within the same string
            in_original_prev = prev_sa < n
            in_original_curr = curr_sa < n

            if in_original_prev != in_original_curr and lcp_val > best_len:
                best_len = lcp_val
                best_start = curr_sa if in_original_curr else prev_sa

        return combined[best_start: best_start + best_len]
