# Complexity Analysis: Circuit Breaker Pattern

The Circuit Breaker is a behavioral pattern used to manage service reliability. Its complexity is evaluated based on the computational overhead it adds to each service call and its impact on system-wide latency.

## 1. Time Complexity

| Operation             | Complexity | Description                                                                                       |
| --------------------- | ---------- | ------------------------------------------------------------------------------------------------- |
| **Call Wrapping**     | `O(1)`     | Checking the current state (`OPEN`, `CLOSED`, or `HALF_OPEN`) is a constant time operation.       |
| **State Transition**  | `O(1)`     | Updating failure counters and timestamps happens in constant time after the service call returns. |
| **Fail-Fast Trigger** | `O(1)`     | When the circuit is `OPEN`, the rejection happens instantly, bypassing the network entirely.      |

### 1.1 Impact on Latency

- **Healthy State (`CLOSED`):** Adds negligible latency (nanoseconds) to check the state and increment a counter.
- **Failure State (`OPEN`):** **Decreases** overall system latency. By failing fast, it prevents the application from waiting for network timeouts (which can be several seconds or more).

---

## 2. Space Complexity

The space complexity per Circuit Breaker instance is **O(1)**:

Regardless of the number of requests processed, the memory footprint remains constant. We only store:

- The current state (Enum)
- A failure counter (Integer)
- A timestamp for the last failure (Float)
- Threshold configurations (Integers/Floats)

---

## 3. Reliability Metrics

In reliability engineering, the Circuit Breaker improves the **MTTR (Mean Time To Recovery)** and **Availability** of the system:

| Metric                  | With Circuit Breaker   | Without Circuit Breaker         |
| ----------------------- | ---------------------- | ------------------------------- |
| **Cascading Risk**      | Near Zero              | High                            |
| **Resource Exhaustion** | Prevented              | Likely (Thread pool saturation) |
| **User Experience**     | Instant "Service Busy" | Frustrating "Infinite Loading"  |
| **Self-Healing**        | Automatic              | Manual / Restart Required       |

---

## 4. Engineering Trade-offs

- **Granularity:** A single breaker for the whole API is simple but "heavy-handed." A breaker per endpoint (e.g., `/get-price` vs `/checkout`) is more complex to manage but provides better availability.
- **Threshold Tuning:**
  - **Too Low:** Leads to "False Tripping" during minor network blips.
  - **Too High:** Allows too many failures to hit the system, potentially causing the very crash it was meant to prevent.

- **Half-Open Sensitivity:** The recovery logic assumes that a single successful call in `HALF_OPEN` means the system is healthy. In some 2026 architectures, a "Success Percentage" is used instead for higher confidence.
