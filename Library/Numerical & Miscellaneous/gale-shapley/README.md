# Gale-Shapley Stable Matching

## 1. Overview

In any two-sided market—whether matching freelance developers to client projects, or routing high-priority enterprise clients to exclusive machine learning models—conflicting preferences are inevitable. If a platform relies on a simple "first-come, first-served" greedy approach, it risks market instability.

The **Gale-Shapley Algorithm** is a Nobel Prize-winning combinatorial optimization engine. It mathematically guarantees a "stable" matching between two equally sized sets. A matching is stable if there are **zero blocking pairs**—meaning there is no scenario where Client A and Model 2 would both mutually prefer to bypass the platform's assignment to pair up with each other instead.

---

## 2. Technical Features

- **Guaranteed Stability:** Uses a strict proposal-and-rejection mechanism to definitively eliminate the possibility of blocking pairs, ensuring optimal market satisfaction.
- ** Preference Resolution:** Pre-computes the Receiver preference arrays into fast-lookup hash maps. This drops the inner-loop comparison from down to , safely bounding the absolute worst-case scenario to strict time complexity.
- **Proposer Optimality:** Implements the algorithmic game-theory principle where the group actively making the proposals (the `free_proposers` queue) mathematically secures the best possible valid matches, while the receiving group gets the worst valid matches.
- **Efficient State Tracking:** Utilizes `collections.deque` for queue operations, efficiently handling the ripple effects of broken engagements and re-proposals.

---

## 3. Architecture

```text
.
├── core/                  # Combinatorial Optimization Engine
│   ├── __init__.py        # Package initialization
│   └── matcher.py         # Proposer-driven matching logic and rank hashing
├── docs/                  # Technical Documentation
│   ├── logic.md           # The definition of "Stability" and Blocking Pairs
│   └── complexity.md      # Game theory and worst-case O(N^2) bounds
├── test-project/          # Two-Sided Marketplace Simulator
│   ├── app.py             # Enterprise Client vs. ML Model conflict resolution
│   └── instructions.md    # Guide for evaluating proposer-optimality
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

| Metric                   | Specification                                 |
| ------------------------ | --------------------------------------------- |
| **Time Complexity**      | (Worst-case limit on total proposals)         |
| **Space Complexity**     | (Requires full preference matrices)           |
| **Algorithmic Paradigm** | Combinatorial Optimization / Greedy Iteration |
| **Game Theory Bias**     | Strictly Proposer-Optimal / Receiver-Pessimal |

---

## 5. Deployment & Usage

### Integration

The `StableMatcher` can be deployed as the core assignment engine for any platform that requires matching two sets of users based on ranked preferences:

```python
from core.matcher import StableMatcher

# Define ranked preferences for the Proposers (e.g., Clients)
client_prefs = {
    "Client A": ["License 1", "License 2"],
    "Client B": ["License 1", "License 2"]
}

# Define ranked preferences for the Receivers (e.g., Software Licenses)
license_prefs = {
    "License 1": ["Client B", "Client A"],
    "License 2": ["Client A", "Client B"]
}

# Execute the Proposer-Optimal matching
final_assignments = StableMatcher.match(client_prefs, license_prefs)

print(final_assignments)
# Output: {'License 1': 'Client B', 'License 2': 'Client A'}

```

### Running the Simulator

To observe the engine systematically resolving a multi-party conflict over exclusive ML models:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the Marketplace Simulator:

```bash
python app.py

```

---

## 6. Industrial Applications

- **Two-Sided Marketplaces:** Matching gig-economy workers to local jobs, or matching freelance software engineers to enterprise contracts based on mutual skill and rate preferences.
- **Network Routing:** Assigning incoming user traffic to regional server clusters where users rank servers by lowest latency, and servers rank users by priority tier.
- **Institutional Assignments:** The exact algorithm used by the National Resident Matching Program (NRMP) to assign graduating medical students to hospital residency programs.
