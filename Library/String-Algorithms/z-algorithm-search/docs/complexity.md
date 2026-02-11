# Complexity Analysis: Z-Algorithm

The Z-Algorithm is a state-of-the-art string matching algorithm. Its primary strength is achieving a linear time complexity while remaining more conceptually accessible than the Knuth-Morris-Pratt (KMP) algorithm.

## 1. Time Complexity

| Component                | Complexity | Description                                         |
| ------------------------ | ---------- | --------------------------------------------------- |
| **Z-Array Construction** |            | Building the Z-array for the concatenated string.   |
| **Pattern Search**       |            | Iterating through the Z-array to identify matches.  |
| **Total Time**           | \*\*\*\*   | Where is the text length and is the pattern length. |

### 1.1 The Linear Time Proof

In a naive search, we might compare the same character in the text multiple times. The Z-algorithm avoids this using the **Z-box** ():

- Every character in the string is checked for a match exactly once to potentially become the new \*\*\*\* boundary.
- Once a character is inside a Z-box, we use previously computed values to determine its in \*\*\*\* time, or we start a match that moves the boundary further.
- Since the boundary only moves from to and never moves backward, the total number of character comparisons is bounded by .

---

## 2. Space Complexity

| Requirement            | Complexity | Description                                                              |
| ---------------------- | ---------- | ------------------------------------------------------------------------ |
| **Z-Array Storage**    |            | We must store an integer for every character in the concatenated string. |
| **Search Result List** |            | Where is the number of occurrences of the pattern.                       |
| **Total Space**        | \*\*\*\*   | Linear auxiliary space.                                                  |

---

## 3. Comparison with Other Search Algorithms

| Algorithm       | Time (Best/Worst) | Space | Notable Feature                               |
| --------------- | ----------------- | ----- | --------------------------------------------- |
| **Naive**       |                   |       | Simple but slow on repetitive data.           |
| **Z-Algorithm** | \*\*\*\*          |       | Extremely fast; easier to code than KMP.      |
| **KMP**         |                   |       | Uses slightly less space than Z-Algorithm.    |
| **Boyer-Moore** |                   |       | Often faster in practice on natural language. |

---

## 4. Engineering Trade-offs

- **Memory Overhead:** Unlike the Naive or Boyer-Moore algorithms, the Z-algorithm requires space to hold the Z-array. For extremely large texts (e.g., searching a 4GB file), this might require a "sliding window" adaptation to avoid memory exhaustion.
- **Alphabet Independence:** The algorithm is independent of the alphabet size (ASCII, Unicode, Binary), making it highly versatile for raw byte searches in compiled software binaries or ML model weights.
