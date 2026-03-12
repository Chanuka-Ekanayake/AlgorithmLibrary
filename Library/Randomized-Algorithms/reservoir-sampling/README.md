# Reservoir Sampling

## 1. Overview

**Reservoir Sampling** is an elegant randomized algorithm used to sample $k$ items from a stream of $n$ items, where $n$ is either unknown or too large to fit in memory. 

Unlike standard sampling, which requires knowing the total population size to assign a fixed probability to each item, Reservoir Sampling maintains a valid uniform sample at every step of the process. This makes it ideal for processing network logs, database streams, and live analytical data.

---

## 2. Technical Features

-   **Algorithm R:** Implements the classic single-pass sampling logic (Vitter, 1985).
-   **Guaranteed Uniformity:** Proven mathematical fairness — every item has exactly $k/n$ probability of selection.
-   **Streaming Interface:** Includes a generator-based stateful sampler (`streaming_sample`) for long-running processes.
-   **Memory Efficient:** Requires exactly $O(k)$ space regardless of the input stream length.
-   **Generic Types:** Supports sampling of any data type (objects, strings, numbers).

---

## 3. Architecture

```text
.
├── core/                   # Optimisation Engine
│   ├── __init__.py         # Package initialisation
│   └── reservoir.py        # Algorithm R and streaming logic
├── docs/                   # Technical Documentation
│   ├── logic.md            # Mathematical proof and pseudocode
│   └── complexity.md       # O(n) time and O(k) space analysis
├── test-project/           # Fairness Testing Simulator
│   ├── app.py              # Statistical validation and demo
│   └── instructions.md     # Experimentation guide
└── README.md               # Documentation Entry Point
```

---

## 4. Performance Specifications

| Metric | Specification |
|---|---|
| **Time Complexity** | $O(n)$ where $n$ is total items in stream |
| **Space Complexity** | $O(k)$ where $k$ is sample size |
| **Memory Guarantee** | Strict constant space bound |
| **Passes** | Exactly 1 pass over the data |

---

## 5. Deployment & Usage

### Basic Usage
```python
from core.reservoir import ReservoirSampler

items = range(1000)
sample = ReservoirSampler.sample_from_iterable(items, k=5)
# Result: [12, 452, 98, 221, 678] (random)
```

### Streaming Usage
```python
sampler = ReservoirSampler.streaming_sample(k=10)
next(sampler) # Init

for item in live_data_stream:
    reservoir = sampler.send(item)
```

---

## 6. Real-World Applications

-   **Database Query Sampling:** When a user requests "random 100 rows" from a multi-terabyte table without a known row count.
-   **System Monitoring:** Monitoring a high-traffic network link and keeping a sample of packets for inspection by security tools.
-   **A/B Testing:** Selecting a fixed number of users for a new experiment from an incoming stream of website visitors.
-   **Large Language Models:** Selecting a representative subset of training data from massive web-crawled datasets.
