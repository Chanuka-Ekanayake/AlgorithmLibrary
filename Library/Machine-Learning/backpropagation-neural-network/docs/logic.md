# Algorithm Logic: Neural Network & Backpropagation

## 1. The Multi-Layer Perceptron (MLP)

A neural network is a mathematical function that maps inputs to outputs. It does this by passing the inputs through interconnected layers of "neurons".

### 1.1 The Neuron (Perceptron)
A single neuron does two things:
1. Calculates a **weighted sum** of its inputs plus a bias:  
   $Z = (w_1 \cdot x_1) + (w_2 \cdot x_2) + \dots + b$
2. Passes that sum through an **Activation Function** (like Sigmoid) to introduce non-linearity:  
   $A = \sigma(Z) = \frac{1}{1 + e^{-Z}}$

### 1.2 Feedforward Pass
In a 3-layer network (Input $\rightarrow$ Hidden $\rightarrow$ Output), the data flows forward:
1. The Inputs are multiplied by the Input-to-Hidden weights.
2. The Hidden neurons sum these up, add their bias, and apply Sigmoid.
3. The Hidden outputs are multiplied by the Hidden-to-Output weights.
4. The Output neurons sum these up, add their bias, and apply Sigmoid to produce the final prediction.

---

## 2. The Learning Problem

If the network predicts $0.8$, but the correct answer (target) is $0.0$, the network has made an error. We calculate the **Loss** (e.g., Mean Squared Error).

The goal of learning is to adjust the weights and biases to make the Loss as small as possible. But how do we know which weights to increase, and which to decrease? 

Enter **Backpropagation**.

---

## 3. Backpropagation (The Backward Pass)

Backpropagation is simply the application of the **Chain Rule of Calculus** to calculate the gradient (slope) of the Loss with respect to every single weight in the network.

### Step 1: The Output Layer Error
First, we calculate how wrong the output layer is:
$$E_{output} = \text{Target} - \text{Output}$$

### Step 2: Gradients for Output Weights
We want to know how much a specific weight $w_{ho}$ connecting a hidden neuron to an output neuron contributed to the error. 
Using the derivative of the Sigmoid function ($\sigma'(x) = \sigma(x) \cdot (1 - \sigma(x))$), the gradient is:
$$\text{Gradient}_{o} = E_{output} \times \text{Output} \times (1 - \text{Output}) \times \text{LearningRate}$$

We update the weight:
$$w_{ho} \leftarrow w_{ho} + (\text{Gradient}_{o} \times \text{Hidden\_Output})$$
We update the bias:
$$b_{o} \leftarrow b_{o} + \text{Gradient}_{o}$$

### Step 3: Backpropagating Error to the Hidden Layer
Here is the genius of the algorithm: we don't have explicit "targets" for the hidden layer. How do we know if a hidden neuron was wrong?
We calculate the hidden neuron's error by **summing the errors of the output neurons it connects to, weighted by the strength of the connection**:
$$E_{hidden} = \sum (E_{output} \times w_{ho})$$

### Step 4: Gradients for Hidden Weights
Now that we have the error for the hidden neurons, we apply the exact same calculus to update the Input-to-Hidden weights $w_{ih}$:
$$\text{Gradient}_{h} = E_{hidden} \times \text{Hidden\_Output} \times (1 - \text{Hidden\_Output}) \times \text{LearningRate}$$

Update the weight:
$$w_{ih} \leftarrow w_{ih} + (\text{Gradient}_{h} \times \text{Input})$$
Update the bias:
$$b_{h} \leftarrow b_{h} + \text{Gradient}_{h}$$

---

## 4. Why Non-Linearity Matters (The XOR Problem)

If you build a neural network with no activation function (a linear network), it doesn't matter if you have 100 hidden layers — the entire network mathematically collapses into a single linear equation ($y = mx + b$).

Linear equations can only draw straight lines. They cannot solve problems like **XOR (Exclusive OR)**:
- $(0,0) \rightarrow 0$
- $(0,1) \rightarrow 1$
- $(1,0) \rightarrow 1$
- $(1,1) \rightarrow 0$

Try drawing a single straight line on a graph that separates the $1$s from the $0$s. It is impossible.

By applying the non-linear **Sigmoid** function in the hidden layer, the neural network warps the geometry of the space, transforming the XOR problem into a space where a straight line *can* separate the classes in the output layer.
