from typing import List


class SegmentTree:
    """
    Segment Tree with Lazy Propagation.

    Supports efficient range sum queries and range update operations
    (add a value to all elements in a range) in O(log n) time.

    Real-world use case: Stock price range analysis — query the total
    traded volume over any date range, and apply bulk adjustments
    (e.g., stock splits, corrections) to ranges of dates instantly.
    """

    def __init__(self, data: List[int]):
        """
        Builds the segment tree from an input list.
        Time Complexity: O(n)
        Space Complexity: O(n)

        Args:
            data: The initial array to build the tree from.
        """
        self.n = len(data)
        # tree[i] holds the segment sum for node i
        self.tree: List[int] = [0] * (4 * self.n)
        # lazy[i] holds the pending (deferred) update for node i's subtree
        self.lazy: List[int] = [0] * (4 * self.n)
        if self.n > 0:
            self._build(data, 0, 0, self.n - 1)

    # -------------------------------------------------------------------------
    # Private: Build
    # -------------------------------------------------------------------------

    def _build(self, data: List[int], node: int, start: int, end: int) -> None:
        """Recursively builds the segment tree from the input array."""
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            self._build(data, left_child, start, mid)
            self._build(data, right_child, mid + 1, end)
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

    # -------------------------------------------------------------------------
    # Private: Lazy Propagation Helper
    # -------------------------------------------------------------------------

    def _push_down(self, node: int, start: int, end: int) -> None:
        """
        Pushes a pending lazy update from a parent node down to its children.
        This is called before we recurse into a node's children.
        """
        if self.lazy[node] != 0:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            left_len = mid - start + 1
            right_len = end - mid

            # Apply the lazy update to the left child
            self.tree[left_child] += self.lazy[node] * left_len
            self.lazy[left_child] += self.lazy[node]

            # Apply the lazy update to the right child
            self.tree[right_child] += self.lazy[node] * right_len
            self.lazy[right_child] += self.lazy[node]

            # Clear the lazy tag on the current node — it's been pushed down
            self.lazy[node] = 0

    # -------------------------------------------------------------------------
    # Private: Range Update
    # -------------------------------------------------------------------------

    def _update_range(
        self, node: int, start: int, end: int, l: int, r: int, val: int
    ) -> None:
        """
        Adds `val` to every element in the index range [l, r].

        Args:
            node:  Current tree node index.
            start: Left boundary of the current node's segment.
            end:   Right boundary of the current node's segment.
            l:     Left boundary of the target range (0-indexed).
            r:     Right boundary of the target range (0-indexed).
            val:   The value to add to each element in [l, r].
        """
        if r < start or end < l:
            # Completely outside — do nothing
            return

        if l <= start and end <= r:
            # Completely inside — apply update and tag for later propagation
            self.tree[node] += val * (end - start + 1)
            self.lazy[node] += val
            return

        # Partially overlapping — push pending updates down first, then recurse
        self._push_down(node, start, end)
        mid = (start + end) // 2
        self._update_range(2 * node + 1, start, mid, l, r, val)
        self._update_range(2 * node + 2, mid + 1, end, l, r, val)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    # -------------------------------------------------------------------------
    # Private: Range Query
    # -------------------------------------------------------------------------

    def _query_range(
        self, node: int, start: int, end: int, l: int, r: int
    ) -> int:
        """
        Returns the sum of elements in the index range [l, r].

        Args:
            node:  Current tree node index.
            start: Left boundary of the current node's segment.
            end:   Right boundary of the current node's segment.
            l:     Left boundary of the query range (0-indexed).
            r:     Right boundary of the query range (0-indexed).

        Returns:
            The sum of elements in [l, r].
        """
        if r < start or end < l:
            # Completely outside — contributes 0
            return 0

        if l <= start and end <= r:
            # Completely inside — return the stored sum
            return self.tree[node]

        # Partially overlapping — push down lazy, then recurse
        self._push_down(node, start, end)
        mid = (start + end) // 2
        left_sum = self._query_range(2 * node + 1, start, mid, l, r)
        right_sum = self._query_range(2 * node + 2, mid + 1, end, l, r)
        return left_sum + right_sum

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def update(self, l: int, r: int, val: int) -> None:
        """
        Adds `val` to every element in the array between index l and r (inclusive).
        Time Complexity: O(log n)

        Args:
            l:   Left index of the range (0-indexed).
            r:   Right index of the range (0-indexed).
            val: The value to add to each element in [l, r].

        Raises:
            IndexError: If l or r are out of bounds.
        """
        if l < 0 or r >= self.n or l > r:
            raise IndexError(
                f"Range [{l}, {r}] is invalid for array of size {self.n}."
            )
        self._update_range(0, 0, self.n - 1, l, r, val)

    def query(self, l: int, r: int) -> int:
        """
        Returns the sum of elements between index l and r (inclusive).
        Time Complexity: O(log n)

        Args:
            l: Left index of the range (0-indexed).
            r: Right index of the range (0-indexed).

        Returns:
            The integer sum of elements in [l, r].

        Raises:
            IndexError: If l or r are out of bounds.
        """
        if l < 0 or r >= self.n or l > r:
            raise IndexError(
                f"Range [{l}, {r}] is invalid for array of size {self.n}."
            )
        return self._query_range(0, 0, self.n - 1, l, r)

    def point_update(self, index: int, val: int) -> None:
        """
        Adds `val` to the single element at the given index.
        This is a special case of update(index, index, val).
        Time Complexity: O(log n)

        Args:
            index: The 0-indexed position to update.
            val:   The value to add.
        """
        self.update(index, index, val)

    def point_query(self, index: int) -> int:
        """
        Returns the current value at a single index.
        This is a special case of query(index, index).
        Time Complexity: O(log n)

        Args:
            index: The 0-indexed position to query.

        Returns:
            The current integer value at that index.
        """
        return self.query(index, index)
