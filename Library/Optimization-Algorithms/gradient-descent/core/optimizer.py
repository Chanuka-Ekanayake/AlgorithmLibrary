"""
Gradient Descent Optimizer
Implements Batch Gradient Descent to find the optimal weights and bias 
for a linear regression model by minimizing the Mean Squared Error (MSE).
"""

from typing import List, Tuple

class GradientDescentOptimizer:
    """
    Mathematical optimization engine for training machine learning models.
    """

    @staticmethod
    def compute_cost(X: List[float], y: List[float], weight: float, bias: float) -> float:
        """
        Calculates the Mean Squared Error (MSE) Cost Function: J(w,b).
        This measures how far off the current model's predictions are from the actual data.
        
        Args:
            X: List of input features.
            y: List of actual target values.
            weight: Current model weight (slope).
            bias: Current model bias (y-intercept).
            
        Returns:
            The computed total error as a float.
        """
        m = len(X)
        if m == 0:
            return 0.0

        total_error = 0.0
        for i in range(m):
            # f_wb(x) = w * x + b
            prediction = (weight * X[i]) + bias
            
            # Squared error for the current data point
            total_error += (prediction - y[i]) ** 2
            
        # Divide by 2m to mathematically simplify the derivative later
        return total_error / (2 * m)

    @staticmethod
    def optimize(
        X: List[float], 
        y: List[float], 
        learning_rate: float = 0.01, 
        epochs: int = 1000
    ) -> Tuple[float, float, List[float]]:
        """
        Executes the gradient descent loop to find the optimal parameters.
        
        Args:
            X: List of input features (training data).
            y: List of target values (labels).
            learning_rate: The step size (alpha) taken towards the minimum.
            epochs: The number of iterations to run the optimization.
            
        Returns:
            A tuple containing (final_weight, final_bias, cost_history_array).
        """
        m = len(X)
        
        # Initialize model parameters at zero
        weight = 0.0
        bias = 0.0
        
        # Track the error over time to verify convergence
        cost_history = []

        for epoch in range(epochs):
            weight_gradient = 0.0
            bias_gradient = 0.0

            # 1. Calculate the partial derivatives (gradients) for the entire dataset
            for i in range(m):
                prediction = (weight * X[i]) + bias
                error = prediction - y[i]
                
                # Derivative of MSE with respect to weight (w)
                weight_gradient += error * X[i]
                
                # Derivative of MSE with respect to bias (b)
                bias_gradient += error

            # Average the gradients across all training examples
            weight_gradient /= m
            bias_gradient /= m

            # 2. Update parameters by taking a step in the *opposite* direction of the slope
            weight -= learning_rate * weight_gradient
            bias -= learning_rate * bias_gradient

            # 3. Track the cost to ensure the model is actually learning
            current_cost = GradientDescentOptimizer.compute_cost(X, y, weight, bias)
            cost_history.append(current_cost)

        return weight, bias, cost_history