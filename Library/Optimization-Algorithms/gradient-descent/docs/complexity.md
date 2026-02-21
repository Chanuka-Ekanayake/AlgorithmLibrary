# Complexity Analysis: Gradient Descent (Batch)

Gradient Descent does not have a "worst-case" time complexity in the traditional sense of sorting an array. Instead, its complexity is dictated by the hyperparameters set by the engineer (Epochs) and the sheer volume of the training data (Dataset Size).

## 1. Time Complexity

| Parameter                 | Impact                                                                                              | Complexity                                            |
| ------------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Dataset Size ()**       | The algorithm must compute the error for every single data point to calculate the average gradient. | per epoch                                             |
| **Epochs ()**             | The total number of iterations the algorithm takes to step down the error curve.                    | Multiplier                                            |
| **Total Time Complexity** | \*\*\*\*                                                                                            | Directly scales with data size and training duration. |

### The Computational Bottleneck

In **Batch Gradient Descent** (the version implemented here), the entire dataset of size is processed before a single weight update is made. If is 10,000,000 records, calculating one epoch takes significant time. This is why industrial applications often use **Stochastic Gradient Descent (SGD)** or **Mini-Batch Gradient Descent**, which update the weights after looking at only 1 (or a small batch) of data points, drastically speeding up the convergence rate at the cost of some stability.

---

## 2. Space Complexity

| Component                  | Complexity           | Description                                                                                               |
| -------------------------- | -------------------- | --------------------------------------------------------------------------------------------------------- |
| **Model Parameters**       |                      | Regardless of dataset size, a linear regression model only stores a `weight` and a `bias`.                |
| **Gradients**              |                      | Temporary variables (`weight_gradient`, `bias_gradient`) are reused every epoch.                          |
| **Cost History**           |                      | An array storing the cost at each epoch to monitor convergence.                                           |
| **Total Space Complexity** | \*\*\*\* (Auxiliary) | The optimization engine itself requires almost no memory, making it highly efficient once data is loaded. |

---

## 3. The "Goldilocks" Hyperparameter: Learning Rate ()

The time complexity assumes the algorithm actually reaches the bottom of the error curve (convergence). Whether it succeeds or fails entirely depends on the **Learning Rate** ().

The update rule mathematically scales the gradient by :

- ** is Too Small (e.g., 0.00001):** The algorithm takes microscopic steps. It will eventually find the minimum, but it might take 100,000 epochs to get there, wasting massive amounts of server compute time.
- ** is Optimal (e.g., 0.01):** The algorithm takes large steps initially when the slope is steep, and naturally takes smaller steps as the slope levels out near the minimum, converging quickly and safely.
- ** is Too Large (e.g., 1.5):** The step size overshoots the minimum entirely. It bounces to the other side of the error curve, higher than where it started. The error explodes to infinity (Divergence), and the model collapses.

---

## 4. Engineering Constraints

- **Feature Scaling:** If one feature in the dataset is measured in millions (e.g., house price) and another in single digits (e.g., number of bedrooms), the error surface becomes a stretched, narrow valley. Gradient Descent will oscillate wildly and struggle to converge unless the input data is mathematically normalized (scaled between 0 and 1) before training begins.
- **Local Minima:** For linear regression, the cost function is a perfect bowl (convex), meaning there is only one global minimum. However, in deep neural networks, the cost surface has thousands of "local minima." Standard gradient descent can get trapped in these shallow valleys, which is why advanced optimizers (like Adam or RMSprop) are built on top of this foundational logic.
