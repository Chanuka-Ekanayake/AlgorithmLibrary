# numerical-analysis / Kahan Summation

## Summary

This repository directory implements the **Kahan Summation Algorithm** in native Python. This algorithm (occasionally referred to mathematically as *compensated summation*) was conceived specifically to radically reduce precision errors found constantly when summating finite-precision float structures within computer science applications.

While modern architectures feature powerful FPU cores, the cyclic issue of adding massively disparate exponents triggers low-order truncation. Kahan discovered that by keeping a running "compensation variable" containing the negative inversion of those dropped bits, accuracy could be maintained reliably.

---

## Directory Structure Overview

The codebase is structured identically targeting standard algorithmic library constraints:

- `core/`: The functional implementations. Contains the `KahanAccumulator` loop logic structure.
- `docs/`: Extensive deep dives into mathematical logic vectors, as well as Big-O analytical bounds concerning speed execution and memory blocks.
- `test-project/`: A robust standalone application to prove algorithmic precision using CLI benchmark metrics. 

---

## How Catastrophic Cancellation Occurs

When operating heavily cyclic integrations:
$$ \Sigma_{i=1}^{n} (x_i) $$

Adding $10000.0$ and $0.0001$ evaluates identically as `10000.0` in severe precision constraints because the smaller integer slides completely beyond the fractional tail registers. Standard float types typically truncate everything rightward of 24 to 53 boundaries. When doing numerical simulations tracking millions of points, these microscopic fractional losses rapidly sum together to wildly derail outputs.

---

## Quick Start API Guide

To utilize the core structures inside your local python codebase, simply reference the module directly. We offer two paradigms dependent on consumer constraints:

### Functional Mode
Best executed when your variables are completely loaded sequentially inside an operational array or iterable format blocks.

```python
from kahan_summation.core import kahan_sum

values = [0.1] * 10
# Standard python sum may return: 0.9999999999999999
perfect = kahan_sum(values)
print(perfect) # Outputs strictly 1.0!
```

### Accumulator / Stateful Mode
Best utilized operating standard continuous data stream pipes or websocket listener logic where variables arrive asynchronously across temporal boundaries and cannot be loaded entirely bounding RAM limits.

```python
from kahan_summation.core import KahanAccumulator

accum = KahanAccumulator(initial_value=0.0)

def block_receiver(number):
    accum.add(number)
    print(f"Current Precision Sum: {accum.get_sum()}")
```

---

## References & Scientific Literature

This core implementation heavily borrows from the standardized academic literature structures surrounding algorithmic stabilization structures:

1. **William Kahan**: "Further remarks on reducing truncation errors." *Communications of the ACM* (1965)
2. **Nicholas J. Higham**: "The accuracy of floating point summation." *SIAM Journal on Scientific Computing* (1993)
3. **Arnold Neumaier**: "Rundungsfehleranalyse einiger Verfahren zur Summation endlicher Summen." *ZAMM* (1974)

## Performance Implications
As rigorously documented within `docs/complexity.md`, consumers utilizing this algorithmic repository should recognize the fundamental $4\times$ computational calculation expansion per array. Hardware pipelines lacking dedicated parallel cycle execution blocks might constraint primary thread limitations heavily loops are implemented indiscriminately globally. Consider bounding Kahan equations strictly where precision trumps temporal speed!

## Licensing Details
See repository root configurations referencing explicit bounds open source contribution limitations. Standard MIT structures applied universally across subdirectories sequentially.

---

## Frequently Asked Questions

### Is Kahan Summation slower than standard addition?
Yes. Due to the requirement of executing four distinct mathematical instructions per cyclic addition (one addition, three subtractions) versus purely a singular standard addition step, runtime normally scales by a constant multiplicative delay of up to $4.0\times$.

### Does Python already utilize this feature natively?
Yes! The Python standard module `math` exposes a method named `math.fsum()` which executes a mathematically identical tracking technique internally bounded within underlying C execution threads. This repository serves identically as the programmatic logical equivalence of that hidden function explicitly unpacked natively inside python! 

### When does Kahan Summation fundamentally fail to secure precision?
If you are adding numerical volumes spanning ranges breaching language limit absolute boundaries. For instance, creating numerical calculations breaching standard $10^{308}$ boundaries triggers language-defined `Infinity` objects. No algorithm resolving `Infinity - Infinity` can restore data structures post-collapse. For bounded data limits, generalized variants prevent isolated condition collapses safely guaranteeing convergence.
