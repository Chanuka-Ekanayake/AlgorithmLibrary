# LRU Cache: Least Recently Used Cache

## 1. Overview

The **LRU (Least Recently Used) Cache** is a fundamental data structure used in system design, caching layers, and optimization scenarios. It maintains a fixed-capacity store of key-value pairs and automatically evicts the least recently accessed item when the cache becomes full.

This module provides a **production-grade, O(1) time-complexity implementation** ideal for:
- **CPU Cache Management** - Simulating hardware cache behavior
- **Database Query Caching** - Memoizing expensive database queries
- **Web Server Caching** - Caching API responses and page fragments
- **Distributed System Optimization** - Reducing latency in microservices
- **Memory Management** - Virtual memory page replacement algorithms

---

## 2. Key Engineering Features

* **Constant Time Operations:** Both `get()` and `put()` operations run in **O(1)** time using a hash map backed by an OrderedDict
* **Automatic Eviction:** Intelligent least-recently-used eviction policy automatically removes stale data
* **Recency Tracking:** Access to any item automatically updates its recency status
* **Memory Efficient:** Fixed capacity prevents unbounded memory growth
* **Production Ready:** Type-safe with comprehensive error handling and statistics tracking
* **Simple API:** Intuitive `get()` and `put()` methods matching common cache interfaces

---

## 3. Folder Architecture

```text
.
├── core/                      # Core Implementation
│   └── lru_cache.py          # O(1) LRU Cache using OrderedDict
├── docs/                      # Technical Documentation
│   ├── logic.md              # Internal mechanics and design
│   ├── complexity.md         # Time/Space complexity analysis
│   └── use_cases.md          # Real-world application examples
├── test-project/             # Practical Examples & Tests
│   ├── cache_simulator.py    # Interactive cache demonstration
│   ├── benchmark.py          # Performance measurement
│   └── instructions.md       # Setup and usage guide
└── README.md                 # Module Entry Point (Current File)

```

---

## 4. Performance Benchmarks

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|-----------------|------------------|-------|
| **get(key)** | O(1) | O(1) | Hash map lookup + OrderedDict position update |
| **put(key, value)** | O(1) | O(1) | Hash map insert + eviction when full |
| **delete(key)** | O(1) | O(1) | Direct hash map removal |
| **Overall Space** | - | O(capacity) | Fixed-size cache never exceeds capacity |

---

## 5. Quick Start

### Basic Usage

```python
from core.lru_cache import LRUCache

# Create a cache with capacity 3
cache = LRUCache(capacity=3)

# Add items
cache.put("user_1", {"name": "Alice", "age": 30})
cache.put("user_2", {"name": "Bob", "age": 25})
cache.put("user_3", {"name": "Charlie", "age": 35})

# Retrieve items (marks as recently used)
print(cache.get("user_1"))  # {'name': 'Alice', 'age': 30}

# Add a new item - evicts least recently used (user_2)
cache.put("user_4", {"name": "David", "age": 28})

# user_2 is gone
print(cache.get("user_2"))  # None

# Check cache state
print(cache.get_all_keys())  # ['user_3', 'user_1', 'user_4']
print(cache.get_stats())
```

### Real-World Example: Database Query Cache

```python
cache = LRUCache(capacity=100)

def get_user_with_cache(user_id):
    # Check cache first
    cached_user = cache.get(user_id)
    if cached_user:
        return cached_user
    
    # Cache miss - fetch from database
    user = fetch_from_database(user_id)
    cache.put(user_id, user)
    return user
```

---

## 6. Algorithm Details

### Internal Structure
- **Hash Map (OrderedDict):** Maps keys to values while maintaining insertion/access order
- **Eviction Policy:** Removes the first item (oldest/least recently used) when capacity exceeded
- **Recency Tracking:** Accessed items are moved to the end of the order

### How It Works

1. **GET Operation:**
   - Look up key in hash map: O(1)
   - Move item to end (mark as recently used): O(1)
   - Return value

2. **PUT Operation:**
   - If key exists: Update value and move to end: O(1)
   - If new key: Add to hash map: O(1)
   - If at capacity: Remove first item: O(1)

3. **DELETE Operation:**
   - Remove key from hash map: O(1)

---

## 7. Why Python's OrderedDict?

In Python 3.7+, regular dictionaries maintain insertion order. However, `OrderedDict` provides:
- Explicit `move_to_end()` method for recency updates
- Clear, self-documenting code showing intent
- Compatibility with older Python versions
- Optimized implementation for order-based operations

---

## 8. Common Pitfalls & Solutions

| Issue | Problem | Solution |
|-------|---------|----------|
| **Capacity 0 or negative** | Invalid cache | Constructor validates capacity > 0 |
| **Accessing non-existent key** | KeyError | `get()` returns None safely |
| **Memory leak** | Cache grows unbounded | Fixed capacity with automatic eviction |
| **Stale data** | Old items not removed | Access-based eviction via recency |

---

## 9. Testing & Validation

Run the test project to see LRU Cache in action:

```bash
cd test-project
python cache_simulator.py
python benchmark.py
```

---

## 10. Further Reading

- [Google's LRU Cache in BigTable](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/)
- CPU Cache Architecture and Cache Replacement Policies
- Virtual Memory and Page Replacement Algorithms

---

## 11. Complexity Summary

| Metric | Value |
|--------|-------|
| **Time (get)** | O(1) |
| **Time (put)** | O(1) |
| **Time (delete)** | O(1) |
| **Space** | O(capacity) |

This implementation is optimal for the LRU Cache problem and suitable for production use.
