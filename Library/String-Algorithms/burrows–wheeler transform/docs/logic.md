# Algorithm Logic: Burrows-Wheeler Transform (BWT)

The BWT does not compress data. It is a data _rearrangement_ algorithm. Its sole purpose is to take a string and shuffle its characters so that identical bytes sit next to each other, creating "runs" of data (e.g., `...aaaaabbbb...`) that are highly compressible by secondary algorithms.

## 1. The Forward Transform (The Setup)

To understand how BWT works, let's transform the string `banana`.
First, we append our unique End-Of-File marker: `banana$`.

The algorithm executes three steps:

1. **Rotate:** Generate every possible cyclic permutation (rotation) of the string.
2. **Sort:** Sort those rotations alphabetically.
3. **Extract:** Take only the **Last Column** of the sorted matrix.

### The BWT Matrix

Here is what the matrix looks like before and after sorting:

| Unsorted Rotations |     | Sorted Rotations | First Column (F) | Last Column (L) |
| ------------------ | --- | ---------------- | ---------------- | --------------- |
| `banana$`          |     | `$banana`        | **$**            | **a**           |
| `anana$b`          |     | `a$banan`        | **a**            | **n**           |
| `nana$ba`          |     | `ana$ban`        | **a**            | **n**           |
| `ana$ban`          |     | `anana$b`        | **a**            | **b**           |
| `na$bana`          |     | `banana$`        | **b**            | **$**           |
| `a$banan`          |     | `na$bana`        | **n**            | **a**           |
| `$banana`          |     | `nana$ba`        | **n**            | **a**           |

**The Output:** The BWT string is the Last Column: `annb$aa`.
Notice how the `n`s and `a`s have started to group together. In a file with millions of characters, this grouping effect becomes massive.

---

## 2. Why Do Characters Group Together?

This is the genius of the BWT. Look at the sorted matrix.

Because we sorted the matrix alphabetically, rows that start with the same sequence of characters are grouped together. For example, rows starting with `an` are adjacent.

Because these are _cyclic_ permutations, the character in the **Last Column** is always the character that immediately _preceded_ the First Column in the original string.

- What usually precedes `an` in the word `banana`? The letter `n`.
- What usually precedes `the` in an English text? A space (` `).

By sorting the contexts (the suffixes), we naturally pull all the identical preceding characters into a unified block in the last column.

---

## 3. The LF Mapping (The Magic Trick)

How do we get `banana` back if we only have the string `annb$aa`? We use the **Last-to-First (LF) Mapping** property.

If you have the Last Column (`L`), you can easily figure out the First Column (`F`) just by sorting `L` alphabetically.

**The Golden Rule of BWT:**

> _The -th occurrence of a character in the Last column corresponds to the exact same original character as the -th occurrence of that character in the First column._

Let's look at the `n`s in our `banana$` example:

- The **1st 'n'** in the Last Column is at index 1.
- The **2nd 'n'** in the Last Column is at index 2.
- The **1st 'n'** in the First Column is at index 5.
- The **2nd 'n'** in the First Column is at index 6.

Because of the cyclic sorting, the **1st 'n' in L** is mathematically guaranteed to be the exact same physical byte as the **1st 'n' in F**.

### Reconstructing the String

To rebuild the string, we just bounce back and forth between L and F:

1. Start at the `$` in F. The character in L in that same row is `a`. (String so far: `a`)
2. That `a` is the _1st 'a'_ in L. Find the _1st 'a'_ in F. The character in L in that row is `n`. (String so far: `na`)
3. That `n` is the _1st 'n'_ in L. Find the _1st 'n'_ in F. The character in L in that row is `a`. (String so far: `ana`)

You repeat this pointer jump exactly times, and the original string materializes in reverse order.
