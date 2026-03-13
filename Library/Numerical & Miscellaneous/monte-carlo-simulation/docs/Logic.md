# Monte Carlo Simulation Logic

## 1. Introduction
The **Monte Carlo Method** is a broad class of computational algorithms that rely on repeated random sampling to obtain numerical results. The underlying concept is to use randomness to solve problems that might be deterministic in principle. It is widely used in three distinct problem classes: **optimization**, **numerical integration**, and **simulating probability distributions**.

The modern version of the Monte Carlo method was created by Stanislaw Ulam, John von Neumann, and Nicholas Metropolis in the 1940s while working on nuclear weapons projects at Los Alamos. It was named after the Monte Carlo Casino in Monaco because Ulam's uncle frequently gambled there, highlighting the method's core reliance on chance and probability.

---

## 2. Core Mathematical Foundation

The theoretical justification for Monte Carlo methods relies heavily on two foundational theorems in probability theory:

### The Law of Large Numbers (LLN)
The Weak Law of Large Numbers states that the sample average of independent and identically distributed (i.i.d.) random variables converges in probability to the expected value as the sample size $N$ goes to infinity.
$$ \lim_{N \to \infty} P\left( \left| \frac{1}{N} \sum_{i=1}^N X_i - \mu \right| < \epsilon \right) = 1 $$
*In simpler terms: The more random experiments you run, the closer your average result will be to the true theoretical expected value.*

### The Central Limit Theorem (CLT)
The CLT states that the distribution of the sum (or average) of a large number of independent, identically distributed variables will be approximately normally distributed, regardless of the underlying distribution. This helps quantify the *error* bounds of a Monte Carlo simulation.

---

## 3. Key Implementations and Logic

Our core code implements three classic scenarios to demonstrate Monte Carlo logic.

### A. Estimating $\pi$ (Numerical Integration/Area)
This is an example of using randomness to approximate a deterministic constant.

1. **The Setup:** Imagine a square centered at $(0,0)$ with side lengths of 2. The area is $2 \times 2 = 4$. Inside this square, a circle of radius $r=1$ is inscribed. The area of the circle is $\pi r^2 = \pi(1)^2 = \pi$.
2. **The Logic:** If you randomly drop a point inside the square, the probability that the point lands inside the inscribed circle is the ratio of their areas:
   $$ P(\text{inside circle}) = \frac{\text{Area of Circle}}{\text{Area of Square}} = \frac{\pi}{4} $$
3. **The Simulation:**
   - Generate points $(x, y)$ where both $x$ and $y$ are uniformly distributed between $-1.0$ and $1.0$.
   - Check if the point falls inside the circle using the Pythagorean theorem: $x^2 + y^2 \leq 1$.
   - Tally the points inside the circle vs total points.
   - Multiply the ratio by 4 to estimate $\pi$.

### B. 1D Random Walk (Stochastic Processes)
A random walk describes a path that consists of a succession of random steps on some mathematical space.

1. **The Setup:** A particle begins at $x=0$.
2. **The Logic:** At every discrete time step, flip a fair coin. 
   - Heads: Move forward one step ($+1$).
   - Tails: Move backward one step ($-1$).
3. **The Expectation:** 
   - Since the coin is fair, the *expected value* of the final position after $N$ steps is strictly $0$.
   - However, the expected *absolute distance* from the origin boundedly grows. Statistically, the distance scales proportionally to the square root of the number of steps: $E[|S_N|] \approx \sqrt{2N / \pi}$.

### C. Geometric Brownian Motion (Financial Modeling)
This demonstrates a highly practical application: modeling stock market behavior to price options (e.g., Black-Scholes).

1. **The Setup:** An asset starts at an initial price $S_0$. We want to predict its price at time $t$ in the future.
2. **The Logic:** Stock returns are assumed to be normally distributed. The Geometric Brownian Motion (GBM) model assumes that a stock's percentage return over a small interval $dt$ has two components:
   - A deterministic "drift" (the expected average return, $\mu$).
   - A stochastic "shock" (the volatility, $\sigma$, multiplied by a random normal variable).
   The discrete formula for the price step is:
   $$ S_{t+dt} = S_t \times \exp{\left( (\mu - \frac{\sigma^2}{2})dt + \sigma \sqrt{dt} Z \right)} $$
   Where $Z \sim \mathcal{N}(0, 1)$ is a standard normal random variable.
3. **The Simulation:**
   - Generate thousands of independent "paths" calculating discrete steps day-by-day.
   - Average the final prices to find the expected future value. By discounting this expected value, financial analysts can price complex derivatives.

---

## 4. Advantages of Monte Carlo
1. **Curse of Dimensionality:** Unlike deterministic numerical integration (like the Trapezium rule or Simpson's rule) which scales exponentially poorly in higher dimensions, Monte Carlo integration scales beautifully regardless of dimension count.
2. **Flexibility:** It can handle highly non-linear functions, obscure probability distributions, and chaotic systems without requiring closed-form analytical equations.

## 5. Summary
The Monte Carlo algorithm relies on the fact that macroscopic truths can be revealed by averaging a massive quantity of microscopic, chaotic, random events. By leveraging modern computing power to brute-force millions of randomized scenarios, we converge on accurate answers to otherwise intractable problems.