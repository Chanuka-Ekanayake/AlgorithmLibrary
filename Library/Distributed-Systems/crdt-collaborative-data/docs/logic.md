# Algorithm Logic: Conflict-free Replicated Data Types (CRDTs)

## 1. The Problem: Collaboration Without a Leader

In Raft or Paxos, a **Leader** coordinates all writes — if the leader dies or the network partitions, the system stalls. But what if you're building a collaborative shopping list app where Alice (on a plane, offline) and Bob (on a train, offline) are both editing the same list simultaneously?

CRDTs solve this by making conflict **mathematically impossible**. Every replica can accept writes immediately, without contacting any other node. When replicas eventually sync, the merge operation is guaranteed to produce the same result regardless of the order messages arrive.

---

## 2. The Mathematical Foundation: Join-Semilattice

A CRDT's merge operation must satisfy three properties that together form a **Join-Semilattice**:

1. **Commutative:** `merge(A, B) = merge(B, A)` — Order of syncing doesn't matter.
2. **Associative:** `merge(merge(A, B), C) = merge(A, merge(B, C))` — Grouping doesn't matter.
3. **Idempotent:** `merge(A, A) = A` — Duplicate messages are harmless.

If a merge function satisfies all three, then **Strong Eventual Consistency** is guaranteed: any two replicas that have received the same set of updates (in any order, with any duplicates) will have identical state.

---

## 3. CRDT Taxonomy: State-Based vs. Operation-Based

Our implementation uses **State-Based CRDTs (CvRDTs)**:

- **State-Based (CvRDT):** Replicas send their entire state. The receiver calls `merge()` to combine it with their local state. Requires only eventual delivery (tolerates duplicates and reordering).
- **Operation-Based (CmRDT):** Replicas send individual operations (e.g., "add X"). Requires exactly-once, causal delivery, which is harder to guarantee.

State-based CRDTs are simpler and more robust — they work even if the network duplicates or reorders messages.

---

## 4. The Four Primitives

### 4.1 G-Counter (Grow-Only Counter)

**Intuition:** Each node has its own "counter slot." Only that node can increment its slot. The global count is the sum of all slots.

```text
State: { "node_A": 5, "node_B": 3, "node_C": 7 }
Value: 5 + 3 + 7 = 15

Merge Rule: element-wise MAX
  Local:  { "node_A": 5, "node_B": 3 }
  Remote: { "node_A": 3, "node_B": 4, "node_C": 7 }
  Result: { "node_A": 5, "node_B": 4, "node_C": 7 }
```

**Why MAX works:** Each node's counter only grows. Taking the maximum of two observations always yields the most up-to-date value. This is the simplest join-semilattice.

### 4.2 PN-Counter (Positive-Negative Counter)

**Intuition:** Two G-Counters in a trench coat. One tracks increments (P), the other tracks decrements (N). The net value is `P - N`.

```text
P-Counter: { "node_A": 10 }  →  Total P = 10
N-Counter: { "node_A": 3  }  →  Total N = 3
Net Value: 10 - 3 = 7
```

**Why it works:** Since G-Counters can only grow, and we never try to make a counter "go down," the semilattice properties are preserved. Subtraction is purely a read-time calculation.

### 4.3 LWW-Register (Last-Writer-Wins)

**Intuition:** Every write is tagged with a timestamp. When two replicas merge, the value with the highest timestamp wins.

```text
Replica A: ("dark_mode", ts=1000.5)
Replica B: ("light_mode", ts=1000.8)

Merge Result: ("light_mode", ts=1000.8) — B was more recent
```

**Trade-off:** LWW is simple but can silently drop writes. If Alice sets "dark_mode" at t=1000.5 and Bob sets "light_mode" at t=1000.8, Alice's preference is lost. This is acceptable for settings/status fields but not for collaborative text.

### 4.4 OR-Set (Observed-Remove Set) — The Star of the Show

**Intuition:** The hardest problem in CRDTs is concurrent add + remove of the same element. The OR-Set solves it elegantly with **unique tags**.

**The Scenario:**
```text
Alice's device (offline):  adds "Milk"   → tag: alice:abc123
Bob's device (offline):    adds "Milk"   → tag: bob:def456
Bob's device (offline):    removes "Milk" → tombstones: {bob:def456}
```

**The Merge:**
```text
Tags for "Milk": {alice:abc123, bob:def456}
Tombstones:      {bob:def456}
Live tags:       {alice:abc123}   ← Alice's add SURVIVES!
Result:          "Milk" is IN the set  ✓
```

**Why it works:** Bob's remove only tombstones the tags Bob had *observed* at remove time. Alice's concurrent add created a *different* tag that Bob never saw. So Alice's add wins — this is called **add-wins semantics**, and it's the safest default for collaborative applications.

---

## 5. State Progression: A Visual Walkthrough

```text
Timeline:
─────────────────────────────────────────────────────
Alice (offline)          Bob (offline)
─────────────────────────────────────────────────────
add("Milk")              add("Eggs")
add("Bread")             add("Milk")
remove("Bread")          remove("Milk")
                         add("Butter")
─── Both come online and SYNC ───
─────────────────────────────────────────────────────
Alice merges Bob's state    Bob merges Alice's state
─────────────────────────────────────────────────────
Result (BOTH identical):
  {"Milk", "Eggs", "Butter"}

Why "Milk" survived: Alice's add("Milk") created tag alice:xxx
  which Bob's remove never saw. Add wins!
Why "Bread" is gone: Alice herself removed it, tombstoning
  her own tag. No concurrent add existed to save it.
```

---

## 6. CRDTs vs. Consensus: When to Use What

| Scenario | Use CRDT | Use Raft/Paxos |
| --- | --- | --- |
| Collaborative editing (Figma, Google Docs) | ✅ | ❌ |
| Offline-first mobile apps | ✅ | ❌ |
| Distributed counters (view counts, likes) | ✅ | ❌ |
| Bank account balance (must never go negative) | ❌ | ✅ |
| Leader election | ❌ | ✅ |
| Distributed locking | ❌ | ✅ |

**Rule of thumb:** If you need a **guarantee** (e.g., "balance ≥ 0"), use consensus. If you need **availability and partition tolerance**, use CRDTs.

---

## 7. Real-World: How Figma Uses CRDTs

Figma's multiplayer engine is built on CRDTs:

1. Each user's browser has a **local CRDT replica** of the design document.
2. Every cursor movement, shape drag, or property change is a local CRDT mutation — applied instantly (no server round-trip).
3. Mutations are streamed to the Figma server, which merges them and broadcasts to other users.
4. If a user goes offline and reconnects, their accumulated local mutations merge cleanly with the server state. No conflicts, no "merge conflict" dialogs.

This is why Figma feels "instant" even on slow connections — the CRDT guarantees that optimistic local updates will always converge correctly.
