# Bloom Filter: Probabilistic Membership Checker

## 1. Overview

A **Bloom Filter** is a space-efficient, probabilistic data structure used to determine whether an element is a member of a set. It is uniquely designed to provide high-speed responses with zero **False Negatives** (if the filter says an item is not there, it is definitely not there) while maintaining a small, controllable rate of **False Positives**.

In a professional environment, Bloom Filters are used to prevent expensive database lookups or network requests by acting as an immediate "pre-filter" guard.

---

## 2. Technical Features

* **Multi-Hash Architecture:** Uses  independent hash functions to map items into a fixed-size bit array.
* **Constant Time Operations:** Both insertion and membership checks perform at  time, regardless of how many millions of items are in the set.
* **Memory Optimization:** Capable of representing vast datasets in a fraction of the memory required by traditional Hash Sets.
* **Security Application:** Includes a `test-project` that simulates a real-time **Malicious URL Filter** for protecting software downloads.

---

## 3. Architecture

```text
.
├── core/                  # Engine Logic
│   └── bloom_filter.py    # Multi-hash and bit-array implementation
├── docs/                  # Technical Documentation
│   ├── logic.md           # The mechanics of multi-hashing and collisions
│   └── complexity.md      # Space-time trade-off analysis
├── test-project/          # Security Simulator
│   ├── app.py             # Malicious URL Guard CLI
│   ├── url_database.csv   # Dataset of known security threats
│   └── instructions.md    # Operation and testing guide
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric | Specification |
| --- | --- |
| **Time Complexity** |  (Constant relative to dataset size) |
| **Space Complexity** |  (Fixed memory footprint) |
| **Accuracy** | 100% True Negative |
| **Deletions** | Not Supported (Standard Implementation) |

---

## 5. Deployment & Usage

### Integration

The `BloomFilter` class is designed for low-latency membership testing:

```python
from core.bloom_filter import BloomFilter

# Initialize for 1000 items with 1% false positive rate
security_guard = BloomFilter(expected_items=1000, false_positive_rate=0.01)

# Add a blacklisted key
security_guard.add("KEY-992-XJK")

# Fast check
if security_guard.exists("KEY-992-XJK"):
    print("Potential threat detected.")

```

### Running the Simulator

To execute the Malicious URL Guard:

1. Navigate to the `test-project` directory:
```bash
cd test-project

```


2. Run the application:
```bash
python app.py

```



---

## 6. Real-World Applications

* **Content Delivery Networks (CDNs):** Filtering one-hit-wonder requests to save cache space.
* **Cryptocurrency:** SPV (Simplified Payment Verification) nodes use Bloom Filters to sync relevant transactions.
* **Database Systems:** Postgres and Apache Cassandra use them to avoid scanning data blocks for keys that don't exist.
* **Browser Security:** Instantly checking URLs against a local list of millions of malicious sites.