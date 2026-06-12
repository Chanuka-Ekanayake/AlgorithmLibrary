# Complexity Analysis & Trade-offs

This document compares the computational efficiency and memory footprints of the most common rate limiting algorithms.

---

## 1. Complexity Comparison Table

Let $N$ be the limit (maximum allowed requests) and $U$ be the number of active users/clients.

| Algorithm | Time Complexity (Check) | Space Complexity (Per User) | Memory Footprint (High Scale) | Strict Boundary Protection | Allows Burst Traffic |
| --- | --- | --- | --- | --- | --- |
| **Fixed Window Counter** | $O(1)$ | $O(1)$ | Low | No (double limit at boundary) | No |
| **Sliding Window Log** | $O(\log N)$ or $O(N)$ | $O(N)$ | Very High (stores timestamps) | Yes | No |
| **Sliding Window Counter** (Weighted) | $O(1)$ | $O(1)$ | Low (stores two integers) | Yes (Approximated) | No |
| **Token Bucket** | $O(1)$ | $O(1)$ | Low | Yes | Yes (Burst capacity) |

---

## 2. Mathematical Trade-offs & Approximations

The **Weighted Sliding Window Counter** is an approximation algorithm. 

### Accuracy vs. Performance
* **The Approximation Error:** The algorithm assumes that request rates are distributed uniformly within the previous fixed window. If a user spikes all their requests in the last second of the previous window, the weighted average assumes they occurred evenly across the entire previous window.
* **Why it's accepted in production:** In practice, the error rate is mathematically bounded to be under $5\%$ (specifically, it never under-limits by more than $5\%$ under worst-case non-uniform distributions). The massive savings in memory ($O(1)$ vs $O(N)$) make it the preferred choice for massive-scale API gateways like Cloudflare and various Redis plugins.

### Comparison to Token Bucket
* **Token Bucket** is optimized for traffic shaping: it allows burst capacity up to the bucket size, and then limits requests strictly to the refill rate.
* **Sliding Window Counter** is optimized for strict window limit compliance: it ensures that the rate over any sliding interval is kept under the limit, avoiding sudden traffic bursts that could crash downstream services.
