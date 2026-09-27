# Backpropagation (Neural Network)

## 1. Overview

**Backpropagation** is the foundational algorithm behind the deep learning revolution. It is a method for calculating the gradient of the loss function with respect to the weights of a neural network. This gradient is then used by optimization algorithms (like Gradient Descent) to update the weights, allowing the network to "learn" from data.

This package contains a pure Python implementation of a **Multilayer Perceptron (MLP)** — a feedforward artificial neural network. It features an input layer, a hidden layer, and an output layer, demonstrating how non-linear problems can be solved using the chain rule of calculus.

---

## 2. Technical Features

- **Pure Python, Zero Dependencies:** Built without NumPy or PyTorch to expose the raw mathematical mechanics of forward passes and backpropagation.
- **Non-Linearity:** Implements the Sigmoid activation function and its derivative to capture non-linear relationships.
- **XOR Capable:** Unlike Logistic Regression, this network uses its hidden layer to easily solve non-linearly separable problems like XOR.
- **Pedagogical Matrix Math:** Uses basic nested loops and lists to demonstrate exactly how weights and biases interact with layer activations.

---

## 3. Architecture

```text
.
├── core/                  # Neural Network Engine
│   ├── __init__.py        # Package initialization
│   └── neural_network.py  # Feedforward logic, Backpropagation, and weight updates
├── docs/                  # Technical Documentation
│   ├── logic.md           # The Chain Rule, activation functions, and gradient descent
│   └── complexity.md      # Analysis of time/space scaling per epoch
├── test-project/          # Neural Network Simulator
│   ├── app.py             # Trains the network to solve the classic XOR problem
│   └── instructions.md    # Guide for running the training visualization
└── README.md              # Documentation Entry Point
```

---

## 4. Performance Specifications

| Metric                  | Specification                                     |
| ----------------------- | ------------------------------------------------- |
| **Training Time**       | O(E × N × W) (Epochs × Samples × Weights)         |
| **Prediction Time**     | O(W) (Number of connections/weights)              |
| **Space Complexity**    | O(W) (Memory scales with network size)            |
| **Activation**          | Sigmoid function, $f(x) = 1 / (1 + e^{-x})$       |
| **Loss Function**       | Mean Squared Error (MSE)                          |

---

## 5. Deployment & Usage

### Integration

The `NeuralNetwork` class supports configurable input, hidden, and output sizes:

```python
from core.neural_network import NeuralNetwork

# 1. Create a network (e.g., 2 inputs, 4 hidden nodes, 1 output)
nn = NeuralNetwork(input_nodes=2, hidden_nodes=4, output_nodes=1, learning_rate=0.5)

# 2. Define training data (XOR problem)
X_train = [[0, 0], [0, 1], [1, 0], [1, 1]]
y_train = [[0], [1], [1], [0]]

# 3. Train the network
nn.train(X_train, y_train, epochs=10000)

# 4. Predict
for x in X_train:
    prediction = nn.predict(x)
    print(f"Input: {x} -> Output: {prediction[0]:.4f}")
```

### Running the Simulator

To watch the neural network learn a non-linear problem from scratch:

1. Navigate to the `test-project` directory:
   ```bash
   cd test-project
   ```
2. Run the simulation:
   ```bash
   python app.py
   ```

---

## 6. Industrial Applications

Backpropagation and Neural Networks form the basis of modern AI:

- **Computer Vision:** Convolutional Neural Networks (CNNs) for image recognition, facial detection, and medical imaging.
- **Natural Language Processing (NLP):** Transformers and Recurrent Neural Networks (RNNs) for translation, summarization, and LLMs (like GPT).
- **Control Systems:** Deep Reinforcement Learning for autonomous driving, robotics, and game-playing AI (e.g., AlphaGo).
- **Predictive Analytics:** Forecasting stock markets, weather, and consumer behavior using deep multilayer perceptrons.
