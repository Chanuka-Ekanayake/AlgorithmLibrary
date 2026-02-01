# Algorithm Logic: LRU Cache (Least Recently Used)

## 1. The Core Objective

The goal of an LRU Cache is to manage a fixed amount of memory by keeping the most frequently accessed items readily available and automatically discarding the items that haven't been touched in the longest time.

To achieve ** time complexity**, we combine two distinct data structures:

1. **Hash Map (Dictionary):** For instant  search.
2. **Doubly Linked List:** For instant  re-ordering and eviction.

---

## 2. Why a Doubly Linked List?

In a standard array or singly linked list, removing an item or moving it to the front is expensive () because you have to shift elements or traverse the list to find the previous node.

* A **Doubly Linked List** allows a node to know both its successor (`next`) and its predecessor (`prev`).
* This allows us to "snip" a node out of the middle and reconnect its neighbors in constant time.

---

## 3. The Sentinel Node Strategy

We use two "dummy" nodes: a **Head** and a **Tail**.

* **Head (Most Recent):** New or accessed items are always moved to the position right after the Head.
* **Tail (Least Recent):** The item to be evicted is always the one right before the Tail.
* **Benefit:** These nodes are never deleted. They ensure that `node.prev` and `node.next` are never `null` during our operations, which prevents edge-case crashes when the cache is empty or full.

---

## 4. Operational Flow

### 4.1 The `get(key)` Logic

1. **Look up** the key in the Hash Map.
2. **If not found:** Return `-1`.
3. **If found:**
* The map gives us the specific `Node`.
* **Remove** the node from its current position in the list.
* **Add** it back to the front (immediately after the Head).
* This marks it as the "Most Recently Used."



### 4.2 The `put(key, value)` Logic

1. **If the key exists:** Remove the old node from the list and the map.
2. **Create** a new node and add it to the front of the list.
3. **Add** the new node to the map.
4. **Capacity Check:**
* If `map.size > capacity`:
* Identify the **LRU node** (at `tail.prev`).
* **Remove** it from both the list and the map.



---

## 5. Industrial Application: Database Accelerator

In your 2026 software marketplace project, this logic is used as a **Query Accelerator**:

* **Scenario:** Fetching "Machine Learning Model" metadata from a slow database.
* **Logic:** The first time a user views a model, the system fetches it from the DB and stores it in the LRU Cache.
* **Benefit:** Subsequent views (by that user or others) are served instantly from memory. If the cache fills up, models that haven't been viewed in weeks are automatically evicted to make room for trending ones.

---

## 6. Type Safety & Guarding

To maintain high engineering standards, our implementation uses **Type Guards**. Even though the Sentinel nodes prevent `None` values, we explicitly check for `None` to satisfy strict static analysis tools, ensuring the code is "Production Ready."