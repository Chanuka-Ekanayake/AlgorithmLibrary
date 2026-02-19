# Locality-Sensitive Hashing (LSH)

## 1. Overview

**Locality-Sensitive Hashing (LSH)** is a probabilistic algorithm used for high-speed similarity search in high-dimensional spaces. Unlike cryptographic hashes (like SHA-256) which are designed to minimize collisions, LSH is specifically engineered so that similar items have a high probability of colliding into the same "bucket."

In your software marketplace, LSH serves as the core of a recommendation engine. When a user explores an ML model, LSH allows the system to find "Near Neighbors" (similar models) across a database of millions in constant or sub-linear time, bypassing the bottleneck of exhaustive comparisons.

---

## 2. Technical Features

- **Sub-linear Search Time:** Drastically reduces the search space by only comparing the query against a small "candidate set" found within a specific hash bucket.
- **Dimensionality Reduction:** Compresses high-dimensional vectors (e.g., 512D embeddings) into compact binary "signatures" while preserving their relative angular distances.
- **Cosine Similarity Alignment:** Our implementation uses **Random Projections** (SimHash), which is mathematically tied to the cosine distance between vectors.
- **Probabilistic Accuracy:** Offers a configurable trade-off between speed and precision. By adjusting the number of projections, you can control the "S-Curve" of collision probability.

---

## 3. Architecture

```text
.
├── core/                  # Probabilistic Search Engine
│   ├── __init__.py        # Package initialization
│   └── lsh.py             # Random projections & bucket management
├── docs/                  # Technical Documentation
│   ├── logic.md           # The geometry of dot-product signatures
│   └── complexity.md      # Analysis of sub-linear retrieval & space
├── test-project/          # Similar Model Finder
│   ├── app.py             # Large-scale simulation with 1,000+ vectors
│   └── instructions.md    # Guide for environment setup & benchmarking
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric                | Specification                                      |
| --------------------- | -------------------------------------------------- |
| **Search Complexity** | (where is # of projections)                        |
| **Space Complexity**  |                                                    |
| **Indexing Speed**    | Instantaneous ( per item)                          |
| **Similarity Metric** | Cosine Similarity (Angular)                        |
| **Ideal For**         | Recommendations, Duplicate Detection, Image Search |

---

## 5. Deployment & Usage

### Integration

The `RandomProjectionLSH` module can be integrated into your marketplace's recommendation pipeline to find similar model embeddings:

```python
from core.lsh import RandomProjectionLSH

# Initialize for 128-dimensional vectors with 12 bit-planes
lsh = RandomProjectionLSH(dimensions=128, num_projections=12)

# Index your models
lsh.add_item("model_v1_resnet", resnet_vector)
lsh.add_item("model_v2_vit", vit_vector)

# Query for similar items
candidates = lsh.query(search_query_vector)
print(f"Candidate similar models: {candidates}")

```

### Running the Simulator

To witness LSH filtering 1,000 models down to a few high-probability candidates in real-time:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Install the requirement:

```bash
pip install numpy

```

3. Run the simulator:

```bash
python app.py

```

---

## 6. Industrial Applications

- **Recommendation Engines:** "Customers who viewed this item also viewed..." systems.
- **Duplicate Detection:** Identifying near-duplicate documents, images, or code snippets in massive datasets.
- **Vector Databases:** The indexing foundation for AI-powered search (FAISS, Milvus).
- **Content Identification:** Fast matching of audio or video fingerprints (e.g., music recognition).

[How LSH Random Projection works in search](https://www.youtube.com/watch?v=8bOrMqEdfiQ)

This video explains the mechanics of using random hyperplanes to partition vector space, which is the exact "fence" logic we implemented in our core module.
