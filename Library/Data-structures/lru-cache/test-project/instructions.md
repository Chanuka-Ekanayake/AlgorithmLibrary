# LRU Cache Test Project - Instructions

## Overview

This test project provides practical examples and performance benchmarks for the LRU Cache implementation.

## Files

- **cache_simulator.py** - Interactive cache visualization tool
- **benchmark.py** - Performance benchmarking and correctness validation
- **instructions.md** - This file

## Prerequisites

- Python 3.7 or higher
- Parent directory structure must be intact (core module accessible)

## Running the Simulator

The simulator helps you understand LRU Cache behavior interactively:

```bash
python cache_simulator.py
```

### Interactive Mode

**Commands:**

```
put <key> <value>    - Add or update an item
get <key>            - Retrieve an item (marks as recently used)
delete <key>         - Remove an item from cache
status               - Display current cache state
history              - Show recent operations
demo                 - Run automated demonstration
exit                 - Exit the simulator
```

**Example Session:**

```
>>> put user_1 Alice
[Shows cache status with Alice added]

>>> put user_2 Bob
[Shows cache status]

>>> get user_1
[Shows cache with user_1 marked as recently used]

>>> put user_3 Charlie
>>> put user_4 David
[If capacity is 3, user_2 should be evicted]

>>> status
[Shows current cache contains user_1, user_3, user_4]
```

### Automated Demo

Choose option 2 at startup to see an automated demonstration showing:

1. Adding items until cache is full
2. Accessing items (demonstrates recency update)
3. Adding new items (demonstrates eviction of least recently used)
4. Verifying evicted items are gone

## Running Benchmarks

The benchmark suite validates performance and correctness:

```bash
python benchmark.py
```

### What It Measures

1. **Basic Operations** - GET, PUT, mixed workloads
2. **Scaling** - Performance with caches of 100 to 100,000 items
3. **Eviction Overhead** - Impact of LRU eviction on performance
4. **Correctness** - 1000 random operations to validate correctness
5. **Summary** - Overall performance characteristics

### Expected Output

```
[1/5] Benchmarking basic operations...
Operation             Cache Size  Num Ops        Time (ms)    Throughput
GET                        1,000  100,000             32.45  3,083,531 ops/sec
PUT                        1,000  100,000             26.78  3,735,206 ops/sec
MIXED (70/15/15)           1,000  100,000             29.12  3,434,426 ops/sec

[2/5] Benchmarking cache size scaling...
  Cache size    100: 3,456,789 ops/sec
  Cache size  1,000: 3,412,654 ops/sec
  Cache size 10,000: 3,401,234 ops/sec
  Cache size 100,000: 3,398,901 ops/sec

[Results show O(1) performance regardless of cache size]
```

## Real-World Usage Scenarios

### 1. Database Query Cache

```python
from core.lru_cache import LRUCache

cache = LRUCache(capacity=1000)

def get_user(user_id):
    # Check cache first
    cached_user = cache.get(user_id)
    if cached_user:
        return cached_user
    
    # Cache miss - fetch from database
    user = database.query("SELECT * FROM users WHERE id = %s", (user_id,))
    cache.put(user_id, user)
    return user
```

### 2. API Response Cache

```python
cache = LRUCache(capacity=100)

def fetch_api(endpoint, params):
    cache_key = f"{endpoint}:{params}"
    
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response
    
    response = requests.get(endpoint, params=params)
    cache.put(cache_key, response.json())
    return response.json()
```

### 3. Computation Memoization

```python
cache = LRUCache(capacity=50)

def expensive_computation(n):
    if (result := cache.get(n)) is not None:
        return result
    
    result = compute_fibonacci(n)  # O(n) computation
    cache.put(n, result)
    return result
```

### 4. Session Store

```python
session_cache = LRUCache(capacity=10000)

def store_session(session_id, session_data):
    session_cache.put(session_id, session_data)

def get_session(session_id):
    return session_cache.get(session_id)
```

## Troubleshooting

### ImportError when running tests

**Problem:** "ModuleNotFoundError: No module named 'core'"

**Solution:** Ensure you're running from the test-project directory:
```bash
cd test-project
python cache_simulator.py
```

### Capacity validation error

**Problem:** "ValueError: Capacity must be positive"

**Solution:** Provide a positive integer for capacity:
```python
cache = LRUCache(capacity=100)  # ✓ Valid
cache = LRUCache(capacity=0)    # ✗ Invalid
cache = LRUCache(capacity=-5)   # ✗ Invalid
```

### Performance is slower than expected

**Factors affecting performance:**

1. **System load** - Other processes consuming CPU
2. **Python version** - Older versions may be slower
3. **PyPy vs CPython** - PyPy is faster for this workload
4. **Disk I/O** - SSD vs HDD affects Python startup
5. **Value size** - Larger values take more time to copy

**Improvement tips:**

```python
# ✓ Recommended: Use with large capacities
cache = LRUCache(capacity=10000)

# ✗ Avoid: Thrashing with small cache
cache = LRUCache(capacity=1)  # Forces constant eviction
```

## Learning Outcomes

After exploring this test project, you should understand:

1. ✓ LRU Cache data structure and eviction policy
2. ✓ How OrderedDict provides O(1) order tracking
3. ✓ Why LRU Cache is essential for performance optimization
4. ✓ Real-world applications in caching scenarios
5. ✓ Performance characteristics and scalability

## Next Steps

- Explore the [logic.md](../docs/logic.md) file for internal mechanics
- Read [complexity.md](../docs/complexity.md) for detailed complexity analysis
- Try the [cache_simulator.py](cache_simulator.py) with different capacities
- Run [benchmark.py](benchmark.py) to measure performance

## Questions?

Refer to the main [README.md](../README.md) or explore the source code in [core/lru_cache.py](../core/lru_cache.py).
