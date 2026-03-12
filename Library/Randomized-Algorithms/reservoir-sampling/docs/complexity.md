# Complexity Analysis: Reservoir Sampling

Reservoir Sampling is highly efficient for large-scale data processing because it avoids storing the entire data set.

---

## 1. Time Complexity

| Step | Complexity | Description |
|---|---|---|
| Initialization | **$O(k)$** | Filling the reservoir with the first $k$ items. |
| Processing Stream | **$O(n - k)$** | Iterating through the rest of the stream. |
| Random Generation | **$O(1)$** | Per item, one random integer is generated. |
| **Total** | **$O(n)$** | The algorithm visits each item exactly once. |

### Note on Optimization
While Algorithm R is $O(n)$, generating a random number for *every* item can be slow for very large $n$. Advanced versions like **Algorithm L** improve performance by calculating "skip distances" (how many items to skip before the next replacement), reducing random number generation to $O(k \log(n/k))$.

---

## 2. Space Complexity

| Component | Complexity | Description |
|---|---|---|
| Reservoir | **$O(k)$** | Stores $k$ items to return at the end. |
| Metadata | **$O(1)$** | One counter to track the current index. |
| Total | **$O(k)$** | Does **not** depend on the stream size $n$. |

This makes the algorithm "online" and suitable for systems with strictly limited memory.

---

## 3. Comparison with Simple Random Sampling

| Feature | Simple Random Sampling | Reservoir Sampling |
|---|---|---|
| Know $n$ beforehand? | **Yes** | **No** |
| Passes over data | 1 (if $n$ known) | 1 |
| Memory usage | $O(n)$ (usually) | **$O(k)$** |
| Efficiency | High | Extreme for streams |

---

## 4. Engineering Trade-offs

-   **Randomness Quality:** The algorithm's fairness depends entirely on the quality of the Pseudo-Random Number Generator (PRNG).
-   **Parallelism:** Reservoir Sampling is naturally sequential. To parallelize, you can sample $k$ items from different chunks of the stream and then "merge" them using **Weighted Reservoir Sampling**, but this is more complex.
-   **Streaming State:** Using a generator/stateful object is preferred in production to avoid holding the stream connection open while processing.
