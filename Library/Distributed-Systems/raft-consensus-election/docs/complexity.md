# Complexity Analysis: Raft Consensus (Election)

Raft is a consensus algorithm designed for **fault tolerance** and **strong consistency**. Its complexity is measured by its ability to reach an agreement across a network despite node failures or message delays.

## 1. Time Complexity

| Event                    | Complexity | Description                                                                                     |
| ------------------------ | ---------- | ----------------------------------------------------------------------------------------------- |
| **Election Time**        |            | Typically resolves within 1-2 election timeout periods () if timeouts are correctly randomized. |
| **Heartbeat Interval**   |            | Leaders send heartbeats at fixed intervals to maintain authority.                               |
| **Detection of Failure** |            | Followers detect a leader failure once their `election_timeout` expires.                        |

### 1.1 The "Split Vote" Delay

If multiple nodes start an election at the exact same time, a "Split Vote" occurs where no one reaches a majority. The complexity of resolving this is minimized by **Randomized Timeouts**, ensuring that in the next round, one node will likely time out before the others and win the election.

---

## 2. Message Complexity

Communication overhead is the primary cost of Raft.

| Operation              | Complexity | Description                                                                                      |
| ---------------------- | ---------- | ------------------------------------------------------------------------------------------------ |
| **RequestVote**        |            | In the worst case, every node times out and requests votes from every other node ( nodes peers). |
| **Heartbeats**         |            | The leader sends one message to each follower per interval.                                      |
| **Quorum Requirement** |            | To make any decision (elect a leader or commit data), a strict majority must agree.              |

---

## 3. Space Complexity

The space complexity per node is:

- \*\*\*\*: Number of peer identifiers stored in the cluster configuration.
- \*\*\*\*: The size of the replicated log (in a full implementation).

For the **Election Module**, memory usage is near-constant ( per node) as we only store state variables, terms, and a set of vote identifiers.

---

## 4. Fault Tolerance Limits

Raft follows the **Quorum Rule** for survival:

- To survive \***\* failures, the cluster must have at least \*\*** nodes.

| Cluster Size () | Max Failures () | Majority Needed |
| --------------- | --------------- | --------------- |
| 3               | 1               | 2               |
| 5               | 2               | 3               |
| 7               | 3               | 4               |
| 9               | 4               | 5               |

---

## 5. Engineering Trade-offs

- **Safety over Availability:** Raft belongs to the **CP** (Consistency and Partition Tolerance) slice of the CAP theorem. If a network partition occurs and a majority cannot be reached, the system will stop accepting writes to remain consistent rather than risk a "Split Brain" scenario.
- **The "Randomization" Necessity:** Without the randomized timeout logic we implemented, the cluster could enter a permanent loop of failed elections, destroying system availability.
