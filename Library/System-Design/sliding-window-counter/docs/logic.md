# Sliding Window Counter Logic & Mechanics

The **Sliding Window Counter** rate limiter checks the request rate within a rolling time window (e.g., the last 60 seconds). Unlike a fixed-window limiter (which resets suddenly at boundaries), it provides a smooth, strict limitation on request rate.

---

## 1. Mathematical Formulation: Weighted Estimate

A standard **Sliding Window Log** stores the timestamp of every single request in a queue. To check limits, it pops old timestamps and counts the remaining items. This requires $O(\text{Limit})$ memory per user, which can easily exhaust database RAM if rates are high.

The **Sliding Window Counter** approximates the count in the sliding window using a **Weighted Estimate** from the previous and current fixed windows. This requires only **two counters** (previous window count and current window count), reducing space complexity to $O(1)$.

```text
|<---- Previous Window (W) ---->|<----- Current Window (W) ----->|
[========== 40 requests ========][======== 10 requests ==========]
                                 ^
                                 |--- Current Time (elapsed: 15s into current window)
```

At current time $T$:
1. Let $W$ be the window size (e.g., 60 seconds).
2. Let $t_{\text{curr}}$ be the elapsed time since the current fixed window began (e.g., 15 seconds).
3. The previous window's contribution decays as time advances. The weight of the previous window is:
   $$\text{weight} = \frac{W - t_{\text{curr}}}{W} = \frac{60 - 15}{60} = 0.75$$
4. The estimated request count in the last 60 seconds is:
   $$\text{Estimated Count} = (\text{Count}_{\text{prev}} \times \text{weight}) + \text{Count}_{\text{curr}}$$
   $$\text{Estimated Count} = (40 \times 0.75) + 10 = 30 + 10 = 40$$

If this estimated count is less than the rate limit, the request is allowed and `Count_curr` is incremented.

---

## 2. Lazy Window Rotation

To avoid background tick threads, the rate limiter uses a **lazy rotation** strategy. Every time a request arrives:
1. It computes `elapsed = now - current_window_start`.
2. If `elapsed >= window_size`:
   * If `elapsed` is within two window lengths, the current window's count is copied to the previous window's count.
   * If more time has elapsed, the previous count is reset to `0`.
   * The current count is reset to `0`.
   * The start time is advanced by the number of completed window sizes to align with the current interval boundary.
3. This guarantees that window rotation is handled dynamically at RAM speed with zero thread overhead when idle.
