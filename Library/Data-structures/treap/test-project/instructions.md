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
- **Insertion Demo:** The program inserts a fixed list of integer keys into a fresh in-memory Treap.
- **BST Sequence Verification:** It prints the Treap keys using an in-order traversal to show that the BST ordering is preserved even though node priorities are randomized.
- **Search/Delete Checks:** The script exercises basic search and delete operations on some of the inserted keys so you can see how the structure updates between traversals.
- **Exploring Further:** If you want to experiment with error handling (for missing keys, etc.) or randomized deletion patterns, you can extend `app.py` with additional operations and re-run the script to observe the results.
