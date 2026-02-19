# Complexity Analysis: Locality-Sensitive Hashing (LSH)

Locality-Sensitive Hashing is an **Approximate Nearest Neighbor (ANN)** algorithm. Its goal is to provide sub-linear search time by trading a small amount of accuracy for massive gains in performance.

## 1. Time Complexity

| Operation                 | Complexity | Description                                                            |
| ------------------------- | ---------- | ---------------------------------------------------------------------- |
| **Indexing (`add_item`)** |            | Projecting a vector of dimension onto random planes.                   |
| **Signature Generation**  |            | The same dot-product operations used to find the "bucket" for a query. |
| **Search (Retrieval)**    |            | Where is the number of items in the resulting bucket. Ideally, .       |

### The "Linear-to-Sublinear" Shift

In a standard search, you must perform comparisons. In LSH, you perform projections and then check only the items that collided in your bucket. This reduces the search time from \***\* to effectively ** or \*\* depending on bucket distribution.

---

## 2. Space Complexity

The space complexity is \*\*\*\*:

- **:** Storing a -bit signature for every item in your database.
- **:** Storing the random hyperplanes (the "fences") used for projection.

---

## 3. Accuracy & The "S-Curve"

LSH performance is defined by two types of errors:

1. **False Positives:** Two dissimilar items end up in the same bucket.

- _Solution:_ Increase (number of planes) to make the "signature" more specific.

2. **False Negatives:** Two similar items end up in different buckets (they "missed" a collision).

- _Solution:_ Use **Multiple Tables** (OR-amplification). By hashing the item into 5 different LSH tables, you only need it to collide in **one** of them to find it.

---

## 4. Engineering Trade-offs

- **The Dimensionality Curse:** As the dimension increases, LSH remains stable, whereas tree-based search (like KD-Trees) degrades into linear scans.
- **Memory vs. Recall:** Adding more hash tables increases the "Recall" (chance of finding the neighbor) but multiplies your memory usage.
- **Static vs. Dynamic:** While adding items is , changing the number of projections () requires re-indexing the entire database.
