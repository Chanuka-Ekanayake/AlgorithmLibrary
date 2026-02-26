# Algorithm Logic: Gale-Shapley Stable Matching

The entire algorithm revolves around eliminating one specific threat to the system: the **Blocking Pair**.

## 1. The Definition of "Stability"

A matching is only considered "stable" if there are absolutely no blocking pairs.

**What is a Blocking Pair?**
Imagine Client A is matched to Model 1, and Client B is matched to Model 2.
If Client A actually prefers Model 2, _and_ Model 2 actually prefers Client A over Client B, the system is unstable. Client A and Model 2 will logically bypass the system to pair up, leaving the other entities stranded.

Gale-Shapley guarantees that **zero** blocking pairs will exist when the algorithm finishes. It achieves this through a ruthless process of proposals and rejections.

---

## 2. The Mechanism: Propose, Engage, Dump

The algorithm runs in a `while` loop, processing a queue of "Free Proposers" until the queue is empty.

1. **The Proposal:** A free Proposer looks at their ranked preference list and proposes to the absolute highest-ranked Receiver they have not yet asked.
2. **The Receiver's Logic:** When a Receiver gets a proposal, they evaluate it purely out of self-interest based on their own ranked list:

- _Scenario A (Free):_ If the Receiver has no current match, they **must** accept the proposal to form a tentative engagement.
- _Scenario B (Trade Down):_ If the Receiver is already engaged, but the new Proposer is ranked _lower_ than their current match, the Receiver firmly **rejects** the new Proposer. The rejected Proposer goes back into the queue to try their next choice.
- _Scenario C (Trade Up):_ If the Receiver is already engaged, and the new Proposer is ranked _higher_ than their current match, the Receiver **breaks their current engagement** and accepts the new Proposer.

3. **The Ripple Effect:** When an engagement is broken, the dumped Proposer is thrown back into the "Free" queue. They must now move down their list and propose to their next best choice.

---

## 3. Step-by-Step Example

Let's look at a micro-market with 2 Clients (Proposers) and 2 Software Licenses (Receivers).

**Client Preferences:**

- **Client X:** Prefers License 1, then License 2.
- **Client Y:** Prefers License 1, then License 2.

**License Preferences:**

- **License 1:** Prefers Client Y, then Client X.
- **License 2:** Prefers Client X, then Client Y.

**The Execution Trace:**

1. **Round 1:** Client X is free. They propose to their top choice: License 1. License 1 is free, so they tentatively engage. _(Matches: License 1 -> Client X)_.
2. **Round 2:** Client Y is free. They propose to their top choice: License 1.
3. **The Conflict:** License 1 is currently engaged to Client X, but looks at its preference list. It prefers Client Y over Client X.
4. **The Dump:** License 1 accepts Client Y and dumps Client X. _(Matches: License 1 -> Client Y)_. Client X goes back into the free queue.
5. **Round 3:** Client X is free again. They already asked License 1, so they move to their second choice: License 2. License 2 is free and accepts. _(Matches: License 2 -> Client X)_.

**The Result:** The queue is empty. The final matches are strictly stable. Even though Client X didn't get their first choice, they cannot form a blocking pair with License 1, because License 1 strictly prefers its current match (Client Y).
