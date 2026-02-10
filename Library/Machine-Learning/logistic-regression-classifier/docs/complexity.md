# Complexity Analysis: Logistic Regression

Logistic Regression is one of the most efficient classification algorithms, making it ideal for large-scale production systems. Understanding its computational complexity is crucial for system design decisions.

## 1. Time Complexity

### 1.1 Training Phase

The time complexity for training is:

$$O(n \times d \times i)$$

**Parameter Breakdown:**
- **$n$ (Number of Samples):** Total training examples
- **$d$ (Number of Features):** Dimensionality of each sample
- **$i$ (Number of Iterations):** Training epochs for gradient descent

### 1.2 Detailed Breakdown

**Per Iteration:**
1. **Forward Pass:** $O(n \times d)$
   - Matrix multiplication: $X \cdot w$ where $X$ is $(n \times d)$ and $w$ is $(d \times 1)$
   - Sigmoid application: $O(n)$

2. **Loss Calculation:** $O(n)$
   - Sum over all predictions and labels

3. **Gradient Computation:** $O(n \times d)$
   - Transpose multiplication: $X^T \cdot (y_{pred} - y)$

4. **Parameter Update:** $O(d)$
   - Update weights and bias

**Total per iteration:** $O(n \times d)$

**Total training:** $O(n \times d \times i)$

### 1.3 Prediction Phase

$$O(n \times d)$$

- Compute $z = Xw + b$: $O(n \times d)$
- Apply sigmoid: $O(n)$
- Threshold comparison: $O(n)$

**Single prediction:** $O(d)$ - extremely fast

---

## 2. Space Complexity

### 2.1 Model Parameters

$$O(d)$$

**Storage Requirements:**
- **Weights:** $d$ parameters (one per feature)
- **Bias:** 1 parameter
- **Total:** $d + 1 \approx O(d)$

### 2.2 Training Memory

$$O(n \times d)$$

**During Training:**
- **Input Data:** $n \times d$ matrix
- **Predictions:** $n$ values
- **Gradients:** $d$ values
- **Loss History:** $i$ values (optional tracking)

**Auxiliary Space:** $O(d)$ - Just for gradients and parameters

---

## 3. Real-World Performance Characteristics

### 3.1 Scalability Analysis

| Dataset Size | Features | Training Time (Approx) |
|--------------|----------|------------------------|
| 1,000 samples | 10 features | < 1 second |
| 10,000 samples | 50 features | 1-2 seconds |
| 100,000 samples | 100 features | 10-30 seconds |
| 1,000,000 samples | 1,000 features | 5-10 minutes |

*Assumes 1000 iterations, standard hardware*

### 3.2 Comparison with Other Algorithms

| Algorithm | Training Complexity | Prediction Complexity |
|-----------|--------------------|-----------------------|
| Logistic Regression | $O(n \times d \times i)$ | $O(d)$ |
| Decision Tree | $O(n \times d \times \log n)$ | $O(\log n)$ |
| Random Forest | $O(t \times n \times d \times \log n)$ | $O(t \times \log n)$ |
| SVM (Linear) | $O(n^2 \times d)$ to $O(n^3 \times d)$ | $O(s \times d)$ |
| Neural Network | $O(n \times d \times h \times l \times i)$ | $O(d \times h \times l)$ |

Where:
- $t$ = number of trees
- $s$ = number of support vectors
- $h$ = hidden units per layer
- $l$ = number of layers

**Key Insight:** Logistic Regression offers one of the best time-to-accuracy ratios for linearly separable data.

---

## 4. Optimization Techniques & Impact

### 4.1 Vectorization (NumPy)

Using NumPy's vectorized operations provides:
- **Speed Increase:** 10-100x faster than pure Python loops
- **Memory Efficiency:** Contiguous memory layout
- **Hardware Optimization:** SIMD instructions, cache efficiency

### 4.2 Stochastic Gradient Descent (SGD)

**Batch Gradient Descent:** $O(n \times d \times i)$ - Uses all data per iteration

**SGD Variant:** $O(b \times d \times i)$ where $b$ is batch size
- Faster convergence in practice
- Reduced memory footprint
- Better for streaming data

### 4.3 Early Stopping

- Monitor validation loss
- Stop when improvement < threshold
- Can reduce $i$ significantly (50-80% reduction common)

---

## 5. Convergence Analysis

### 5.1 Iteration Count

**Typical Convergence:** 100-1000 iterations
**Factors Affecting Convergence:**
- Learning rate $\alpha$
  - Too high: Oscillation or divergence
  - Too low: Slow convergence
- Feature scaling
  - Normalized features converge faster
- Data separability
  - Linearly separable: Fast convergence
  - Overlapping classes: Slower convergence

### 5.2 Learning Rate Impact

| Learning Rate | Iterations to Converge | Risk |
|---------------|------------------------|------|
| 0.001 | 5000+ | Too slow |
| 0.01 | 1000-2000 | Optimal |
| 0.1 | 500-1000 | May overshoot |
| 1.0 | Divergence | Too high |

---

## 6. Best Case vs Worst Case

### Best Case: $O(n \times d)$

**Scenario:**
- Perfectly linearly separable data
- Optimal learning rate
- Convergence in < 10 iterations
- Rare in practice

### Average Case: $O(n \times d \times i)$ where $i \approx 1000$

**Typical Production Scenario:**
- Moderately separable data
- Standard hyperparameters
- Convergence monitoring

### Worst Case: $O(n \times d \times i_{max})$

**Scenario:**
- Highly overlapping classes
- Poor feature scaling
- Suboptimal learning rate
- Requires full iteration limit

---

## 7. Memory Bottlenecks

### 7.1 Large Sample Size ($n >> d$)

**Challenge:** Loading all data in memory

**Solutions:**
- Mini-batch gradient descent
- Online learning (process one sample at a time)
- Data generators (load batches on-the-fly)

### 7.2 High Dimensionality ($d >> n$)

**Challenge:** More features than samples (risk of overfitting)

**Solutions:**
- Regularization (L1 for feature selection)
- Dimensionality reduction (PCA before training)
- Feature selection algorithms

---

## 8. Production Deployment Considerations

### 8.1 Training Phase

- **Batch Processing:** Train offline with full dataset
- **Incremental Learning:** Update weights with new data (warm start)
- **Distributed Training:** Parallelize across machines for massive datasets

### 8.2 Inference Phase

- **Latency:** $O(d)$ - typically < 1ms for $d < 1000$
- **Throughput:** Can process millions of predictions per second
- **Memory:** Tiny model size (KB to MB range)

### 8.3 Real-Time Systems

**Example: Ad Click Prediction**
- **Features:** 1000
- **Prediction Time:** 0.1ms
- **Throughput:** 10,000 requests/second on single core

**Example: Fraud Detection**
- **Features:** 50
- **Prediction Time:** 0.01ms
- **Throughput:** 100,000 transactions/second

---

## 9. Summary Table

| Metric | Complexity | Notes |
|--------|-----------|-------|
| **Training Time** | $O(n \times d \times i)$ | Linear in samples and features |
| **Single Prediction** | $O(d)$ | Constant w.r.t. training size |
| **Batch Prediction** | $O(n \times d)$ | Vectorized for efficiency |
| **Model Size** | $O(d)$ | Minimal storage footprint |
| **Memory (Training)** | $O(n \times d)$ | Dominated by data |
| **Convergence** | Typically 100-1000 iterations | Depends on data and learning rate |

---

## 10. When to Choose Logistic Regression

**Use When:**
- Need fast training and inference
- Interpretability is critical
- Data is approximately linearly separable
- Working with high-dimensional sparse data (text, genomics)
- Need probabilistic outputs
- Deploying to resource-constrained environments

**Avoid When:**
- Data has complex non-linear patterns
- Need to model feature interactions automatically
- Have very small datasets (prone to high variance)
