# Complexity Analysis: Gale-Shapley Stable Matching

The Gale-Shapley algorithm guarantees that a perfectly stable matching will always be found between two equally sized sets. However, the cost of that guarantee scales quadratically, and the rules of the algorithm mathematically favor one side of the market over the other.

## 1. Time Complexity

Let be the number of Proposers (which is equal to the number of Receivers).

| Scenario         | Complexity | Description                                                                                                                                         |
| ---------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Best Case**    |            | Every Proposer's first choice happens to be unique. Everyone proposes once, everyone is accepted immediately, and the algorithm terminates.         |
| **Worst Case**   |            | Every Proposer is rejected by almost every Receiver before finally settling. The total number of proposals made across the entire loop approaches . |
| **Average Case** |            | In randomized preference lists, Proposers generally find a stable match long before exhausting their entire list.                                   |

### The Bottleneck: Array Scans vs. Hash Maps

If we look at the inner `while` loop, a Receiver often has to decide between their _current_ match and a _new_ proposal.

If the algorithm has to scan the Receiver's preference array from start to finish to figure out who is ranked higher, that check takes time. Nested inside a loop that can run times, this would accidentally degrade the algorithm to . By pre-computing the Receiver preferences into a fast-lookup dictionary (`receiver_ranks`), we reduce that comparison to , safely locking the absolute worst-case scenario at .

---

## 2. Space Complexity

| Structure               | Complexity | Description                                                                                                |
| ----------------------- | ---------- | ---------------------------------------------------------------------------------------------------------- |
| **Preference Matrices** |            | Both the Proposers and Receivers must store a ranked list of all members of the opposite set ( items).     |
| **Rank Lookups**        |            | The pre-computed dictionary that allows for rank comparisons requires storing an inverted matrix of ranks. |
| **Match Tracking**      |            | Storing the final pairs and tracking the queue of free Proposers requires linear space.                    |
| **Total Space**         | \*\*\*\*   | The space required strictly scales with the size of the preference lists.                                  |

---

## 3. Game Theory: Proposer Optimality

The most important "complexity" of Gale-Shapley is its inherent, mathematical bias. In a market where multiple stable configurations are possible, the algorithm does not find a "neutral" middle ground.

- **Proposer-Optimal:** The group that does the proposing (in our code, the `free_proposers` queue) is mathematically guaranteed to get the absolute _best_ valid partner they could possibly have in any stable matching.
- **Receiver-Pessimal:** The group that receives the proposals is mathematically guaranteed to end up with the _worst_ valid partner they could possibly have in any stable matching.

### Real-World Business Implications

If you use this algorithm on your e-commerce platform to match freelance developers to client projects, you must decide who plays which role:

- If the **Clients propose** to the Developers, the algorithm maximizes client satisfaction.
- If the **Developers propose** to the Clients, the algorithm maximizes developer satisfaction.

You cannot maximize both. The architecture of the algorithm forces you to pick a winning side.
