# Algorithm Logic: Consistent Hashing (The Hash Ring)

## 1. The "Ring" Concept

In traditional hashing, we use . When the number of servers () changes, the result of the modulo changes for almost every key.

Consistent Hashing solves this by mapping both **Servers** and **Data Keys** onto a single circular number line (the "Ring"). We treat the maximum possible hash value as being right next to the minimum value (e.g., wraps back to ).

---

## 2. Placing Nodes (Servers)

When a server is added to the cluster:

1. We hash the server's ID (e.g., `Server-A`) multiple times using virtual suffixes (`Server-A#1`, `Server-A#2`).
2. These hashes are plotted as points on the ring.
3. Using **Virtual Nodes** ensures that a single physical server is responsible for many non-contiguous segments of the ring, which averages out the load.

---

## 3. The "Clockwise Search"

To find which server should store a specific piece of data (like a "Software Binary" in your marketplace):

1. **Hash the Key:** We find the point on the ring where the data's key resides.
2. **Travel Clockwise:** From that point, we move clockwise around the ring.
3. **The First Hit:** The first server node we encounter is the "Owner" of that data.

---

## 4. Handling Cluster Changes

### Adding a Server

When a new server (Server-X) is inserted between Server-A and Server-B:

- Only the keys that were previously assigned to Server-B but now fall between Server-A and the new Server-X need to move.
- All other servers and their data remain **completely unaffected**.

### Server Failure

If a server crashes:

- Its segment of the ring is simply bypassed.
- The next request for data in that segment will continue clockwise until it hits the **next** available server.
- Only the data from the failed server is redistributed, preventing a system-wide re-indexing.

---

## 5. Logic Flow: `get_node(key)`

1. **Hash the Request:** Calculate `h = hash(key)`.
2. **Binary Search:** Find the smallest hash in our sorted list of virtual nodes that is .
3. **Handle Overflow:** If is larger than any node hash, return the very first node in the list (wrapping around the ring).
4. **Return:** Provide the physical node identifier associated with that hash.
