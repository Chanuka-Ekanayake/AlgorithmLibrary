# Coin Change (Dynamic Programming Allocation)

## 1. Overview

In a cloud or e-commerce environment that sells computational resources, API credits, or software licenses in predefined pricing tiers, allocating the exact requested amount to a user is a critical backend task.

While a standard "Greedy" algorithm (always picking the largest available bundle first) is fast, it fundamentally fails when bundle denominations are non-standard, resulting in massively inefficient allocations. The **Coin Change** algorithm solves this using **Dynamic Programming (DP)**. It evaluates overlapping subproblems from the bottom up to mathematically guarantee that every user request is fulfilled using the absolute minimum number of database transactions or server allocations.

---

## 2. Technical Features

- **Mathematical Optimization:** Abandons greedy heuristics in favor of exploring optimal substructures, guaranteeing the lowest possible overhead for any given target amount.
- **State Tracking & Backtracking:** Maintains a historical breadcrumb array (`tracker`) during the bottom-up calculation. This allows the engine to instantly backtrack from the target to generate a perfectly accurate "receipt" of the specific bundles used.
- **Bottom-Up Architecture:** Avoids the severe function overhead and stack-overflow risks associated with recursive (top-down) brute force by iteratively building the solution from $0$ up to the target amount.
- **Immutable Failure States:** Gracefully detects and handles impossible allocation requests (e.g., requesting 7 credits when only bundles of 5 and 10 exist) without entering infinite loops.

---

## 3. Architecture

```text
.
├── core/                  # Allocation Engine
│   ├── __init__.py        # Package initialization
│   └── optimizer.py       # Bottom-up DP table and backtracking receipt generation
├── docs/                  # Technical Documentation
│   ├── logic.md           # Optimal substructure and overlapping subproblems
│   └── complexity.md      # The Greedy Fallacy and O(T * B) bounds
├── test-project/          # API Credit Bundle Allocation Simulator
│   ├── app.py             # Side-by-side execution of Greedy vs. DP algorithms
│   └── instructions.md    # Guide for evaluating overhead reduction metrics
└── README.md              # Documentation Entry Point

```

---

## 4. Performance Specifications

Let $T$ be the Target amount and $B$ be the number of available Bundle denominations.

| Metric                  | Specification                              |
| ----------------------- | ------------------------------------------ |
| **Time Complexity**     | $O(T \times B)$                            |
| **Space Complexity**    | $O(T)$ (for the `dp` and `tracker` arrays) |
| **Allocation Accuracy** | 100% (Mathematically Optimal)              |

---

## 5. Deployment & Usage

### Integration

The `ResourceOptimizer` can be imported to power the checkout logic for customized billing tiers:

```python
from core.optimizer import ResourceOptimizer

# 1. Define active pricing tiers/bundles
pricing_tiers = [100, 1500, 2500]

# 2. User requests exactly 3,000 API credits
requested_credits = 3000

try:
    # 3. Generate optimal allocation receipt
    receipt = ResourceOptimizer.get_optimal_allocation(pricing_tiers, requested_credits)
    print(f"Bundles Allocated: {len(receipt)}")
    print(f"Receipt: {receipt}")
    # Output: Bundles Allocated: 2 | Receipt: [1500, 1500]

except ValueError as e:
    print(f"Allocation Error: {e}")

```

### Running the Simulator

To observe exactly how a naive Greedy allocator wastes system resources compared to the DP engine:

1. Navigate to the `test-project` directory:

```bash
cd test-project

```

2. Run the Allocation Simulator:

```bash
python app.py

```

---

## 6. Industrial Applications

- **Cloud Resource Provisioning:** Dynamically allocating the exact number of virtual machine instances or Kubernetes pods needed to fulfill a specific compute threshold with minimal waste.
- **E-Commerce Billing:** Calculating the optimal combination of gift cards, promotional credits, or custom currency bundles to satisfy an exact cart total.
- **Inventory Management:** Fulfilling bulk hardware orders using the minimum number of shipping containers or predefined pallet sizes.
