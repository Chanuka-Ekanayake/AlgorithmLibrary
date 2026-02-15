# Complexity Analysis: Count-Min Sketch (CMS)

The Count-Min Sketch is a probabilistic structure used for frequency estimation in high-volume data streams. Its complexity is defined by the **error bound** () and the **confidence** ().

## 1. Time Complexity

| Operation            | Complexity | Description                                                                         |
| -------------------- | ---------- | ----------------------------------------------------------------------------------- |
| **`add(item)`**      |            | Each addition requires hash calculations and increment operations (where is depth). |
| **`estimate(item)`** |            | Retrieval requires hash calculations and finding the minimum of counter values.     |

### 1.1 Stream Performance

Since (depth) is typically a small constant (e.g., 5 to 10), the time complexity is effectively \*\*\*\* per event. This makes the CMS capable of processing millions of events per second on standard 2026 hardware.

---

## 2. Space Complexity

The space complexity of a Count-Min Sketch is:

- ** (Error Bound):** Determines the width of the matrix ().
- ** (Confidence Bound):** Determines the depth of the matrix ().

### 2.1 Fixed Memory Footprint

Unlike a Hash Map, which grows linearly with the number of unique items (), the CMS has ** space relative to **. Once the matrix size is set, it never grows, regardless of how many billions of items pass through the stream.

---

## 3. Accuracy & The "Min" Logic

The CMS is a **biased estimator**, but the bias is one-sided:

1. **Never Under-estimates:** The estimated count is always greater than or equal to the actual frequency ().
2. **Probability of Over-estimation:** The error in the estimate is at most with a probability of .

### Why use the Minimum?

Every hash collision adds "noise" to a counter. By using multiple independent hash functions (depth), we spread this noise. The probability that an item collides with "heavy hitters" in **all** rows is extremely low. Taking the minimum effectively filters out the most significant collision errors.

---

## 4. Comparison: CMS vs. Exact Counting

| Feature           | Standard Frequency Map        | Count-Min Sketch         |
| ----------------- | ----------------------------- | ------------------------ |
| **Accuracy**      | 100% Exact                    | Approximate              |
| **Memory**        | (Grows with unique items)     | (Fixed size)             |
| **Throughput**    | High (but slows as RAM fills) | Constant High            |
| **Item Recovery** | Possible to list all items    | Impossible (Sketch only) |

---

## 5. Engineering Trade-offs

- **The "Heavy Hitter" Advantage:** CMS is most accurate for high-frequency items. In your marketplace, this means it will perfectly identify the "Viral" models, even if it slightly over-counts the "Long Tail" (obscure models).
- **Collision Saturation:** If the matrix is too small ( is too large) and the stream is massive, the counters will eventually saturate with noise. Choosing the right `width` is the most critical design decision.
