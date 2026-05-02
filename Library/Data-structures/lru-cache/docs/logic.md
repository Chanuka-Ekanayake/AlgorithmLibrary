# LRU Cache: Internal Logic & Design

## Data Structure Overview

The LRU Cache implementation uses a **Hash Map (OrderedDict)** to achieve O(1) operations:

```
┌─────────────────────────────────────┐
│      OrderedDict (Python 3.7+)      │
├─────────────────────────────────────┤
│ Maintains both:                     │
│ - Key → Value mapping (hash table)  │
│ - Insertion/Access order (linked)   │
└─────────────────────────────────────┘
```

## Why OrderedDict Instead of Traditional Doubly-Linked List?

### Traditional Approach (Textbook)
```
Hash Map: key → Node reference
    │
    └─→ Node ─→ Node ─→ Node
         ↓       ↓       ↓
       value   value   value
    (doubly-linked)
```

### Python Optimized Approach (This Implementation)
```
OrderedDict internally maintains the linked structure
- Eliminates manual node creation
- Leverages CPython's optimized C implementation
- Cleaner, more maintainable code
- Same O(1) complexity
```

## Operation Mechanics

### GET Operation Flow

```python
def get(self, key):
    if key not in cache:
        return None                    # Miss: O(1)
    
    cache.move_to_end(key)            # Mark as recent: O(1)
    return cache[key]                 # Return value: O(1)
```

**Timeline Example (Capacity 3):**
```
Initial:     [A] [B] [C]  (order: least to most recent)

get(A):      [B] [C] [A]  (A moved to end - now most recent)

get(B):      [C] [A] [B]  (B moved to end)

get(C):      [A] [B] [C]  (C moved to end)
```

### PUT Operation Flow

```python
def put(self, key, value):
    if key in cache:
        cache[key] = value            # Update: O(1)
        cache.move_to_end(key)        # Mark as recent: O(1)
    else:
        cache[key] = value            # Insert: O(1)
        if len(cache) > capacity:
            cache.popitem(last=False) # Evict LRU: O(1)
```

**Timeline Example (Capacity 3):**
```
Initial:     [A] [B] [C]   (full)

put(D, d):   [B] [C] [D]   (A evicted as least recent)

put(B, b'):  [C] [D] [B]   (B updated and moved to end)

put(E, e):   [D] [B] [E]   (C evicted)
```

## Why O(1) Time Complexity?

### Hash Map Lookup
```
Key → Value: O(1) amortized
(Python dict uses hash table)
```

### OrderedDict.move_to_end(key)
```
Implemented in C with pointers, not full list traversal
- Just updates linked list pointers
- No iteration through items
- O(1) guaranteed
```

### popitem(last=False)
```
Removes the first node in the linked structure
- No traversal needed
- Direct pointer manipulation
- O(1) constant time
```

## Memory Layout (Conceptual)

```
Memory View of [User_1] [User_2] [User_3]

┌─────────┬──────────┐
│ User_1  │ 0x2048   │  ← Points to User_2
├─────────┼──────────┤
│ User_2  │ 0x3072   │  ← Points to User_3
├─────────┼──────────┤
│ User_3  │ None     │  ← Tail (most recent)
└─────────┴──────────┘

Oldest ────────────────→ Newest
```

## Eviction Timing

```python
# Add items until full
cache = LRUCache(3)
cache.put(1, 'a')  # [1]
cache.put(2, 'b')  # [1, 2]
cache.put(3, 'c')  # [1, 2, 3] ← Full

# Next insertion triggers eviction
cache.put(4, 'd')  # [2, 3, 4] ← Item 1 evicted
```

**Eviction Decision:** Item 1 was the least recently used:
- Never accessed after insertion
- Furthest from the end of the order
- First to be removed by `popitem(last=False)`

## Recency Semantics

An item becomes "recently used" when:

1. **PUT (new key):** Item added at the end
2. **PUT (existing key):** Item updated and moved to end
3. **GET:** Item accessed and moved to end
4. **DELETE:** Item removed entirely

```python
cache.put(1, 'a')     # 1 is now most recent
cache.get(1)          # 1 remains most recent (moved to end)
cache.put(1, 'a2')    # 1 is still most recent (updated)
cache.put(2, 'b')     # 1 is no longer most recent
```

## Edge Cases

### Empty Cache
```python
cache.get(1)  # Returns None (no error)
cache.delete(1)  # Returns False
```

### Single Item Cache
```python
cache = LRUCache(1)
cache.put(1, 'a')  # [1]
cache.put(2, 'b')  # [2] ← Item 1 immediately evicted
```

### Accessing Non-Existent Key
```python
cache.put(1, 'a')  # [1]
cache.get(2)  # Returns None, no side effects
```

### Updating Existing Key
```python
cache.put(1, 'a')  # [1]
cache.put(1, 'a2')  # Still [1], just updated value
                    # Not [1, 1] - prevents duplicates
```

## Comparison: Hash Map vs. OrderedDict vs. Manual Linked List

| Aspect | Hash Map | OrderedDict | Manual Linked List |
|--------|----------|-------------|-------------------|
| Lookup (get) | O(1) | O(1) | O(1) |
| Insertion | O(1) | O(1) | O(1) |
| Move to End | ❌ Not possible | O(1) | O(1) with node ref |
| Eviction | ❌ Cannot pick | O(1) | O(1) |
| Code Complexity | N/A | Simple | Complex (pointers) |
| Maintainability | N/A | High | Low (prone to bugs) |
| CPython Optimized | ✓ | ✓ | ❌ |

## Conclusion

The OrderedDict-based approach combines:
- **Simplicity:** No manual node creation
- **Efficiency:** C-level implementation
- **Correctness:** Built-in order guarantees
- **Maintainability:** Clear, readable code

All while maintaining the optimal **O(1) amortized time complexity** for all operations.
