from typing import List


class WaveletTree:
    """
    Wavelet Tree — a succinct range query data structure.

    Built over a static integer array, the Wavelet Tree answers the following
    queries in O(log(max_value)) time each:

    1. kth_smallest(l, r, k)  — the k-th smallest element in arr[l..r]
    2. count_less_than(l, r, x) — how many elements in arr[l..r] are < x
    3. range_frequency(l, r, x) — how many times x appears in arr[l..r]

    Real-world use case: A streaming analytics platform processes millions of
    sensor readings. At any moment, an operator can ask:
      • "What is the median reading between sensor #100 and sensor #500?"
      • "How many readings in that window exceeded the threshold value 80?"
      • "How often did sensor #200 to #300 report exactly 42°C?"
    The Wavelet Tree answers all of these in O(log V) per query, where V is
    the value range — making it vastly faster than sorting on every query.

    Structure:
        The tree is built recursively over the value range [lo, hi].
        At each level, elements ≤ mid go to the LEFT child, elements > mid
        go to the RIGHT child. A prefix-count array records, for each position
        i, how many of the first i elements went LEFT at this node. This lets
        us translate [l, r] index ranges through every level in O(1).

    Constraints:
        - The array is static (built once, read many times).
        - All values must be non-negative integers.
        - Best suited for dense integer ranges; for very sparse values,
          coordinate compression is applied automatically.
    """

    # ------------------------------------------------------------------
    # Inner node — each node covers a value sub-range [lo, hi]
    # ------------------------------------------------------------------

    class _Node:
        """
        One level of the Wavelet Tree, covering value range [lo, hi].

        Attributes:
            lo:     The minimum value handled by this node (inclusive).
            hi:     The maximum value handled by this node (inclusive).
            left:   Left child node (values ≤ mid).
            right:  Right child node (values > mid).
            b:      Prefix-left-count array of length n+1.
                    b[i] = number of elements among the first i elements
                           (indices 0..i-1 in this node's sequence) that
                           went LEFT (i.e., value ≤ mid).
        """

        __slots__ = ("lo", "hi", "left", "right", "b")

        def __init__(self, lo: int, hi: int) -> None:
            self.lo: int = lo
            self.hi: int = hi
            self.left: "WaveletTree._Node | None" = None
            self.right: "WaveletTree._Node | None" = None
            self.b: List[int] = []  # length = len(arr_slice) + 1

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self, arr: List[int]) -> None:
        """
        Builds the Wavelet Tree from the input array.

        Time Complexity:  O(n log V)  where V = max_value - min_value + 1
        Space Complexity: O(n log V)

        Args:
            arr: A list of non-negative integers. Must be non-empty.

        Raises:
            ValueError: If arr is empty.
        """
        if not arr:
            raise ValueError("WaveletTree requires a non-empty array.")

        # --- Coordinate compression -----------------------------------
        # Map the actual values to a compact range [0, num_unique - 1].
        # This ensures the tree depth is O(log(num_unique_values)), not
        # O(log(max_value)), making it efficient even for large integers.
        sorted_unique = sorted(set(arr))
        self._rank: List[int] = sorted_unique          # rank → original value
        self._compress: dict = {v: i for i, v in enumerate(sorted_unique)}

        compressed = [self._compress[v] for v in arr]
        self.n: int = len(arr)

        # Build the tree over the compressed range
        self._root = self._build(compressed, 0, len(sorted_unique) - 1)

    def _build(self, arr: List[int], lo: int, hi: int) -> "_Node":
        """
        Recursively builds a Wavelet Tree node for value range [lo, hi].

        At each node we record a prefix-left-count array b[], then
        partition arr into left_arr (values ≤ mid) and right_arr (values > mid)
        and recurse.

        Args:
            arr: The sub-sequence of (compressed) values at this level.
            lo:  Lower bound of the value range.
            hi:  Upper bound of the value range.

        Returns:
            The constructed _Node for this level.
        """
        node = self._Node(lo, hi)

        if lo == hi:
            # Leaf — all elements here have the same value; b is trivially
            # just [0, 1, 2, ..., len(arr)].
            node.b = list(range(len(arr) + 1))
            return node

        mid = (lo + hi) // 2

        # Build prefix-left counts and partition arr in a single pass ------
        left_arr: List[int] = []
        right_arr: List[int] = []
        b = [0] * (len(arr) + 1)

        for i, val in enumerate(arr):
            if val <= mid:
                b[i + 1] = b[i] + 1
                left_arr.append(val)
            else:
                b[i + 1] = b[i]
                right_arr.append(val)

        node.b = b

        # Recurse into children only if they would be non-empty
        if left_arr:
            node.left = self._build(left_arr, lo, mid)
        if right_arr:
            node.right = self._build(right_arr, mid + 1, hi)

        return node

    # ------------------------------------------------------------------
    # Private helpers — translate index ranges across tree levels
    # ------------------------------------------------------------------

    def _left_count(self, node: "_Node", l: int, r: int) -> int:
        """
        Returns how many elements in positions [l, r] went LEFT at `node`.
        This is a constant-time lookup into the prefix array.

        Args:
            node: The current tree node.
            l:    Left boundary (0-indexed, inclusive).
            r:    Right boundary (0-indexed, inclusive).

        Returns:
            Number of elements in [l, r] that are ≤ mid at this level.
        """
        return node.b[r + 1] - node.b[l]

    def _translate_left(self, node: "_Node", l: int, r: int):
        """
        Returns the new (l, r) range for the LEFT child of `node`.

        The left child receives only elements that went left, so we map
        original positions through the prefix-left-count array.

        Returns:
            Tuple (new_l, new_r) in left child's index space.
        """
        # node.b[l] elements among [0, l-1] went left →
        # position l maps to node.b[l] in the left child
        new_l = node.b[l]
        new_r = node.b[r + 1] - 1
        return new_l, new_r

    def _translate_right(self, node: "_Node", l: int, r: int):
        """
        Returns the new (l, r) range for the RIGHT child of `node`.

        Right child receives elements that went right. Among [0, l-1],
        (l - node.b[l]) went right, shifting the index.

        Returns:
            Tuple (new_l, new_r) in right child's index space.
        """
        # Total elements going right before position l
        right_offset_l = l - node.b[l]
        right_offset_r = (r + 1) - node.b[r + 1]
        new_l = right_offset_l
        new_r = right_offset_r - 1
        return new_l, new_r

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def kth_smallest(self, l: int, r: int, k: int) -> int:
        """
        Returns the k-th smallest element in arr[l..r] (1-indexed).

        At each tree level, we count how many elements in [l, r] went LEFT
        (i.e., have value ≤ mid). If that count ≥ k, the answer must be in
        the left subtree; otherwise it's in the right subtree and we subtract
        the left count from k.

        Time Complexity: O(log V) per query.

        Args:
            l: Left index of the range (0-indexed, inclusive).
            r: Right index of the range (0-indexed, inclusive).
            k: The rank to find (1-indexed; k=1 is the minimum).

        Returns:
            The actual (decompressed) k-th smallest value.

        Raises:
            IndexError: If l, r are out of bounds or k is out of [1, r-l+1].
        """
        self._validate_range(l, r)
        if not (1 <= k <= r - l + 1):
            raise IndexError(
                f"k={k} is out of range for sub-array of length {r - l + 1}."
            )

        node = self._root
        while node.lo < node.hi:
            left_cnt = self._left_count(node, l, r)
            if k <= left_cnt:
                # Answer is in the left half
                l, r = self._translate_left(node, l, r)
                node = node.left
            else:
                # Answer is in the right half; reduce k by left count
                k -= left_cnt
                l, r = self._translate_right(node, l, r)
                node = node.right

        # node.lo == node.hi — we've arrived at the exact (compressed) value
        return self._rank[node.lo]

    def count_less_than(self, l: int, r: int, x: int) -> int:
        """
        Returns the number of elements in arr[l..r] that are strictly less
        than x.

        We descend the tree: whenever the entire right half is ≥ x, we move
        entirely left; otherwise we split.

        Time Complexity: O(log V) per query.

        Args:
            l: Left index of the range (0-indexed, inclusive).
            r: Right index of the range (0-indexed, inclusive).
            x: The threshold value (compared against original array values).

        Returns:
            Count of elements e in arr[l..r] where e < x.

        Raises:
            IndexError: If l or r are out of bounds.
        """
        self._validate_range(l, r)

        # Coordinate-compress x: find how many unique values are < x
        # (i.e., the compressed rank of x within our value universe)
        x_compressed = self._compress_threshold(x)
        if x_compressed == 0:
            return 0  # No value in the array is < x

        node = self._root
        count = 0

        while node is not None and node.lo < node.hi:
            mid = (node.lo + node.hi) // 2
            left_cnt = self._left_count(node, l, r)

            if x_compressed <= mid:
                # x falls in the left half — move left, right side doesn't contribute
                l, r = self._translate_left(node, l, r)
                node = node.left
            else:
                # All left-half elements are < x — count them, then descend right
                count += left_cnt
                l, r = self._translate_right(node, l, r)
                node = node.right

        # If node is a leaf (lo == hi), check if that leaf value < x
        if node is not None and node.lo < x_compressed:
            count += r - l + 1

        return count

    def range_frequency(self, l: int, r: int, x: int) -> int:
        """
        Returns the number of times x appears in arr[l..r].

        Uses count_less_than on x and x+1; the difference gives the count
        of x specifically.

        Time Complexity: O(log V) per query.

        Args:
            l: Left index of the range (0-indexed, inclusive).
            r: Right index of the range (0-indexed, inclusive).
            x: The value to count.

        Returns:
            Number of occurrences of x in arr[l..r].

        Raises:
            IndexError: If l or r are out of bounds.
        """
        self._validate_range(l, r)
        return self.count_less_than(l, r, x + 1) - self.count_less_than(l, r, x)

    def range_median(self, l: int, r: int) -> int:
        """
        Returns the lower median of arr[l..r].

        The lower median is the ⌈(r-l+2)/2⌉-th smallest element.
        For even-length ranges this returns the lower of the two middle values.

        Time Complexity: O(log V).

        Args:
            l: Left index of the range (0-indexed, inclusive).
            r: Right index of the range (0-indexed, inclusive).

        Returns:
            The median value in arr[l..r].

        Raises:
            IndexError: If l or r are out of bounds.
        """
        self._validate_range(l, r)
        length = r - l + 1
        k = (length + 1) // 2
        return self.kth_smallest(l, r, k)

    # ------------------------------------------------------------------
    # Private validation and compression helpers
    # ------------------------------------------------------------------

    def _validate_range(self, l: int, r: int) -> None:
        """Raises IndexError if the range [l, r] is invalid."""
        if l < 0 or r >= self.n or l > r:
            raise IndexError(
                f"Range [{l}, {r}] is invalid for array of size {self.n}."
            )

    def _compress_threshold(self, x: int) -> int:
        """
        Returns the compressed rank of x in our value universe.
        Specifically, returns the number of unique values in the array
        that are strictly less than x — which equals the compressed
        coordinate that x would occupy if it were in the array.

        This is computed via binary search over self._rank.
        """
        lo, hi = 0, len(self._rank)
        while lo < hi:
            mid = (lo + hi) // 2
            if self._rank[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        return lo
