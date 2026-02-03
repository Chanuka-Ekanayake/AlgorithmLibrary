# Algorithm Logic: Token Bucket (API Rate Limiting)

## 1. The Core Analogy

Imagine a physical bucket that holds "tokens."

- **The Refill:** Tokens are dropped into the bucket at a fixed, steady rate (e.g., 5 tokens per second).
- **The Capacity:** The bucket has a maximum size. If it's full, new tokens spill over and are lost.
- **The Request:** When a user makes an API request, they must "spend" a token from the bucket.
- **The Rejection:** If the bucket is empty, the request is rejected (typically with a `429 Too Many Requests` status).

---

## 2. Why Token Bucket? (The "Burst" Advantage)

Unlike the **Leaky Bucket** algorithm, which forces requests to leave at a strictly uniform rate, the **Token Bucket** allows for **burstiness**.

If a user hasn't made a request in a while, their bucket fills up to the maximum capacity. They can then spend all those tokens at once in a quick burst. This is much more representative of real-world internet usage, where a browser might need to fetch 10 small assets simultaneously after a period of inactivity.

---

## 3. The "Lazy Refill" Strategy

A naive implementation might use a background thread or a timer to add tokens every second. However, this is inefficient for systems with millions of users. Instead, we use **Lazy Refill**:

1. **Don't refill in the background.**
2. **Wait** until a request actually arrives.
3. **Calculate** the time difference since the last request.
4. **Add** tokens proportional to that time gap:

5. **Process** the request using the newly updated balance.

---

## 4. Logical Flow of a Request

When `is_allowed(user_id)` is called:

1. **Retrieve:** Find the bucket associated with the `user_id`.
2. **Synchronize:** Acquire a lock to ensure thread safety (crucial for multi-threaded web servers).
3. **Refill:** Run the "Lazy Refill" math to bring the token count up to date.
4. **Check:** \* **IF** : Subtract 1 token and return `True` (Allow).

- **ELSE**: Return `False` (Rate Limited).

5. **Release:** Unlock and return the result.

---

## 5. Industrial Application: API Tiering

In your 2026 software marketplace, this logic is used to enforce subscription tiers:

| Tier           | Capacity (Burst) | Refill Rate (Steady) | Use Case                |
| -------------- | ---------------- | -------------------- | ----------------------- |
| **Free**       | 5 Tokens         | 1 Token / Sec        | Casual Browsing         |
| **Pro**        | 50 Tokens        | 10 Tokens / Sec      | Heavy Data Retrieval    |
| **Enterprise** | 500 Tokens       | 100 Tokens / Sec     | Bulk ML Model Downloads |
