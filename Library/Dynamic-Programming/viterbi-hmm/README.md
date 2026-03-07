# Viterbi Hidden Markov Model Decoder

Welcome to the **Viterbi HMM Decoder** project!

This sub-repository implements the acclaimed Viterbi Decoding algorithm, heavily utilized in statistical Natural Language Processing (NLP), sequence analysis in computational biology, and telecommunications error-correction.

## Overview and Background

The Viterbi algorithm is fundamentally a dynamic programming mechanism. It was formulated by Andrew Viterbi while he was looking for a solution to decode convolutional error-correcting codes. It elegantly bypasses exponential-time brute force evaluations and provides the single most optimal, maximum-likelihood sequence of hidden states matching an observed phenomenon by strictly caching maximum intermediary thresholds (a concept known interchangeably as Memoization).

Instead of scoring $O(|S|^T)$ different potential state paths—which is nearly physically impossible even for modern supercomputers operating on modest sequence lengths of $T=1000$ and $|S|=40$ states—dynamic programming guarantees an absolute answer in merely $O(|S|^2 \cdot T)$ computations safely shielding the CPU from combinatorial explosion.

Our implementation here offers a generalized Python solver strictly utilizing raw probabilities (for absolute beginner algorithmic demonstration purposes) rather than logarithmic-space scaling. The concepts are identically mapped to academic logic diagrams.

## Key Directory Structure

```text
viterbi-hmm/
├── README.md               # You are here. Detailed usage outline.
├── core/
│   ├── __init__.py         # Package initialization exposing ViterbiDecoder. 
│   └── decoder.py          # The core DP engine generating the Viterbi tables and tracing paths.
├── docs/
│   ├── logic.md            # Heavy mathematical rigor validating Markov Property formulas.
│   └── complexity.md       # Full runtime Time/Space asymptotic analysis.
└── test-project/
    ├── app.py              # An executable showcasing two distinct HMM scenarios (Weather & POS Tagging).
    └── instructions.md     # Guidelines regarding testing outputs and terminal usage execution.
```

## Setup & Execution Context 

Ensure you have a modern Python 3.7+ distribution available within your environment.

No exterior PIP packages (such as `numpy`, `pandas` or `scikit-learn`) are mandated for this implementation. Everything utilizes pure Python standard library types (`List`, `Dict`, `Tuple`) strictly adhering to structural type hints defined in `typing`.

## Rapid API Usage Tutorial

### 1. Identify Your Environment Spaces

A Hidden Markov Model strictly needs Definition spaces.
```python
# S = The categorical variables you are trying to guess.
states = ['Rainy', 'Sunny']

# O = The categorical variables you literally witnessed.
observations = ['walk', 'shop', 'clean']
```

### 2. Define Boundary Probabilities

Next, we establish the matrix definitions detailing the Markov transition matrices.

```python
start_probability = {
    'Rainy': 0.6,
    'Sunny': 0.4
}

transition_probability = {
    'Rainy': {'Rainy': 0.7, 'Sunny': 0.3},
    'Sunny': {'Rainy': 0.4, 'Sunny': 0.6},
}

emission_probability = {
    'Rainy': {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
    'Sunny': {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
}
```

### 3. Initialize & Execute

Import the class logic and spawn the engine. You can subsequently pass arbitrary observation sequence strings to the decoder to retrieve your hidden variables!

```python
from core.decoder import ViterbiDecoder

viterbi_engine = ViterbiDecoder(
    states=states,
    observations=observations,
    start_prob=start_probability,
    transition_prob=transition_probability,
    emission_prob=emission_probability
)

# Friend was witnessed performing these actions in order
events = ['walk', 'shop', 'clean']

# What was the likely weather outside?
likely_weather, final_prob = viterbi_engine.decode(events)

print("Best Path:", likely_weather)
print("Probability:", final_prob)
```

## Educational Caveat

This project is tuned explicitly for Algorithm Library educational transparency.
1. We check float summing explicitly without dropping missing matrices.
2. We iterate fully out across the inner loop matching the $O(S^2 T)$ logic, maintaining strict memory pointers rather than abstract vector operations. 
3. Production pipelines utilizing Viterbi decoders almost universally operate in `(-)` Log Space and leverage the `numpy` numerical suite for C-bindings, drastically changing the syntax compared to exactly what happens behind the hood!

## Testing Check
For verifying full environment operations, please execute:
`python test-project/app.py`
