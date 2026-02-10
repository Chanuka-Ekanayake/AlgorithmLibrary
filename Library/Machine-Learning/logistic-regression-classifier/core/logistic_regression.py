import numpy as np
from typing import Optional

class LogisticRegression:
    """
    Logistic Regression implementation from scratch using NumPy.
    
    This algorithm is used for binary classification problems.
    It applies the sigmoid function to model the probability that a given input
    belongs to the positive class (label 1).
    """

    def __init__(self, learning_rate: float = 0.01, n_iterations: int = 1000, 
                 regularization: Optional[str] = None, lambda_param: float = 0.01):
        """
        Args:
            learning_rate: Step size for gradient descent.
            n_iterations: Maximum number of training iterations.
            regularization: Type of regularization ('l1', 'l2', or None).
            lambda_param: Regularization strength (λ).
        """
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.regularization = regularization
        self.lambda_param = lambda_param
        self.weights = None
        self.bias = None
        self.losses = []

    def _sigmoid(self, z: np.ndarray) -> np.ndarray:
        """
        The Sigmoid (Logistic) Function: σ(z) = 1 / (1 + e^(-z))
        Maps any real value to a probability between 0 and 1.
        """
        # Clip to prevent overflow in exp
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))

    def _compute_loss(self, y: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Binary Cross-Entropy Loss (Log Loss):
        L = -1/m * Σ [y*log(ŷ) + (1-y)*log(1-ŷ)]
        
        This measures how far our predictions are from the actual labels.
        """
        m = len(y)
        epsilon = 1e-15  # Prevent log(0)
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        
        loss = -np.mean(y * np.log(y_pred) + (1 - y) * np.log(1 - y_pred))
        
        # Add regularization term if specified
        if self.regularization == 'l2':
            loss += (self.lambda_param / (2 * m)) * np.sum(self.weights ** 2)
        elif self.regularization == 'l1':
            loss += (self.lambda_param / m) * np.sum(np.abs(self.weights))
            
        return loss

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'LogisticRegression':
        """
        Train the logistic regression model using Gradient Descent.
        
        LOGIC:
        1. Initialize weights and bias to zero.
        2. For each iteration:
           a. Compute predictions (forward pass).
           b. Calculate loss.
           c. Compute gradients (backward pass).
           d. Update weights and bias.
        3. Repeat until convergence or max iterations.
        """
        # --- 1. Initialization ---
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        # --- 2. Gradient Descent ---
        for i in range(self.n_iterations):
            # Forward Pass: Compute linear combination and apply sigmoid
            linear_model = np.dot(X, self.weights) + self.bias
            y_predicted = self._sigmoid(linear_model)
            
            # Compute loss for monitoring
            loss = self._compute_loss(y, y_predicted)
            self.losses.append(loss)
            
            # Backward Pass: Compute gradients
            dw = (1 / n_samples) * np.dot(X.T, (y_predicted - y))
            db = (1 / n_samples) * np.sum(y_predicted - y)
            
            # Add regularization to gradients
            if self.regularization == 'l2':
                dw += (self.lambda_param / n_samples) * self.weights
            elif self.regularization == 'l1':
                dw += (self.lambda_param / n_samples) * np.sign(self.weights)
            
            # Update parameters
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
            
            # Optional: Print progress every 100 iterations
            if (i + 1) % 100 == 0:
                print(f"Iteration {i + 1}/{self.n_iterations}, Loss: {loss:.4f}")
        
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Return the probability estimates for each sample.
        
        Returns:
            Array of probabilities for the positive class (1).
        """
        linear_model = np.dot(X, self.weights) + self.bias
        return self._sigmoid(linear_model)

    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        """
        Predict binary class labels.
        
        Args:
            X: Input features.
            threshold: Decision boundary (default 0.5).
            
        Returns:
            Array of binary predictions (0 or 1).
        """
        probabilities = self.predict_proba(X)
        return (probabilities >= threshold).astype(int)

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate the accuracy of the model.
        
        Returns:
            Accuracy as a percentage (0-100).
        """
        predictions = self.predict(X)
        accuracy = np.mean(predictions == y)
        return accuracy * 100
