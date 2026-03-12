# Algorithm Logic: Reservoir Sampling

Reservoir Sampling is a family of randomized algorithms for choosing a simple random sample without replacement of size $k$ from a population of unknown size $n$ in a single pass over the items.

The size of the population $n$ is not known to the algorithm and is typically too large to fit all items into main memory.

---

## 1. The Problem: Sampling from a Stream

Imagine you are processing a stream of data (e.g., millions of tweets, network packets, or database rows). You want to maintain a "representative" sample of $k$ items so that at any point in time, every item seen so far has the same probability of being in your sample.

The constraints are:
1. **Single Pass:** You can only see each item once.
2. **Memory:** You can only store $k$ items at a time.
3. **Unknown $n$:** You don't know when the stream will end.

---

## 2. Algorithm R (The Simple Solution)

The most common version, Algorithm R, works as follows:

1.  **Initialization:** Fill the "reservoir" (the sample array) with the first $k$ items from the stream.
2.  **Iterative Step:** For every subsequent item at 0-based index $i$ (where $i \ge k$):
    -   Generate a random integer $j$ between $0$ and $i$ (inclusive).
    -   If $j < k$, replace the item at `reservoir[j]` with the new item.
    -   Otherwise, discard the new item.

### Why does it work? (The Proof)

To prove that the algorithm is fair, we must show that at any step $n$, the probability that any specific item is in the reservoir is exactly $k/n$.

**Base Case:** After $k$ items, every item is in the reservoir. $P = k/k = 1$. Correct.

**Inductive Step:** Assume that after $n$ items, every item has probability $k/n$ of being in the reservoir. When the $(n+1)$-th item arrives:
-   The $(n+1)$-th item is kept with probability $P(\text{keep}) = k/(n+1)$.
-   For an item already in the reservoir, it stays if:
    1.  The $(n+1)$-th item is discarded, **OR**
    2.  The $(n+1)$-th item is kept but it replaces a *different* index.

Probability an old item stays:
$$P(\text{stays}) = P(\text{discarded}) + P(\text{kept}) \times P(\text{replaced other})$$
$$P(\text{stays}) = \frac{n+1-k}{n+1} + \frac{k}{n+1} \times \frac{k-1}{k}$$
$$P(\text{stays}) = \frac{n+1-k + k-1}{n+1} = \frac{n}{n+1}$$

Total probability for an old item to be in the reservoir after $n+1$ steps:
$$P(\text{in reservoir}) = P(\text{was there after } n) \times P(\text{stays})$$
$$P(\text{in reservoir}) = \frac{k}{n} \times \frac{n}{n+1} = \frac{k}{n+1}$$

The math holds! Every item, whether it arrived first or last, has the same $k/n$ chance of being preserved.

---

## 3. Pseudocode

```text
reservoir = []
for i, item in enumerate(stream):
    if i < k:
        reservoir.append(item)
    else:
        j = random_integer(0, i)
        if j < k:
            reservoir[j] = item
return reservoir
```

---

## 4. Key Advantages

-   **Zero Prep:** Unlike some sampling methods, you don't need to know the total count beforehand.
-   **Constant Memory:** Space usage is $O(k)$, regardless of how many billions of items pass through.
-   **Unbiased:** Mathematically guaranteed to be a uniform random sample.
