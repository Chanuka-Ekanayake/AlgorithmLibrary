# User Guide: The Collaborative Shopping List (CRDT)

This project demonstrates **Conflict-free Replicated Data Types** by simulating three users (Alice, Bob, and Carol) independently editing a shared shopping list while fully offline — then merging without any conflicts.

## What You'll See

The simulation runs four demos in sequence:

1. **G-Counter:** Distributed page-view counting across 3 CDN edge nodes.
2. **PN-Counter:** Warehouse inventory tracking with independent sales.
3. **LWW-Register:** User profile theme sync between phone and laptop.
4. **OR-Set (Main Demo):** The Collaborative Shopping List — three devices go offline, make conflicting edits, come back online, and merge with zero conflicts.

## How to Test

1. **Navigate** to the `test-project` folder.
2. **Run** the simulator:
   ```bash
   python app.py
   ```

## Key Conflict to Watch

In the OR-Set demo, pay close attention to **"Bread"**:
- Alice **removes** "Bread" (going gluten-free)
- Bob **adds** "Bread" (concurrently, without knowing Alice removed it)
- Result: "Bread" **survives** — the OR-Set's "add-wins" semantics ensure that concurrent adds always beat concurrent removes.

This is the core insight of CRDTs: conflicts are resolved by mathematical guarantees, not by human intervention.

## No Dependencies

This project uses only Python standard library modules. No `pip install` required.
