# Red-Black Tree Testing Environment

## Instructions

This lightweight test program verifies the execution integrity of all standard Red-Black Tree operations: Insert, Search, Delete, duplicate handling, and sequential-input stress testing.

### Getting Started

Validate that you are using Python 3 and navigate into the `test-project` folder via terminal:

```bash
cd test-project
python app.py
```

### Explanation of the Output

- **Insertion Demo:** Inserts a curated set of integer keys and prints the in-order traversal — confirming that BST ordering is preserved despite the structural rebalancing.
- **Tree Structure Print:** Displays the actual tree shape with RED/BLACK node colouring so you can visually inspect the color invariants.
- **Search Checks:** Exercises `search()` on existing keys, missing keys, ensuring correct value retrieval and `None` for absent keys.
- **Deletion Sequence:** Deletes three nodes (including the root) and re-prints the in-order traversal after each deletion to confirm correctness.
- **Duplicate Key:** Re-inserts an existing key with a new value — verifies that the value is updated without node duplication.
- **Stress Test:** Inserts keys 1–50 in strictly ascending order (the worst case for an unbalanced BST). Verifies that the resulting height satisfies the Red-Black bound $h \leq 2\lfloor\log_2(n+1)\rfloor$ and that the root is BLACK.
