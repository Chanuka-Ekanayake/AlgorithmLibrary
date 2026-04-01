# Treap Testing Environment

## Instructions

This lightweight test program verifies the execution integrity of standard internal Treap operations: Search, Insert, and recursive Delete.

### Getting Started

Validate that you are using Python 3 and navigate deeply into the inner `test-project` folder via terminal commands:

```bash
cd test-project
python app.py
```

### Explanation of the Output Check
- **Insertion Tracker:** The program sequentially loads a fixed target array string into a fresh memory Treap.
- **BST Sequence Verification:** It prints the Treap keys via "In-Order" algorithms to demonstrably prove that sequential rules haven't forcefully broken via unpredictable priority bubbling routines.
- **Key Recovery:** Tests extraction of node payloads on-demand while dealing accurately with uninitialized errors.
- **Recursion Trimming Base:** Drops random root segments within the layout array and queries extraction algorithms to check if nodes effectively survived subtree rotation swaps correctly.
