# Viterbi Algorithm Logic & Mathematics

The **Viterbi algorithm** is a dynamic programming algorithm used to find the most likely sequence of hidden states (the Viterbi path) in a Hidden Markov Model (HMM) given a sequence of observed events.

This document serves to rigorously explain the logic and flow of the algorithm.

## Background: Hidden Markov Models

Before diving into Viterbi, we must firmly establish what an HMM is. An HMM is characterized by the tuple $\lambda = (S, V, A, B, \pi)$, where:

1.  $S = \{s_1, s_2, \dots, s_N\}$ is a finite set of $N$ states. These states are completely "hidden" to the final observer.
2.  $V = \{v_1, v_2, \dots, v_M\}$ is a finite set of $M$ possible observation symbols. These are what the observer actually sees.
3.  $A = [a_{ij}]$ is the state transition probability matrix. $a_{ij}$ represents the true probability of moving from state $s_i$ at time $t$ to state $s_j$ at time $t+1$.
    $$a_{ij} = P(q_{t+1} = s_j | q_t = s_i)$$
4.  $B = [b_j(k)]$ is the observation emission probability matrix. $b_j(k)$ represents the probability of observing symbol $v_k$ when currently in state $s_j$.
    $$b_j(k) = P(o_t = v_k | q_t = s_j)$$
5.  $\pi = [\pi_i]$ is the initial state probability distribution.
    $$\pi_i = P(q_1 = s_i)$$

Given a sequence of observations $O = (o_1, o_2, \dots, o_T)$ and an HMM model $\lambda$, the Viterbi algorithm solves the general decoding problem:  
**What is the single most probable sequence of hidden states $Q = (q_1, q_2, \dots, q_T)$ that corresponds to the observations?**

---

## Dynamic Programming Formulation

Solving this naively by analyzing every single possible state path requires calculating $N^T$ paths, a computationally infeasible task (exhibiting exponential explosion). The Viterbi algorithm tackles this by leveraging **optimal substructure**. The core realization is that the most likely path to a certain state $s_j$ at time $t$ uniquely stems from the most likely path to some specific state at time $t-1$.

To establish the recurrences, we define two critical variables for our lookup tables (the DP cache):

### Value Matrix ($V$)
Let $V_t(j)$ be the maximum probability of any sequence of states ending at state $s_j$ at time $t$, jointly with the generated observation sequence $o_1, \dots, o_t$.

$$V_t(j) = \max_{q_1, q_2, \dots, q_{t-1}} P(q_1 \dots q_{t-1}, q_t = s_j, o_1, o_2 \dots o_t | \lambda)$$

### Backpointer Matrix ($Bptr$)
Let $Bptr_t(j)$ simply be the index of the state at time $t-1$ that ultimately maximized the probability evaluated in $V_t(j)$. This is an array strictly used to trace the optimal path backward after we finish calculations.

$Bptr_t(j)$ does not hold a mathematical weight, instead holding the categorical state label from $t-1$.

---

## Algorithm Execution Steps

### Step 1: Initialization ($t = 1$)

For time $t=1$, we calculate the probability of starting in each state and immediately emitting the first observed symbol, $o_1$. We initialize our two tables for all $1 \le j \le N$.

$$V_1(j) = \pi_j \cdot b_j(o_1)$$
$$Bptr_1(j) = 0 \text{ (or None)}$$

*(This assumes index starts at 1. The first states have no preceding states, hence None).*

### Step 2: Recursion ($t = 2, 3, \dots, T$)

For each subsequent time step $t$, we iterate over all possible states $s_j$ we could end up in. We want to find the best previous path that could lead us there. For each $j$:

$$V_t(j) = \max_{1 \le i \le N} \left( V_{t-1}(i) \cdot a_{ij} \cdot b_j(o_t) \right)$$

Simultaneously, we maintain the backpointers by storing the specific $i$ that triggered the maximum:

$$Bptr_t(j) = \underset{1 \le i \le N}{\mathrm{argmax}} \left( V_{t-1}(i) \cdot a_{ij} \right)$$
*(Note: we technically do not need to multiply by $b_j(o_t)$ for the argmax calculation because the emission probability is constant irrespective of the preceding state $i$).*

### Step 3: Termination ($t = T$)

When we finish iterating through all observations, the overall maximum path probability rests in the final time column $T$.

$$P^* = \max_{1 \le i \le N} V_T(i)$$

The final state in our optimal sequence is simply the argument that yields that max:

$$q_T^* = \underset{1 \le i \le N}{\mathrm{argmax}} \ V_T(i)$$

### Step 4: Backtracking (Path Reconstruction)

Starting with our optimal ending state $q_T^*$, we follow our backpointers in reverse chronological order to deduce the best sequence.

For $t = T-1, T-2, \dots, 1$:

$$q_t^* = Bptr_{t+1}(q_{t+1}^*)$$

The optimal path is thus $Q^* = (q_1^*, q_2^* \dots, q_T^*)$.

---

## Differences Between Forward Algorithm and Viterbi

It is common to confuse the Viterbi algorithm with the Forward algorithm for HMMs. 
- **Forward algorithm** calculates the generalized likelihood of an observation sequence, marginalizing over *all* possible hidden state sequences. Its recurrence relation uses sums ($\sum$) over previous variables, yielding the cumulative sum of probabilities of all paths. 
- **Viterbi algorithm** calculates the likelihood of the *single most probable sequence*. Instead of marginalizing across paths using sums, it operates strictly via maximums ($\max$) keeping only the winning sub-path at each recursive branch. This distinct replacement of summation with maximization is what guarantees the specific single-best path.

## Why Does This Work?

The Viterbi algorithm works because of the Markov property. The Markov property dictates that the future evolution of the process depends strictly upon the current state and is independent of the sequence of states that preceded it.

If the best path to node `B` at $t=2$ passes through `A` at $t=1$, and the most probable path overall ends at node `C` at $t=3$ by passing through `B` at $t=2$, then the sub-path `A -> B` MUST be explicitly part of the total path `A -> B -> C`. There's no situation where replacing the optimal chunk to `B` dynamically improves the ending condition at `C`, because everything past `B` strictly reacts to the current node `B` itself, not its arbitrary history. 
This exact rationale is the core philosophy defining Dynamic Programming.
