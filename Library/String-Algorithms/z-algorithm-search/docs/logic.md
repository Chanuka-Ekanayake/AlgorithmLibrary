# Algorithm Logic: Z-Algorithm (Linear Search)

## 1. The Core Concept: The Z-Array

The Z-algorithm is built around a single array, the **Z-array**. For a string of length , the Z-array is defined such that is the length of the longest common prefix (LCP) between and the suffix of starting at index .

- **Example:**
- because the suffix starting at index 4 is **"aabx"**, and the first 3 characters (**"aab"**) match the prefix of .

---

## 2. The Efficiency Engine: The Z-Box

To compute the Z-array in time, the algorithm maintains a "window" called the **Z-box**, denoted by the boundaries . This box represents the rightmost substring found so far that is also a prefix of the string.

As we iterate through the string at index , there are two main logic cases:

### Case A: (Outside the Box)

If the current index is outside our known Z-box, we have no "memory" to rely on.

1. We perform a naive character-by-character comparison starting from and .
2. If we find a match, we update and to the end of the match.
3. We've created a new Z-box.

### Case B: (Inside the Box)

This is where the optimization happens. Since matches , the character at is the same as . We look at (where ).

- **Subcase B1:** If is small and fits entirely within the remaining space of the current Z-box (), then . **No new comparisons needed.**
- **Subcase B2:** If reaches or exceeds the boundary , the match _might_ continue further. We start naive comparisons from to extend the Z-box and update and .

---

## 3. The Search Strategy: The Concatenation Trick

To find a `pattern` within a `text`, we don't just compute Z-arrays for both. We use a clever concatenation:

1. **The Sentinel (`\$`):** We use a unique character that appears in neither string. This prevents a match from "bleeding" across the boundary.
2. **The Result:** Any index in the Z-array where indicates a full match of the pattern starting at that position in the text.

---

## 4. Why it Matters for Your Marketplace

In your software marketplace, users search through massive codebases (e.g., searching for the function `calculate_loss`).

- **Naive Search:** If the code has many repetitive prefixes (like thousands of lines starting with `def test_...`), a naive search slows down significantly ().
- **Z-Algorithm Logic:** Even with highly repetitive code, the Z-algorithm "jumps" through the repetitions using the Z-box memory, ensuring the search remains near-instant for the user.
