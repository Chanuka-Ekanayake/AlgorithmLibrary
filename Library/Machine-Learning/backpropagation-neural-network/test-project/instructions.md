# User Guide: Neural Network Simulator (XOR Problem)

This project demonstrates the power of a **Multilayer Perceptron** trained via **Backpropagation** on the classic **XOR (Exclusive OR)** logic gate problem.

## What You'll See
1. **Initial State:** The network starts with random weights. It will wildly mispredict the XOR truth table.
2. **Training Phase:** The network performs 10,000 iterations (epochs) of forward passes, error calculations, and backpropagation weight updates. You will see the Mean Squared Error (MSE) steadily drop as the calculus gradients optimize the network.
3. **Final State:** The network will output predictions incredibly close to the true binary values (0 or 1), proving it has "learned" the pattern.

## Why the XOR Problem?
The XOR problem is famous in AI history. In the 1960s, researchers proved that a single-layer network (a Perceptron) is mathematically incapable of learning XOR because the points cannot be separated by a single straight line. 

This simulator demonstrates that by adding a **Hidden Layer** and a **Non-Linear Activation Function (Sigmoid)**, the network can warp its internal representation of the data and solve the problem perfectly.

## How to Test

1. **Navigate** to the `test-project` folder.
2. **Run** the simulator:
   ```bash
   python app.py
   ```
