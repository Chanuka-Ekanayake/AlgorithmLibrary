# Running the Suffix Array + LCP Simulator

This test project simulates a **Plagiarism Detection Engine** that finds shared substrings between submitted documents.

## Steps

1. Navigate to the `test-project` directory:

```bash
cd test-project
```

2. Run the simulator:

```bash
python app.py
```

## What to Observe

- The **Suffix Array** built for the submitted document.
- All **exact match positions** found via binary search.
- The **Longest Repeated Substring** in the submitted document.
- The **Longest Common Substring** detected between two compared documents.
- Execution time demonstrating O(N log N) construction + O(M log N) querying.
