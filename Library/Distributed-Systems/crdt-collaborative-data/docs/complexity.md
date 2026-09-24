# Complexity Analysis: Conflict-free Replicated Data Types (CRDTs)

CRDTs trade **space** for **coordination freedom**. By storing enough metadata to resolve conflicts locally, they eliminate the need for any network round-trips during writes.

## 1. Time Complexity

### 1.1 Local Operations

| CRDT Type | `add` / `increment` | `remove` / `decrement` | `query` (value/contains) |
| --- | --- | --- | --- |
| **G-Counter** | O(1) | N/A | O(R) — sum over R replicas |
| **PN-Counter** | O(1) | O(1) | O(R) — sum P minus sum N |
| **LWW-Register** | O(1) | N/A | O(1) |
| **OR-Set** | O(1) | O(T) — T = tags for element | O(1) amortized |

Local operations are near-instant. The `R` factor in counter queries is typically small (number of replicas, not data size).

### 1.2 Merge Operations

| CRDT Type | Merge Complexity | Description |
| --- | --- | --- |
| **G-Counter** | O(R) | Element-wise MAX over R replica slots |
| **PN-Counter** | O(R) | Two G-Counter merges |
| **LWW-Register** | O(1) | Single timestamp comparison |
| **OR-Set** | O(E × T + S) | E = unique elements, T = avg tags per element, S = tombstone set size |

### 1.3 Convergence

Unlike Gossip (which converges in O(log N) rounds), CRDTs converge in **exactly 1 merge** — a single state exchange between any two replicas immediately synchronizes them. The total system converges when every pair of replicas has exchanged state at least once (directly or transitively).

| Metric | Complexity | Description |
| --- | --- | --- |
| **Per-pair convergence** | O(1) merge | One merge call fully synchronizes two replicas |
| **Full cluster convergence** | O(N) merges | Each node merges with at least one up-to-date peer |

---

## 2. Space Complexity

This is where CRDTs pay their tax. Metadata grows to enable conflict-free resolution.

| CRDT Type | Space per Replica | Description |
| --- | --- | --- |
| **G-Counter** | O(R) | One integer per replica in the cluster |
| **PN-Counter** | O(R) | Two integers per replica (P slot + N slot) |
| **LWW-Register** | O(1) | One value + one timestamp |
| **OR-Set** | O(E × T + S) | E elements × T tags each, plus S tombstones |

### 2.1 The OR-Set Tombstone Problem

The OR-Set's tombstone set grows monotonically — every remove adds tags to the tombstone set that can never be reclaimed without coordination. In a long-running system, this can cause **unbounded metadata growth**.

**Mitigation strategies:**
- **Garbage Collection Epochs:** Periodically, all replicas agree on a "safe point" and prune tombstones older than that point.
- **Causal Stability:** Once a tombstone has been observed by all replicas, it can be safely discarded.
- **Optimized OR-Set Variants:** The "Optimized OR-Set" (Bieniusa et al., 2012) reduces metadata by using dot-based versioning instead of UUIDs.

---

## 3. Message Complexity

Since CRDTs are state-based (CvRDT), the message size equals the full state:

| CRDT Type | Message Size | Description |
| --- | --- | --- |
| **G-Counter** | O(R) | The entire counts map |
| **PN-Counter** | O(R) | Both P and N counts maps |
| **LWW-Register** | O(1) | Value + timestamp |
| **OR-Set** | O(E × T + S) | All elements with tags + all tombstones |

**Optimization:** In practice, systems use **delta-CRDTs** (Almeida et al., 2018) that only transmit the *changes* since the last sync, reducing message size from O(state) to O(delta).

---

## 4. CRDTs vs. Consensus: Complexity Trade-offs

| Metric | CRDT (OR-Set) | Raft Consensus | Gossip Protocol |
| --- | --- | --- | --- |
| **Write latency** | O(1) — local | O(RTT × majority) | O(1) — local |
| **Read consistency** | Eventual | Strong (Linearizable) | Eventual |
| **Messages per write** | 0 (async sync) | O(N) | O(fan-out) |
| **Space overhead** | O(E × T + S) metadata | O(log size) | O(K) knowledge map |
| **Conflict resolution** | Mathematical (automatic) | Leader-based (no conflicts) | Version vector (last-write) |
| **Offline writes** | ✅ Unlimited | ❌ Requires quorum | ✅ Limited |

---

## 5. Scalability Characteristics

### 5.1 What Scales Well
- **Number of operations:** Local writes are O(1); CRDTs handle millions of operations per second per replica.
- **Geographic distribution:** Zero-coordination writes mean replicas in Tokyo and London can operate at local latency.

### 5.2 What Doesn't Scale Well
- **Number of replicas (R):** G-Counter and PN-Counter state grows linearly with R. At R > 10,000, consider hierarchical aggregation.
- **Tombstone accumulation:** OR-Set tombstones grow unboundedly without garbage collection. Production systems must implement periodic pruning.
- **State transfer size:** Full-state CvRDT sync becomes expensive for large datasets. Delta-state CRDTs or operation-based CRDTs (CmRDTs) mitigate this.

---

## 6. Performance Benchmarking (Theoretical)

| Dataset (OR-Set) | Elements | Replicas | Merge Time | State Size |
| --- | --- | --- | --- | --- |
| Small (Shopping list) | 50 | 3 | < 1 ms | ~ 2 KB |
| Medium (Shared playlist) | 10,000 | 10 | ~ 5 ms | ~ 500 KB |
| Large (Collaborative doc) | 100,000 | 50 | ~ 50 ms | ~ 10 MB |
| Massive (Global inventory) | 1,000,000 | 100 | ~ 500 ms | ~ 200 MB |

> **Note:** These are estimates for a naive state-based OR-Set. Delta-CRDTs reduce merge times and message sizes by 10-100x in practice.

---

## 7. References & Further Reading

- Shapiro, M., Preguiça, N., Baquero, C., & Zawirski, M. (2011). "Conflict-free Replicated Data Types." *SSS 2011*.
- Bieniusa, A., et al. (2012). "An Optimized Conflict-free Replicated Set." *arXiv:1210.3368*.
- Almeida, P., Shoker, A., & Baquero, C. (2018). "Delta State Replicated Data Types." *Journal of Parallel and Distributed Computing*.
- Kleppmann, M., & Beresford, A. R. (2017). "A Conflict-free Replicated JSON Datatype." *IEEE TPDS*.
- Ink & Switch (2019). "Local-first Software: You Own Your Data, in Spite of the Cloud."
