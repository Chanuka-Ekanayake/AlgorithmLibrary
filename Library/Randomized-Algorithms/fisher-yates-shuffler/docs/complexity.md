# Complexity Analysis: Fisher-Yates Shuffle

The Fisher-Yates algorithm (also known as the Knuth Shuffle) is the most efficient way to generate a random permutation of a finite sequence.

## 1. Time Complexity

| Scenario | Complexity | Description |
| --- | --- | --- |
| **Best Case** |  | The algorithm always performs exactly  swaps. |
| **Average Case** |  | Linear time complexity regardless of the initial order. |
| **Worst Case** |  | Every element is visited and potentially swapped once. |

### 1.1 Why it is Linear

The algorithm consists of a single loop that runs from the end of the array to the beginning. Inside the loop, two operations occur:

1. **Random Index Selection:** 
2. **Element Swap:** 
Since we do  work for each of the  elements, the total complexity is .

---

## 2. Space Complexity

The space complexity is:


 (Auxiliary Space)

### 2.1 In-Place Logic

* Unlike algorithms that create a new "shuffled" list by randomly picking items from a "source" list (which would require  additional space), Fisher-Yates performs all operations within the original array.
* The only memory used is for temporary variables during the swap process (an index  and a temporary storage for the value).

---

## 3. Statistical Properties

### 3.1 Unbiased Distribution

A shuffle is considered **unbiased** if every possible permutation of the list is equally likely to occur.

* For a list of size n, there are n! (n factorial) possible permutations.
* Fisher-Yates ensures that the probability of any specific permutation appearing is exactly:

  1/n!
### 3.2 Comparison with "Random Sort"

Many developers shuffle by assigning a random number to each element and sorting them (O(n log n)).

* **Efficiency:** Fisher-Yates is faster (O(n) vs O(n log n)).
* **Bias:** Sorting algorithms can introduce subtle biases depending on the sorting implementation, whereas Fisher-Yates is mathematically proven to be fair.

---

## 4. Performance Summary

| Metric | Performance |
| --- | --- |
| **Passes over data** | 1 (Single Pass) |
| **Swaps performed** | n |
| **Random numbers generated** | n |
| **Auxiliary Space** | O(1) |