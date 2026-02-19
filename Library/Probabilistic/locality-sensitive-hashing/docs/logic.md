# Algorithm Logic: Locality-Sensitive Hashing (LSH)

## 1. The Paradox of Hashing

In a traditional hash map (like Python's `dict`), changing one bit in the input results in a completely different hash. This is called the "Avalanche Effect."

- **Standard Hash:** `hash("Model_A")` vs `hash("Model_A_v2")` No relationship.
- **LSH Hash:** `LSH("Model_A")` vs `LSH("Model_A_v2")` **High probability of the same hash.**

---

## 2. Random Projections (SimHash)

The core logic of our implementation uses **Random Projections** to approximate **Cosine Similarity**.

### The "Hyperplane" Fence

Imagine your high-dimensional vectors as points on a sphere. We place several random "fences" (hyperplanes) through the center of that sphere.

1. For every vector, we ask: "Which side of the fence are you on?"
2. If it's on the "Positive" side, we assign a bit `1`.
3. If it's on the "Negative" side, we assign a bit `0`.

### The Binary Signature

By using random planes, each vector gets a -bit signature (e.g., `1101`).

- Vectors that are physically close to each other in space are very likely to end up on the same side of most fences.
- Therefore, they will share the same binary signature.

---

## 3. The Dot Product Logic

Mathematically, we determine the "side of the fence" using the **Dot Product** between the data vector () and the random plane vector ():

Since the dot product is related to the angle between vectors, this logic naturally groups items with similar angular directions (Cosine Similarity).

---

## 4. Sub-linear Retrieval

The logic allows for near-instant search because of the **Bucketing Strategy**:

1. **Index Time:** We store every model ID in a hash table where the key is its binary signature.
2. **Query Time:** We generate the signature for our "Search Query" and go straight to that bucket in the hash table.
3. **Result:** We only compare our query against the few items in that specific bucket, ignoring 99% of the database.

---

## 5. Usage in the Marketplace

On your platform, LSH powers the **"Similar Models"** recommendation engine:

- **Vectorization:** Every model's weights or metadata is converted into a vector.
- **LSH Indexing:** These vectors are hashed into the LSH table.
- **Discovery:** When a user views a "Face Detection Model," the system queries the LSH bucket and finds other "Computer Vision" models instantly, even if you have millions of listings.
