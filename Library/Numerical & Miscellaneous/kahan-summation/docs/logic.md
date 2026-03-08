# Kahan Summation: Mathematical Logic and Proofs

## 1. Introduction

The **Kahan Summation Algorithm**, also known as **compensated summation**, was devised by William Kahan in 1965 to significantly reduce the numerical error incurred when adding a sequence of finite-precision floating-point numbers.

In standard addition, we typically maintain a running total. Due to finite-precision representation of floats in memory (such as IEEE 754 standards), a tiny fractional number added to a very large number might fall out of the register's precision bounds. In naive summation, the low-order bits of the smaller number are lost to rounding error. When this happens iteratively over thousands or millions of numbers, the total error can dwarf the actual sum.

## 2. Standard Float Limitations

Floating-point numbers are represented in memory as scientific notation:
$$ \text{significand} \times \text{base}^{\text{exponent}} $$

For example:
- `1.0e8` (Large) = `1.0000000 * 10^8`
- `1.0e-5` (Small) = `1.0000000 * 10^-5`

To add these two together, a CPU aligns the exponent of the smaller number to the larger number. If the difference between their exponents exceeds the number of digits/bits maintained in the significand (e.g., 24 bits for a standard python float or C `float`, 53 for a `double`), the smaller number becomes completely truncated during alignment.

This effect, known as catastrophic cancellation or round-off error, makes naive loops unpredictable when sequences contain values spanning vast orders of magnitude.

## 3. The Algorithm Logic

Kahan Summation tackles this by preserving a separate variable, usually denoted as `c` (compensation), that collects the small errors that are lost due to truncation. This effectively extends the precision of the accumulator implicitly without requiring larger scalar types.

### The Standard Approach
```python
total = 0.0
for val in values:
    total += val
```
*(Precision is lost permanently whenever `total + val` experiences truncation).*

### The Kahan Approach

Here is the exact algorithmic implementation:

```python
total = 0.0
compensation = 0.0

for val in values:
    # 1. Compensate the element we wish to add.
    y = val - compensation
    
    # 2. Add it to the total. 't' is the new total.
    # Note that low-order digits of 'y' may be lost here if 'total' is huge.
    t = total + y
    
    # 3. Recover the lost digits!
    # (t - total) recovers the high-order digits of 'y'
    # Subtracting 'y' recovers the *negative* of the lost low-order digits.
    compensation = (t - total) - y
    
    # 4. Set our running total to the new value.
    total = t
```

## 4. Step-By-Step Mathematical Explanation

Let's do a walkthrough of the exact steps during adding a very small sequence: `[10000.0, 3.14159]` in a severely restricted decimal float environment that can only hold 5 significant digits.

**Iteration 1: Add `10000.0`**
1. `val = 10000.0`
2. `y = 10000.0 - 0.0 = 10000.0`
3. `t = 0.0 + 10000.0 = 10000.0`
4. `compensation = (10000.0 - 0.0) - 10000.0 = 0.0`
5. `total = 10000.0`

**Iteration 2: Add `3.14159`**
1. `val = 3.14159`
2. `y = 3.14159 - 0.0 = 3.14159`
3. `t = 10000.0 + 3.14159 -> 10003.1` 
   - Wait: The max precision is 6 digits (`10003.1`), meaning `0.04159` was entirely dropped due to rounding error.
4. `compensation = (10003.1 - 10000.0) - 3.14159 = 3.1 - 3.14159 = -0.04159`
   - Wow! The compensation variable has accurately captured the exact digits that our standard summation dropped.
5. `total = 10003.1`

In the third iteration, when we add the next value, the `-0.04159` stored in `compensation` will be subtracted from `val`, meaning the lost piece will try to be re-added alongside the new number. Over time, those tiny accumulated fractions build up enough to flip the lowest-order bit of the main sum.

## 5. Potential Pitfalls: Optimization Flags
In modern compiler frameworks (such as GCC/Clang with `-Ofast`), vectorizations like the "Fast Math" optimization might detect that `compensation = (t - total) - y` mathematically simplifies to `0` using perfect infinite-precision real arithmetic. 

As a consequence, the compiler may optimize away the compensation variable completely, defeating the purpose of Kahan Summation and breaking the entire loop back down to naive evaluation.

Developers must use compiler pragmas, compiler-specific constructs (like strict IEEE 754 float guarantees), or careful memory volatility definitions to forbid simplifying this equation.

## 6. Neumaier's Variant (Improved Kahan-Babuška)
Kahan's algorithm assumes the running `total` is strictly larger (in magnitude) than the current `val` being added. While this is true when iteratively building a huge sum from small elements, in scenarios where a massive number `val` is added to a relatively small `total`, the high-order bits of *total* might be the ones lost, causing the error tracker `c` to miss information.

Neumaier introduced a check to swap the components being subtracted if the condition fails:
```python
def neumaier_sum(values):
    total = 0.0
    c = 0.0
    for val in values:
        t = total + val
        
        if abs(total) >= abs(val):
            # If total is larger, val's low-order bits are lost
            c += (total - t) + val
        else:
            # If val is larger, total's low-order bits are lost
            c += (val - t) + total
            
        total = t
    return total + c
```
By implementing this branch condition, Neumaier ensures worst-case round-off is protected regardless of order. This makes it an ideal generalized replacement when input variance is severe.
