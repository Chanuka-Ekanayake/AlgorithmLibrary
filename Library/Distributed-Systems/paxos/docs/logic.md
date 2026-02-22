# Algorithm Logic: Paxos Consensus

Imagine a distributed database for your e-commerce platform with three nodes (A, B, and C). Two different users simultaneously try to purchase the last available software license.

User 1's request hits Node A. User 2's request hits Node B.
Node A wants the cluster to agree the buyer is "User 1". Node B wants the cluster to agree the buyer is "User 2".

Without Paxos, Node A and Node B might both write their own values, causing a "split-brain" where the database fundamentally corrupts itself. Paxos prevents this using a strict Two-Phase Commit protocol.

## Phase 1: The Promise (Prepare)

Before a Proposer can tell the database what to write, it must ask for permission and gather intelligence about what the other nodes are doing.

1. **Generate ID:** The Proposer generates a unique, monotonically increasing ID (e.g., `ID: 100`).
2. **Broadcast:** It sends a `PREPARE(100)` message to all Acceptors (Nodes A, B, and C).
3. **The Promise:** When an Acceptor receives `PREPARE(100)`, it checks its internal memory.

- If it has already promised to listen to a higher ID (e.g., `ID: 105`), it ignores the message.
- If `100` is the highest ID it has ever seen, it mathematically promises: _"I will never accept another proposal with an ID lower than 100."_

4. **The Intelligence:** If the Acceptor has _already_ accepted a final value from a previous, completed round, it returns that value along with its promise.

---

## Phase 2: The Final Vote (Accept)

Once the Proposer receives a `PROMISE` from a **strict majority** of the Acceptors (e.g., 2 out of 3), it moves to Phase 2.

1. **The Crucial Rule (Value Adoption):** * If *any\* Acceptor returned an already accepted value during Phase 1, the Proposer **must abandon its own value**. It must adopt the existing value and propose it instead. This is how Paxos forces competing Proposers to eventually converge on the exact same data.

- If no Acceptor returned an existing value, the Proposer is free to propose its original value (e.g., "User 1").

2. **Broadcast:** The Proposer sends an `ACCEPT(100, "User 1")` message to all Acceptors.
3. **The Final Check:** When an Acceptor receives the `ACCEPT` message, it checks its promise.

- Did it promise to listen to an ID higher than 100 while the Proposer was busy? If yes, it rejects the `ACCEPT`.
- If 100 is still the highest ID it knows about, it permanently writes the value "User 1" to its disk.

4. **Consensus:** Once a majority of Acceptors write the value, consensus is achieved. The transaction is finalized.

---

## The "Dueling Proposers" Scenario

Let's look at how Phase 1 prevents our User 1 vs. User 2 conflict:

1. **Node A** sends `PREPARE(100)` for User 1. It gets promises from Nodes A and C.
2. **Node B** sends `PREPARE(105)` for User 2. It gets promises from Nodes B and C.
   _(Note: Node C just broke its promise to Node A, because 105 > 100. This is allowed and expected)._
3. **Node A** sends `ACCEPT(100, "User 1")` to Nodes A and C.

- Node A accepts it.
- Node C **rejects** it, because Node C promised Node B it would only listen to IDs .

4. **Node A fails** to get a majority.
5. **Node B** sends `ACCEPT(105, "User 2")` to Nodes B and C. Both accept it.
6. **Consensus Reached:** User 2 wins the license. The system remains perfectly consistent.

When Node A retries its transaction later, it will learn during Phase 1 that "User 2" has already been accepted, and it will inform User 1 that the item is sold out.
