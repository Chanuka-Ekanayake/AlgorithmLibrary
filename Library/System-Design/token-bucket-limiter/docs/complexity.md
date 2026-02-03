# Complexity Analysis: Token Bucket Rate Limiter

The Token Bucket algorithm is designed to balance system protection with user experience by allowing traffic bursts while maintaining a strict long-term average rate.

## 1. Time Complexity

| Operation          | Complexity | Description                                                         |
| ------------------ | ---------- | ------------------------------------------------------------------- |
| **`consume()`**    |            | Lazy refill and token subtraction are basic arithmetic operations.  |
| **`_refill()`**    |            | A simple time-delta calculation regardless of the elapsed duration. |
| **`is_allowed()`** |            | Hash map lookup for the user's bucket followed by consumption.      |

### 1.1 Efficiency of Lazy Refill

Instead of running a background thread that wakes up every second to add tokens (which would consume CPU cycles even when no one is using the API), our implementation uses **Lazy Evaluation**:

- Tokens are only recalculated when a request actually arrives.
- This ensures that idle users consume **zero CPU time**.

---

## 2. Space Complexity

The space complexity is:

Where \***\* is the number of **Unique Identifiers\*\* (Users/IPs) currently being tracked.

### 2.1 Memory Footprint

- **Per User:** We store a small object containing two floats (tokens, timestamp) and one lock.
- **Storage Requirement:** Approximately **~100-200 bytes per user**.
- **Scaling:** Tracking 100,000 active users requires roughly 20MB of RAM, making it highly efficient for local memory or distributed stores like Redis.

---

## 3. Comparison with Other Limiters

| Algorithm          | Complexity | Burst Support | Best Use Case                                     |
| ------------------ | ---------- | ------------- | ------------------------------------------------- |
| **Token Bucket**   |            | **Yes**       | General Purpose APIs (AWS/Stripe style).          |
| **Leaky Bucket**   |            | No            | Traffic shaping/smoothing for network packets.    |
| **Fixed Window**   |            | No            | Simple, low-precision limits.                     |
| **Sliding Window** |            | Yes           | High-precision requirements with low user volume. |

---

## 4. Mathematical Model

The replenishment follows a linear growth function until it hits the ceiling ():

This ensures that regardless of whether the last request was 1 second or 1 year ago, the calculation remains a single-step operation ().

---

## 5. Engineering Trade-offs

- **Lock Contention:** In high-concurrency environments, multiple threads hitting the same user's bucket will wait on the `threading.Lock`. For massive scale, this logic is often moved to **Redis Lua scripts** to offload the atomic operations.
- **Precision vs. Drift:** The use of `time.monotonic()` prevents "time drift" caused by system clock updates (NTP), ensuring the rate limit remains accurate over long uptimes.
