# Complexity Analysis: Longest Increasing Subsequence (LIS)

The LIS problem is a classic example of how the choice of data structure directly dictates performance limits. By maintaining a sorted auxiliary array, we can bypass the need to cross-reference every previously seen element.

## 1. Time Complexity

| Algorithm                            | Complexity | Bottleneck                                                                                                             |
| ------------------------------------ | ---------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Classic DP**                       |            | The nested loop structure requires comparing the current element to every single preceding element.                    |
| **Patience Sorting (Binary Search)** | \*\*\*\*   | Bypasses the inner loop by performing a binary search () on the actively maintained `tails` array for each element (). |

### The Mathematical Advantage

In the classic DP approach, the number of operations follows an arithmetic progression: , which simplifies to , cementing it firmly in territory.

In the optimal approach, we iterate through the array exactly once. At each step, we execute a binary search over an array that is, at most, size . The worst-case scenario mathematically becomes .

---

## 2. Space Complexity

| Algorithm         | Complexity | Description                                                                                                   |
| ----------------- | ---------- | ------------------------------------------------------------------------------------------------------------- |
| **Classic DP**    |            | Requires a `dp` array of size to store subsequence lengths, plus a `parent` array of size for reconstruction. |
| **Binary Search** |            | Requires a `tails_indices` array of up to size , plus the `parent` array of size for reconstruction.          |

**Space Efficiency Parity:**
Both algorithms require strict auxiliary space. The optimization from to in time complexity does **not** come at the cost of increased memory usage. This is why the Binary Search method is unilaterally preferred in production.

---

## 3. Computational Scaling (The Real-World Impact)

To understand why this optimization is critical for a marketplace or data-mining platform (e.g., analyzing daily stock prices over decades), consider how the operations scale as the dataset grows:

| Dataset Size () | Classic DP Operations ()             | Optimal Operations ()           |
| --------------- | ------------------------------------ | ------------------------------- |
| 1,000           | 1,000,000                            | ~10,000                         |
| 10,000          | 100,000,000                          | ~132,000                        |
| 100,000         | 10,000,000,000                       | ~1,660,000                      |
| **1,000,000**   | **1,000,000,000,000** (Server hangs) | **~20,000,000** (Instantaneous) |

---

## 4. Engineering Constraints

- **Strictly Increasing Requirement:** This implementation specifically looks for _strictly_ increasing values. If duplicates are allowed (non-decreasing subsequence), the binary search condition must be adjusted from `bisect_left` to `bisect_right` logic.
- **Array Reconstruction Overhead:** Returning just the integer _length_ of the LIS is simpler and slightly faster. Tracking the `parent` array to reconstruct the exact path adds minor overhead but keeps the overall complexity within bounds while vastly increasing utility.
