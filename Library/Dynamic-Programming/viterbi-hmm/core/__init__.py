"""
================================================================================
Viterbi Algorithm & Hidden Markov Models (HMM) Optimization Library
================================================================================

This module initializes the `core` package for the Viterbi Algorithm project
within the Dynamic Programming algorithms library. It exposes the primary
`ViterbiDecoder` class which contains the computational logic.

Overview of Hidden Markov Models
--------------------------------

A Hidden Markov Model (HMM) is a statistical Markov model in which the system
being modeled is assumed to be a Markov process with unobservable (i.e., hidden)
states. While the states themselves are hidden, there is an observable process
whose outcomes depend on the hidden states. 

An HMM is strictly defined by the following components:
1.  **States (S)**: A set of hidden states. For example, in a weather model, 
    the states might be "Sunny" and "Rainy".
2.  **Observations (O)**: A set of observable events. In the weather model,
    observations might be what a person is wearing, such as "T-shirt", "Coat",
    or "Umbrella".
3.  **Initial Probabilities (PI)**: The probability that the system starts in 
    a specific state.
4.  **Transition Probabilities (A)**: The probability of moving from one hidden
    state to another. This defines the Markov chain aspect.
5.  **Emission Probabilities (B)**: The probability of observing a specific
    event given a specific hidden state.

Overview of the Viterbi Algorithm
---------------------------------

The Viterbi algorithm is a dynamic programming algorithm for finding the most 
likely sequence of hidden states (known as the Viterbi path) that results in a 
sequence of observed events, especially in the context of Markov information
sources and Hidden Markov Models.

Developed by Andrew Viterbi in 1967 as an error-correction scheme for noisy 
digital communication links, it has found universal application in decoding
the convolutional codes used in both CDMA and GSM digital cellular, dial-up
modems, satellite, deep-space communications, and 802.11 wireless LANs.

Dynamic Programming Approach:
Instead of evaluating the probabilities of every possible state sequence 
(which would be exponentially complex, O(|S|^T)), the Viterbi algorithm uses 
dynamic programming to find the maximum probability path dynamically.

It maintains two tables:
- `v[state][time]`: The maximum probability of observing the sequence up to 
  time `t` and ending in `state`.
- `ptr[state][time]`: The state at time `t-1` that maximized `v[state][time]`. 
  This backpointer table is critical for reconstructing the optimal sequence.

The algorithm runs in O(|S|^2 * T) time.

Detailed Example: Weather Prediction
------------------------------------

Imagine you are locked in a room and cannot see the weather outside. However, 
you can observe what your friend wears every day when they visit you.
- Hidden States: "Sunny", "Rainy"
- Observations: "Walk", "Shop", "Clean"

If your friend's sequence of activities for three days is ["Walk", "Shop", "Clean"],
the Viterbi algorithm can calculate the exact most likely sequence of weather 
states that occurred outside on those three days using the transition matrices 
and emission probabilities of your friend's behaviors.

Log Probabilities & Underflow
----------------------------
In real-world implementations, sequences can be hundreds or thousands of steps long.
Multiplying hundreds of small probabilities (between 0 and 1) inevitably leads to
computational underflow, where numbers become so small that floating-point 
precision registers them as absolute zero. 

To circumvent this, implementations heavily utilize logarithmic space:
Instead of: P(A) * P(B)
We compute: log(P(A)) + log(P(B))
Because log function is monotonic, the path that maximizes the sum of log-probabilities
is exactly the same path that maximizes the product of raw probabilities. 

This particular implementation, however, focuses on algorithmic clarity and
teaching the raw Dynamic Programming mechanism. We stick to raw probabilities, 
though production-level code should convert to log-space.

Usage Guidelines
----------------

1. Import the class:
   ```python
   from core.decoder import ViterbiDecoder
   ```

2. Define your states, observations, start probabilities, transition matrix, 
   and emission matrix.

3. Instantiate the decoder:
   ```python
   decoder = ViterbiDecoder(states, observations, start_p, trans_p, emit_p)
   ```

4. Decode your sequence:
   ```python
   sequence = ["obs1", "obs2", "obs3"]
   path, probability = decoder.decode(sequence)
   ```

For more documentation, please see `docs/logic.md` and `docs/complexity.md`.

Author: AlgorithmLibrary Contributor
License: MIT
"""

from .decoder import ViterbiDecoder

__all__ = ['ViterbiDecoder']

# -----------------------------------------------------------------------------
# End of __init__.py module
# -----------------------------------------------------------------------------
# The Viterbi algorithm's dynamic programming nature elegantly solves what would
# otherwise be an intractable combinatorial problem. This module serves as the 
# entry point, providing access to the core decoder logic.
# -----------------------------------------------------------------------------
