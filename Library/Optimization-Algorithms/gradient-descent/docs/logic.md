# Algorithm Logic: Gradient Descent

In Machine Learning, building a predictive model (like Linear Regression) means finding a line that perfectly captures the trend of your data. The equation for a line is , where is the weight (slope) and is the bias (y-intercept).

Gradient Descent is the algorithm that determines the absolute best values for and .

## 1. The Objective: The Cost Function

Before a model can improve, it needs to know how wrong it currently is. We measure this using a **Cost Function**, specifically the **Mean Squared Error (MSE)**.

MSE calculates the difference between what the model predicted () and the actual target value (), squares that difference to eliminate negative numbers, and averages it across all data points.

If you plot every possible value of and against the resulting Cost , it forms a 3D convex bowl. The goal of Gradient Descent is to find the exact coordinates at the absolute bottom of that bowl.

---

## 2. The Compass: Partial Derivatives

If you drop a ball on the side of a bowl, gravity pulls it downward based on the slope of the surface. In our code, **Calculus** acts as gravity.

We calculate the partial derivative of the Cost Function with respect to both our weight () and our bias (). The derivative gives us the exact slope of the curve at our current position.

- **Derivative with respect to :**

  \[
  \frac{\partial J}{\partial w}
  = \frac{2}{N} \sum_{i=1}^{N} (\hat{y}_i - y_i) x_i
  = \frac{2}{N} \sum_{i=1}^{N} ((w x_i + b) - y_i) x_i
  \]

- **Derivative with respect to :**

  \[
  \frac{\partial J}{\partial b}
  = \frac{2}{N} \sum_{i=1}^{N} (\hat{y}_i - y_i)
  = \frac{2}{N} \sum_{i=1}^{N} ((w x_i + b) - y_i)
  \]
### How the Slope Guides Us

- If the slope is **positive**, it means we are on the right side of the bowl heading upward. We need to decrease our weight to move left toward the minimum.
- If the slope is **negative**, it means we are on the left side of the bowl heading downward. We need to increase our weight to move right toward the minimum.

---

## 3. The Descent: The Update Rule

Once we know the slope, we update our parameters by taking a step in the _opposite_ direction of the gradient.

This is where the **Learning Rate** () comes in. It determines the size of the step we take.

Notice the subtraction sign.

- If the derivative is positive, we subtract a positive number, making smaller (moving left).
- If the derivative is negative, we subtract a negative number, effectively adding to , making it larger (moving right).

---

## 4. The Loop: Epochs

This process of calculating the error, finding the gradients, and updating the weights is repeated over and over. Each full pass through the dataset is called an **Epoch**.

With each epoch, the model steps closer to the bottom of the bowl. Because the curve flattens out at the bottom, the derivative approaches zero. As the derivative shrinks, the updates to and naturally become smaller and smaller, allowing the algorithm to smoothly settle precisely on the optimal values without overshooting.
