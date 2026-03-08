# Running the Kahan Summation Benchmark Suite

## Overview

Welcome to the Kahan Summation test application platform! This sub-module provides a robust, interactive Command Line Interface (CLI) application (`app.py`) designed to empirically prove the phenomenon of precision loss in computers. More importantly, it demonstrates how utilizing our Core Kahan Accumulator completely mitigates this mathematical drift.

If you have ever been curious about floating-point errors, this sandbox is the perfect place to safely explore catastrophic cancellations at scale.

## 1. System Requirements

Before running the evaluation, please ensure your host system adheres to the following prerequisites:
- **Operating System:** Any OS capable of interpreting Python (Linux, macOS, Windows).
- **Python Version:** Core Python 3.7+ is enforced. This ensures the `decimal` and `typing` libraries function correctly without breaking backward compatibility constraints.
- **Hardware Profile:** Highly recommended to run on CPUs that adhere strictly to IEEE 754 Floating-Point architecture standards (typically standard on all x86_64, ARM processors).

*Note: No external libraries (like NumPy or Pandas) are required! The test suite relies exclusively on the Python standard library for maximum portability and standalone isolation.*

## 2. Installation and Verification

The test project requires zero external package dependency installations (`pip install`). However, you must invoke the script properly to ensure the `core/accumulator.py` relative imports successfully bind to the environment block.

1. Open your terminal application.
2. Navigate directly into the module folder directory:
   ```bash
   cd "Library/Numerical & Miscellaneous/kahan-summation"
   ```
3. Ensure the project structure is intact by listing files:
   ```bash
   ls -la test-project/app.py
   ```

## 3. Executing the Application

### Basic Standard Run
To run the benchmark suite against a standard dataset footprint (1,000,000 algorithmic floats):
```bash
python3 test-project/app.py
```

### Advanced Algorithmic Overrides
If you wish to configure the variance distributions or the exact array size $N$ bounds, the script provides CLI argument overrides mapping:

- `--size [INTEGER]`: Determines the exact number of array variables generated for the mathematical summation. Larger sequences mathematically guarantee higher degrees of accumulated small-fraction errors.
- `--variance [INTEGER]`: Determines the exponent variability bounds $10^{-v}$ to $10^{v/2}$. Expanding this spreads values further across the scientific number plane, forcing truncation events on virtually every addition cycle inside naive summation execution loops.

**Example: A Heavy Stress Test**
```bash
python3 test-project/app.py --size 5000000 --variance 25
```

## 4. Interpreting Results

The console application will yield a block of diagnostics. Here is exactly what those diagnostics summarize:

- **Perfect Mathematical Sum**: Uses Python's infinite-precision `decimal.Decimal` library. This is the grounded absolute truth mathematically guaranteed to be accurate.
- **Naive Standard Sum**: Uses standard CPU `float` registers. Notice how widely it diverges from the absolute truth due to constant lower-bound bit shedding.
- **Kahan Compensated Sum**: Uses our custom `core.accumulator` logic. Notice this is almost universally identical down to the lowest sub-decimal plane to the perfect iteration.
- **Ratio / Speed Metrics**: Due to executing four distinct hardware math instructions (`sub, add, sub, sub`) versus purely one instruction per iteration block, the Kahan implementation runs generally 3x to 5x slower depending precisely on how local memory is fetched.

## 5. Troubleshooting (Compiler Fast-Math)

If your environment utilizes compilers like PyPy or Numba JIT, you may witness the Kahan float error mirroring the Naive float exactly! If this happens, your compiler's optimizer block has executed a "Fast Math" vector transformation and fundamentally deleted our compensation algebraic equation!

Always run Kahan algorithms strictly on unoptimized mathematical IEEE paths or apply hard boundary pragmas limiting compilation overrides limits. Without standard IEEE guarantees, compensated algorithm operations inevitably simplify dynamically back down to zero boundaries mathematically during optimization compilation.

## 6. Extending the Benchmarks

If you identify novel edge cases, we highly encourage adding them to the benchmark suite pipeline.
Some excellent additions would be:
- Integration testing utilizing NumPy `float32` arrays instead of python standard 64-bit floats, which drops precision significantly faster.
- Modifying the `generate_test_data` configuration blocks to emit purely monotonic increasing sequences, testing `total` explosion characteristics against fixed error tracking configurations.
- Interleaving high scale variance jumps sequentially instead of purely locally randomized buffers maps.

## 7. Mathematical Extensions
Consider implementing the `Babuška-Neumaier` logic branch directly into the `app.py` benchmark loop to evaluate Branch Prediction pipelining costs across massive standard standard deviations arrays experimentally. Utilizing deterministic time matrices could validate conditional logic scaling accurately.
