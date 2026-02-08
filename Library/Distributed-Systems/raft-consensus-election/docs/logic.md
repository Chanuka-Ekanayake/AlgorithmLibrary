# Algorithm Logic: Raft Leader Election

## 1. The Goal: Single "Source of Truth"

In a distributed marketplace, multiple servers must agree on which server is the "Leader" responsible for processing writes. If two servers act as leaders simultaneously, data corruption occurs. Raft ensures that for any given **Term**, there is **at most one** leader.

---

## 2. The Three States

Every node in the cluster exists in one of three states:

- **Follower:** The default, passive state. They only respond to requests from candidates and leaders.
- **Candidate:** A node that has timed out and is actively campaigning to become the new leader.
- **Leader:** The authority that handles all client requests and sends periodic heartbeats to maintain order.

---

## 3. Logical Clocks: Terms

Since physical clocks can drift between servers, Raft uses **Terms**.

1. Terms act as a logical counter that increments every time an election begins.
2. **Safety Rule:** If a node receives a message with a Term _greater_ than its own, it immediately updates its Term and reverts to a **Follower**. This ensures "stale" leaders are automatically deposed when a newer, faster node starts an election.

---

## 4. The Election Cycle

The logic follows a strict sequence:

1. **The Timeout:** Each Follower has a randomized `election_timeout` (e.g., 150ms to 300ms).
2. **The Campaign:** When the timer expires, the node becomes a **Candidate**, increments its **Term**, and votes for itself.
3. **The Request:** It sends `RequestVote` RPCs to all other nodes.
4. **The Vote:** A Follower will grant a vote if:

- The Candidate's Term is its own.
- It hasn't already voted for someone else in this Term.

5. **The Victory:** If the Candidate receives votes from a **Quorum** (), it promotes itself to **Leader**.

---

## 5. Heartbeats: Maintaining Authority

Once a leader is elected, it must prevent its Followers from timing out and starting new, unnecessary elections.

- The Leader sends empty **AppendEntries** messages (Heartbeats) at regular intervals.
- As long as Followers receive these heartbeats, they reset their `election_timeout` and remain submissive.

---

## 6. Logic: Handling "Split Votes"

If two nodes time out at the same time, they might split the votes (e.g., in a 4-node cluster, each gets 2 votes). No one reaches a majority.

- **The Fix:** Because our implementation uses **Randomized Timeouts**, one of those nodes will likely time out _again_ slightly faster than the other in the next round, breaking the deadlock and electing a winner.
