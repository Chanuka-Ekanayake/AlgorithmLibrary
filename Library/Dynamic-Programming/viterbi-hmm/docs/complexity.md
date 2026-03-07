# Complexity Analysis: Viterbi HMM Decoder

The Viterbi algorithm uses a beautiful combination of memoization and optimal substructure to drastically reduce the complexity of sequence decoding. Without it, verifying the probabilities of all possible hidden state sequences over an observation set would result in exponential time, effectively rendering the algorithm useless for reasonably sized data inputs.

## Variables

Let's rigorously define the variables dictating our model size:
-   **$|S|$ (or $N$)**: The absolute number of unique hidden states in the system.
-   **$|O|$ (or $T$)**: The length of the observation sequence needing to be decoded.
-   **$|U|$**: The number of unique observation symbols that exist in total. 

Variables that are effectively O(1) inside looping logic but important for space:
- **$\pi$ matrix**: 1D list of length $|S|$ mapping starting index initial probabilities.
- **$A$ matrix**: 2D grid matrix of size $|S| \times |S|$ governing Transition Probabilities.
- **$B$ matrix**: 2D grid matrix of size $|S| \times |U|$ governing Emission Probabilities.

---

## Time Complexity: $O(|S|^2 \cdot T)$

The Viterbi decoding logic occurs across distinct phases: Initialization, Recursion, Termination, and Path Tracing. Let's break down the execution time step-by-step.

### 1. Initialization Step
-   For each of the $|S|$ hidden states, we multiply the initial probability by the emission probability of the very first observed symbol out of the $|O|$ observations. 
-   This loops precisely $|S|$ times.
-   **Complexity:** $O(|S|)$

### 2. Recursion Step
-   We iterate through the rest of the observations starting from time $t=1$ to $T$ (so roughly $T$ iterations).
-   Inside each time step, we evaluate the maximum probability of arriving at *each* potential target state, meaning we map over the $|S|$ possible target states.
-   For *each* of those target states we must look back at all originating $|S|$ possible configurations from time $t-1$ to see which originating state yielded the overall maximum combined (prior probability * transition matrix value * emission matrix value) outcome.
-   Summarily, for $T$ time iterations, we run a nested loop of size $|S|$ inside of another nested loop of size $|S|$.
-   **Complexity:** $O(|S|^2 \cdot (T - 1))$ which translates asymptotically directly to $O(|S|^2 \cdot T)$.

### 3. Termination Step
-   When all time iterations conclude, we merely scan the final $t = T$ column to determine which of the $|S|$ final states held the maximum accumulative probability.
-   **Complexity:** $O(|S|)$

### 4. Backtracking (Path Reconstruction) Step
-   With the best final state obtained, we merely follow the cached pointer matrix tracing the route backward step-by-step for $T$ length iterations. 
-   **Complexity:** $O(T)$

### Overall Time Conclusion
Summing the phases: $O(|S|) + O(|S|^2 \cdot T) + O(|S|) + O(T) = O(|S|^2 \cdot T)$.

Because $T$ tends to be long in practical applications, and $|S|$ tends to be relatively small (for instance, $|S| = 2$ for Weather, $|S| \approx 40$ for Part Of Speech tagsets), this complexity generally scales gracefully in practice compared to the exponential nightmare $O(|S|^T)$ of a naive brute-force decoding matrix!

---

## Space Complexity: $O(|S| \cdot T)$

The Viterbi decoder specifically caches intermediate computations so it doesn't need to recursively branch calculate.

### What MUST be stored in memory inside `decode()`?
1.  **Value Matrix (V)**: A table where rows are the hidden states and columns are the observation times $t$. This grid physically houses $|S| \times T$ floating-point elements representing max probabilities.
    -   Memory: $O(|S| \cdot T)$
2.  **Backpointer Matrix (Bptr)**: A table identical in scalar dimensions to V, except it houses strings/ints pointing back to the parent target state that resulted in the cell's probability. 
    -   Memory: $O(|S| \cdot T)$
3.  **HMM Definitions**: The initial grids holding state names ($|S|$), observations ($|U|$), Transition probabilities ($|S|^2$), and Emission probabilities ($|S| \times |U|$).
    -   Memory: $O(|S|^2 + |S| \times |U|)$

### Overall Space Conclusion
Asymptotically, for a fixed model, the state dimensions and alphabet dictionary do not scale as we decode different observations sequences. Thus $O(|S|^2)$ is treated as constant.

The matrices actively tracking the dynamic calculation logic are what scale proportional with sequence input length $T$. 
Overall Space Complexity = $O(|S| \cdot T)$.

---

## Sparse Matrix Optimization Notes

### Log-Space Operations
A major consideration missing from standard $O()$ syntax revolves around the floating-point multiplication of hundreds of small fractions, leading immediately to CPU Underflow. The standard workaround to transform the execution to *Log-Space* means execution loops operate via addition (`prev_V + transition_V + emit_V`) rather than multiplication.
While adding logarithmic floats requires exactly the same asymptotic operations as multiplication float algebra, CPU architecture significantly prefers executing the integer combinations avoiding underflow exceptions inside nested registers.

### Sparsity
If the Transition matrix $A$ or Emission matrix $B$ are extremely sparse (lots of 0.0 value probability chances), evaluating state combinations that mathematically equal $0.0$ wastes clock cycles. 
By maintaining adjacent dictionary mappings linking only "valid connected states," you can drop the $O(|S|^2 \cdot T)$ complexity down into proportional ranges resembling $O(E \cdot T)$, where $E$ represents the distinct count of valid transitions.
