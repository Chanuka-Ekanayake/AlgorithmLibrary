# Algorithm Logic: Fenwick Tree (BIT)

A Fenwick Tree is technically a tree, but it is stored entirely in a flat, 1-dimensional array. The "parent" and "child" relationships between the nodes are not explicitly stored; instead, they are mathematically calculated on the fly using the binary representation of their array index.

## 1. The Core Concept: "Responsibility"

In a standard array, index 5 stores exactly one value: the value at day 5.
In a prefix array, index 5 stores the sum of all values from day 1 to day 5.

In a Fenwick Tree, index 5 stores a specific "chunk" of the sum. The size of that chunk is determined entirely by the **Least Significant Bit (LSB)** of the index.

- **Index 8 (Binary `1000`)**: The LSB is 8. Therefore, index 8 is "responsible" for 8 elements. It holds the sum of elements 1 through 8.
- **Index 10 (Binary `1010`)**: The LSB is 2. Therefore, index 10 is responsible for exactly 2 elements. It holds the sum of elements 9 and 10.
- **Index 11 (Binary `1011`)**: The LSB is 1. Therefore, index 11 is responsible for exactly 1 element. It holds only the value of element 11.

---

## 2. The Bitwise Magic: Isolating the LSB

To navigate the tree, the algorithm must instantly find the LSB of any given index. It does this using the Two's Complement bitwise operation:

**Why does this work?**
In computer memory, negative numbers are stored using Two's Complement. To make a number negative, you flip all the bits and add 1.

Let's look at the index 10 (Binary `1010`):

1. **Original:** `0000 1010` (Decimal 10)
2. **Flip bits:** `1111 0101`
3. **Add 1 (to complete two's complement):** `1111 0110` (Decimal -10)
4. **Bitwise AND:** `0000 1010 & 1111 0110`

```text
  0000 1010  (10)
& 1111 0110  (-10)
-----------
  0000 0010  (2)

```

The bitwise `AND` operation perfectly isolated the Least Significant Bit. For index 10, the LSB is **2**.

---

## 3. Querying: Subtracting the LSB

When you want to know the sum from index 1 to 11, you don't iterate from 1 to 11. You start at 11 and continuously **subtract** the LSB until you hit 0.

**Query(11):**

- Start at **11** (`1011`). It is responsible for 1 element. Add `tree[11]` to the total.
- Subtract LSB (1). Move to **10**.
- Current index is **10** (`1010`). It is responsible for 2 elements. Add `tree[10]` to the total.
- Subtract LSB (2). Move to **8**.
- Current index is **8** (`1000`). It is responsible for 8 elements. Add `tree[8]` to the total.
- Subtract LSB (8). Move to **0**.
- Done.

By adding the values stored at indices 11, 10, and 8, you successfully gathered the sum of all 11 elements in just 3 steps.

---

## 4. Updating: Adding the LSB

When you update the value at index 5, you must also update every "parent" node that includes index 5 in its responsibility range. To find the parents, you continuously **add** the LSB until you exceed the size of the array.

**Update(5, delta):**

- Start at **5** (`0101`). Add delta to `tree[5]`.
- Add LSB (1). Move to **6**.
- Current index is **6** (`0110`). Add delta to `tree[6]`.
- Add LSB (2). Move to **8**.
- Current index is **8** (`1000`). Add delta to `tree[8]`.
- Add LSB (8). Move to **16**.
- (Continue until the array boundary is reached).

Instead of updating everything after index 5, you only updated the specific binary parent nodes, completing the operation in **O(log n)** time.
