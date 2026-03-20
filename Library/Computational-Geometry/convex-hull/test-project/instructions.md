# Convex Hull - Running the Test Project

## 1. Prerequisites

- **Python 3.x**

---

## 2. Instructions

To verify the Convex Hull implementation:

1.  Navigate to the `test-project` directory:
    ```bash
    cd "Library/Computational-Geometry/convex-hull/test-project"
    ```
2.  Run the test script:
    ```bash
    python app.py
    ```

---

## 3. Interpreting Results

The script runs three primary scenarios:
1.  **Square Points**: Verifies that interior points (like (5,5)) are correctly excluded.
2.  **Linear Points**: Checks handling of collinear points (only the endpoints should form the hull).
3.  **Scattered Points**: A standard set of random points to verify general correctness.
