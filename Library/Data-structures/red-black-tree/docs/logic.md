# Red-Black Tree — Core Logic

## Overview

A Red-Black Tree (RBT) is a self-balancing Binary Search Tree (BST). Every node carries an extra bit of information — its **color** (RED or BLACK). By enforcing a strict set of coloring rules, the tree guarantees that no root-to-leaf path is more than twice as long as any other, keeping the height bounded at $O(\log n)$ for *any* sequence of insertions and deletions.

This is in contrast to a Treap, which achieves balance only *in expectation* via randomized priorities. A Red-Black Tree provides a **deterministic worst-case** guarantee.

---

## The Four Invariants

Every valid Red-Black Tree satisfies these invariants at all times:

| # | Rule |
|---|------|
| 1 | Every node is either **RED** or **BLACK**. |
| 2 | The **root** is always **BLACK**. |
| 3 | No two **consecutive RED** nodes may appear on any root-to-leaf path (a RED node's parent and both children must be BLACK). |
| 4 | Every root-to-leaf path (including paths to the sentinel NIL leaves) must contain the **same number of BLACK nodes** — this count is called the **black-height**. |

These four rules together bound the worst-case tree height to $2 \log_2(n+1)$.

---

## Sentinel NIL Node

Rather than using Python `None` as leaf pointers, the implementation uses a single shared **sentinel `NIL` node** (colored BLACK). Every real node's `left`, `right`, and `parent` fields point to this sentinel when no real child / parent exists. This eliminates a large number of null-checks inside the rotation and fixup routines.

---

## Operations

### Search
Identical to a standard BST search — follow left/right based on key comparisons. The RBT's height constraint guarantees $O(\log n)$ comparisons.

### Insert
1. **BST-insert** the new node as RED (inserting RED never breaks invariant #4, since no BLACK count changes).
2. If the new node's parent is also RED, **invariant #3 is violated**. Restore it via `_fix_insert`:

#### Insert Fixup — 3 Cases (and their mirrors)
Let `z` be the inserted RED node and `u` be its uncle (parent's sibling):

| Case | Condition | Action |
|------|-----------|--------|
| **1** | Uncle `u` is RED | Recolor parent and uncle BLACK, grandparent RED. Push violation up to grandparent. |
| **2** | Uncle `u` is BLACK, `z` is an *inner* grandchild (parent is left child but `z` is right child, or vice-versa) | Rotate parent in the direction that makes `z` an outer grandchild. Falls into Case 3. |
| **3** | Uncle `u` is BLACK, `z` is an *outer* grandchild | Recolor parent BLACK, grandparent RED. Rotate grandparent outward. Done. |

Each case either terminates immediately or moves the violation two levels up the tree, so the total number of rotations is at most 2.

### Delete
1. **Locate** the node to remove.
2. If it has two children, replace its key/value with those of its **in-order successor** (the leftmost node in its right subtree), then delete the successor instead (which has at most one child).
3. **Splice out** the node with `_transplant`. If the removed node was **RED**, no invariants break — done. If it was **BLACK**, one path has lost a black node — call `_fix_delete`.

#### Delete Fixup — 4 Cases (and their mirrors)
Let `x` be the node that moved into the deleted position (it carries a "double black" deficit). Let `w` be x's sibling:

| Case | Condition | Action |
|------|-----------|--------|
| **1** | `w` is RED | Rotate parent toward `x`. `w` becomes BLACK, parent becomes RED. Converts to Cases 2–4. |
| **2** | `w` is BLACK, both of `w`'s children are BLACK | Recolor `w` RED. Push deficit up to parent. Continue loop. |
| **3** | `w` is BLACK, `w`'s far child is BLACK, near child is RED | Rotate `w` away from `x`. Converts to Case 4. |
| **4** | `w` is BLACK, `w`'s far child is RED | Rotate parent toward `x`. Recolor to restore balance. Terminates. |

Delete fixup performs at most 3 rotations.

---

## Why Rotations Preserve BST Order

A rotation is a purely structural rearrangement of pointer links. During a **left rotation** on node `x` (with right child `y`), node `y` takes `x`'s position, `x` becomes `y`'s left child, and `y`'s original left subtree `B` becomes `x`'s right subtree. Because `B`'s keys all satisfy `x.key < B.keys < y.key`, BST order is perfectly preserved.
