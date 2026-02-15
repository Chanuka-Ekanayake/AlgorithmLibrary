# Count-Min Sketch (CMS)

## 1. Overview

The **Count-Min Sketch** is a probabilistic data structure that functions as a frequency table for massive data streams. In high-velocity environments, tracking the exact frequency of every unique item (e.g., millions of different software downloads or IP addresses) in a standard hash map is impossible due to linear memory growth.

CMS solves this by using a fixed-size sketching matrix. It provides a conservative frequency estimate with a mathematically proven error bound, using a memory footprint that is **orders of magnitude smaller** than traditional dictionaries.

---

## 2. Technical Features

* **Sub-linear Space Complexity:** The memory usage is determined by your desired accuracy, not by the number of unique items () in the stream.
* **One-Sided Error:** The algorithm provides a "conservative" estimate. It may over-estimate due to hash collisions, but it will **never under-estimate** the true frequency.
* **Point-Query Efficiency:** Both updates and frequency lookups are performed in constant time (), regardless of the billions of events processed.
* **Mergeable Structure (Conceptual):** In principle, multiple compatible sketches from different servers can be combined (summed) to provide a global frequency view in a distributed architecture; the reference `CountMinSketch` implementation in this repository does not yet expose a merge/addition API.

---

## 3. Architecture

```text
.
├── core/                  # Probabilistic Counter Engine
│   ├── __init__.py        # Package initialization
│   └── cms.py             # Matrix management and Min-Query logic
├── docs/                  # Technical Documentation
│   ├── logic.md           # Multi-hash collision and filtering theory
│   └── complexity.md      # Analysis of error bounds and fixed space
├── test-project/          # Trending Model Tracker
│   ├── app.py             # Real-time frequency audit vs. Python Counter
│   └── instructions.md    # Guide for testing "Heavy Hitter" accuracy
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric | Specification |
| --- | --- |
| **Space Complexity** |  relative to stream size |
| **Update Latency** | Ultra-Low (Constant  hashes) |
| **Error Bound** |  |
| **Confidence** |  (typically 99%+) |
| **Ideal For** | Top-K elements, Trending topics, DDoS detection |

---

## 5. Deployment & Usage

### Integration

The `CountMinSketch` is ideal for tracking viral content or monitoring for traffic anomalies:

```python
from core.cms import CountMinSketch

# Initialize with Width=2000 and Depth=5
cms = CountMinSketch(width=2000, depth=5)

# Process a stream of events
for model_id in live_download_stream:
    cms.add(model_id)

# Estimate the frequency of a specific item
count = cms.estimate("Model_X_v2")
print(f"Estimated Downloads: {count}")

```

### Running the Simulator

To see the CMS identify trending ML models in a stream of 100,000 downloads using only a few kilobytes of RAM:

1. Navigate to the `test-project` directory:
```bash
cd test-project

```


2. Run the Trending Tracker:
```bash
python app.py

```



---

## 6. Industrial Applications

* **Trending Topics:** Identifying "Heavy Hitters" in social media or news feeds (e.g., Twitter/X Trends).
* **Network Security:** Monitoring for source-destination pairs that exceed safe request thresholds (DDoS detection).
* **Database Query Planning:** Estimating join sizes and column distribution to optimize SQL execution.
* **AdTech:** Tracking frequency caps for users across massive advertising networks.