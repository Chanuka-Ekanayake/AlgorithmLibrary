# Algorithm Logic: Logistic Regression

## 1. The Core Concept

**Logistic Regression** is a supervised learning algorithm used for **binary classification**. Despite its name containing "regression," it predicts discrete class labels (0 or 1) rather than continuous values.

The key innovation is the **Sigmoid Function**, which transforms any real-valued number into a probability between 0 and 1. This probability represents the likelihood that a given input belongs to the positive class.

---

## 2. The Mathematical Foundation

### 2.1 The Sigmoid (Logistic) Function

The sigmoid function is defined as:

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

Where:
- $z = w_1x_1 + w_2x_2 + ... + w_dx_d + b$ (the linear combination)
- $w$ = weights (feature coefficients)
- $b$ = bias (intercept term)
- $x$ = input features

**Properties:**
- Output range: (0, 1)
- S-shaped curve
- $\sigma(0) = 0.5$ (decision boundary)
- As $z \to \infty$, $\sigma(z) \to 1$
- As $z \to -\infty$, $\sigma(z) \to 0$

### 2.2 The Hypothesis Function

For logistic regression, our prediction is:

$$h_\theta(x) = \sigma(w^Tx + b)$$

This gives us the probability that $y = 1$ given input $x$:

$$P(y=1|x) = h_\theta(x)$$
$$P(y=0|x) = 1 - h_\theta(x)$$

---

## 3. The Cost Function (Binary Cross-Entropy Loss)

We can't use Mean Squared Error (MSE) for classification because the sigmoid function would create a non-convex optimization surface with many local minima.

Instead, we use **Binary Cross-Entropy Loss** (Log Loss):

$$J(\theta) = -\frac{1}{m}\sum_{i=1}^{m}[y^{(i)}\log(h_\theta(x^{(i)})) + (1-y^{(i)})\log(1-h_\theta(x^{(i)}))]$$

Where:
- $m$ = number of training examples
- $y^{(i)}$ = actual label (0 or 1)
- $h_\theta(x^{(i)})$ = predicted probability

**Intuition:**
- When $y = 1$: Loss = $-\log(h_\theta(x))$ (penalizes low probabilities)
- When $y = 0$: Loss = $-\log(1-h_\theta(x))$ (penalizes high probabilities)

---

## 4. Gradient Descent Optimization

To minimize the cost function, we use **Gradient Descent**. We compute the gradients (derivatives) of the cost function with respect to each parameter and update them iteratively.

### 4.1 Gradient Computation

$$\frac{\partial J}{\partial w_j} = \frac{1}{m}\sum_{i=1}^{m}(h_\theta(x^{(i)}) - y^{(i)})x_j^{(i)}$$

$$\frac{\partial J}{\partial b} = \frac{1}{m}\sum_{i=1}^{m}(h_\theta(x^{(i)}) - y^{(i)})$$

### 4.2 Parameter Update Rule

$$w_j := w_j - \alpha \frac{\partial J}{\partial w_j}$$

$$b := b - \alpha \frac{\partial J}{\partial b}$$

Where $\alpha$ is the learning rate (step size).

---

## 5. Step-by-Step Algorithm Walkthrough

### Step 1: Initialization
- Set all weights $w$ to zeros (or small random values)
- Set bias $b$ to zero
- Choose learning rate $\alpha$ and number of iterations

### Step 2: Forward Pass
For each training example:
1. Compute linear combination: $z = w^Tx + b$
2. Apply sigmoid: $\hat{y} = \sigma(z)$
3. Calculate loss: $J(\theta)$

### Step 3: Backward Pass
1. Compute gradients: $\frac{\partial J}{\partial w}$ and $\frac{\partial J}{\partial b}$
2. Update parameters using gradient descent

### Step 4: Iteration
Repeat steps 2-3 until:
- Loss converges (changes become negligible)
- Maximum iterations reached

### Step 5: Prediction
For new data point $x$:
1. Compute $z = w^Tx + b$
2. Apply sigmoid: $p = \sigma(z)$
3. Classify: $\hat{y} = 1$ if $p \geq 0.5$, else $\hat{y} = 0$

---

## 6. Regularization Techniques

To prevent overfitting, we add a penalty term to the cost function.

### 6.1 L2 Regularization (Ridge)

$$J(\theta) = -\frac{1}{m}\sum_{i=1}^{m}[...] + \frac{\lambda}{2m}\sum_{j=1}^{d}w_j^2$$

- Penalizes large weights
- Keeps all features but shrinks coefficients

### 6.2 L1 Regularization (Lasso)

$$J(\theta) = -\frac{1}{m}\sum_{i=1}^{m}[...] + \frac{\lambda}{m}\sum_{j=1}^{d}|w_j|$$

- Can force some weights to exactly zero
- Performs feature selection

---

## 7. Decision Boundary

The decision boundary is where $P(y=1|x) = 0.5$, which occurs when:

$$w^Tx + b = 0$$

This creates a **linear** separation in feature space.

- **Linearly Separable Data:** Perfect classification possible
- **Non-linearly Separable Data:** Need feature engineering or non-linear models

---

## 8. Real-World Engineering Application

### Example: Email Spam Detection

**Features:**
- $x_1$: Number of exclamation marks
- $x_2$: Presence of word "free"
- $x_3$: Number of links

**Process:**
1. Train on labeled emails (spam/not spam)
2. Learn weights: $w_1=0.8$, $w_2=1.2$, $w_3=0.5$, $b=-0.3$
3. New email arrives: [2, 1, 3]
4. Compute: $z = 0.8(2) + 1.2(1) + 0.5(3) - 0.3 = 3.9$
5. Probability: $\sigma(3.9) = 0.98$
6. Classify as SPAM (threshold = 0.5)

---

## 9. Advantages and Limitations

### Advantages
- **Interpretable:** Weights show feature importance
- **Probabilistic:** Provides confidence scores
- **Efficient:** Fast training and prediction
- **No hyperparameters:** (except learning rate and iterations)

### Limitations
- **Linear Decision Boundary:** Can't model complex patterns
- **Assumes Independence:** Features should be relatively independent
- **Sensitive to Outliers:** Extreme values can skew the model
- **Requires Feature Scaling:** Different scales can slow convergence

---

## 10. Extensions

- **Multi-class Classification:** One-vs-Rest or Softmax Regression
- **Polynomial Features:** Create non-linear decision boundaries
- **Neural Networks:** Stack multiple logistic units for deep learning
