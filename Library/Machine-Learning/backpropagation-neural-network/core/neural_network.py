"""
Neural Network (Backpropagation) Core Module

A pure Python implementation of a Multilayer Perceptron (MLP) with one hidden layer.
This module demonstrates the raw mathematics of feedforward neural networks and 
the backpropagation algorithm without relying on external tensor libraries like NumPy.

Author: Algorithm Library
"""

import math
import random
from typing import List


class NeuralNetwork:
    """
    A simple Feedforward Neural Network trained via Backpropagation.
    Architecture: Input Layer -> Hidden Layer -> Output Layer
    Activation: Sigmoid
    Loss: Mean Squared Error (MSE)
    """

    def __init__(self, input_nodes: int, hidden_nodes: int, output_nodes: int, learning_rate: float = 0.1):
        """
        Initializes the network with random weights and zero biases.
        
        Args:
            input_nodes: Number of features in the input vector.
            hidden_nodes: Number of neurons in the hidden layer.
            output_nodes: Number of neurons in the output layer.
            learning_rate: Step size for gradient descent weight updates.
        """
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        self.learning_rate = learning_rate

        # Initialize Weights (Random values between -1 and 1)
        # weights_ih: Weights from Input to Hidden layer
        self.weights_ih = [[random.uniform(-1, 1) for _ in range(input_nodes)] for _ in range(hidden_nodes)]
        
        # weights_ho: Weights from Hidden to Output layer
        self.weights_ho = [[random.uniform(-1, 1) for _ in range(hidden_nodes)] for _ in range(output_nodes)]

        # Initialize Biases (Start at 0)
        self.bias_h = [0.0 for _ in range(hidden_nodes)]
        self.bias_o = [0.0 for _ in range(output_nodes)]

    @staticmethod
    def _sigmoid(x: float) -> float:
        """Sigmoid activation function."""
        # Clip x to prevent overflow in math.exp
        x = max(-700.0, min(700.0, x))
        return 1.0 / (1.0 + math.exp(-x))

    @staticmethod
    def _dsigmoid(y: float) -> float:
        """
        Derivative of the sigmoid function.
        Note: This expects the ALREADY computed sigmoid output (y = sigmoid(x))
        """
        return y * (1.0 - y)

    def predict(self, input_array: List[float]) -> List[float]:
        """
        Performs a forward pass through the network to generate a prediction.
        
        Args:
            input_array: List of input features.
            
        Returns:
            List of output activations.
        """
        if len(input_array) != self.input_nodes:
            raise ValueError(f"Expected {self.input_nodes} inputs, got {len(input_array)}")

        # 1. Input -> Hidden
        hidden_outputs = []
        for i in range(self.hidden_nodes):
            # Dot product of inputs and weights for this hidden neuron
            weighted_sum = self.bias_h[i]
            for j in range(self.input_nodes):
                weighted_sum += input_array[j] * self.weights_ih[i][j]
            # Apply activation
            hidden_outputs.append(self._sigmoid(weighted_sum))

        # 2. Hidden -> Output
        final_outputs = []
        for i in range(self.output_nodes):
            # Dot product of hidden outputs and weights for this output neuron
            weighted_sum = self.bias_o[i]
            for j in range(self.hidden_nodes):
                weighted_sum += hidden_outputs[j] * self.weights_ho[i][j]
            # Apply activation
            final_outputs.append(self._sigmoid(weighted_sum))

        return final_outputs

    def train_step(self, input_array: List[float], target_array: List[float]):
        """
        Performs one forward pass followed by one backward pass (backpropagation)
        to update the weights for a single training example.
        
        Args:
            input_array: List of input features.
            target_array: List of expected output values.
        """
        # ==========================================
        # FORWARD PASS (Compute activations)
        # ==========================================
        
        # 1. Input -> Hidden
        hidden_outputs = []
        for i in range(self.hidden_nodes):
            weighted_sum = self.bias_h[i]
            for j in range(self.input_nodes):
                weighted_sum += input_array[j] * self.weights_ih[i][j]
            hidden_outputs.append(self._sigmoid(weighted_sum))

        # 2. Hidden -> Output
        final_outputs = []
        for i in range(self.output_nodes):
            weighted_sum = self.bias_o[i]
            for j in range(self.hidden_nodes):
                weighted_sum += hidden_outputs[j] * self.weights_ho[i][j]
            final_outputs.append(self._sigmoid(weighted_sum))

        # ==========================================
        # BACKWARD PASS (Compute gradients and update)
        # ==========================================
        
        # 1. Output Layer Error
        output_errors = []
        for i in range(self.output_nodes):
            # Error = Target - Output
            output_errors.append(target_array[i] - final_outputs[i])

        # 2. Gradients for Output Layer
        # Gradient = Error * dsigmoid(Output) * LearningRate
        for i in range(self.output_nodes):
            gradient = output_errors[i] * self._dsigmoid(final_outputs[i]) * self.learning_rate
            
            # Update Bias
            self.bias_o[i] += gradient
            
            # Update Weights (Hidden -> Output)
            # Delta Weight = Gradient * Hidden_Output
            for j in range(self.hidden_nodes):
                self.weights_ho[i][j] += gradient * hidden_outputs[j]

        # 3. Hidden Layer Error (Backpropagate the error)
        hidden_errors = []
        for i in range(self.hidden_nodes):
            error = 0.0
            for j in range(self.output_nodes):
                # The error is proportional to the weight connecting them
                error += output_errors[j] * self.weights_ho[j][i]
            hidden_errors.append(error)

        # 4. Gradients for Hidden Layer
        # Gradient = Error * dsigmoid(Hidden_Output) * LearningRate
        for i in range(self.hidden_nodes):
            gradient = hidden_errors[i] * self._dsigmoid(hidden_outputs[i]) * self.learning_rate
            
            # Update Bias
            self.bias_h[i] += gradient
            
            # Update Weights (Input -> Hidden)
            # Delta Weight = Gradient * Input
            for j in range(self.input_nodes):
                self.weights_ih[i][j] += gradient * input_array[j]

    def train(self, X: List[List[float]], y: List[List[float]], epochs: int, verbose: bool = False):
        """
        Trains the neural network over a dataset for a given number of epochs.
        Uses Stochastic Gradient Descent (SGD) by updating weights per sample.
        
        Args:
            X: List of input vectors.
            y: List of target output vectors.
            epochs: Number of times to iterate over the entire dataset.
            verbose: If True, prints the Mean Squared Error (MSE) periodically.
        """
        for epoch in range(1, epochs + 1):
            
            # Shuffle data for SGD
            dataset = list(zip(X, y))
            random.shuffle(dataset)
            
            for input_array, target_array in dataset:
                self.train_step(input_array, target_array)
                
            if verbose and (epoch % (epochs // 10) == 0 or epoch == 1):
                mse = self.calculate_mse(X, y)
                print(f"Epoch {epoch:5d}/{epochs} | MSE: {mse:.6f}")

    def calculate_mse(self, X: List[List[float]], y: List[List[float]]) -> float:
        """Calculates the Mean Squared Error over a dataset."""
        total_error = 0.0
        for input_array, target_array in zip(X, y):
            prediction = self.predict(input_array)
            for p, t in zip(prediction, target_array):
                total_error += (t - p) ** 2
        return total_error / len(X)
