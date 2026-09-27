# Complexity Analysis: Neural Network (Backpropagation)

## 1. Time Complexity

### 1.1 Forward Pass (Prediction)
To make a single prediction, the network computes the dot product of inputs and weights for every node in every layer.

For a network with $I$ inputs, $H$ hidden nodes, and $O$ outputs:
- Input to Hidden: $I \times H$ multiplications
- Hidden to Output: $H \times O$ multiplications

**Time Complexity:** $\mathcal{O}(I \cdot H + H \cdot O)$  
More simply, $\mathcal{O}(W)$ where $W$ is the total number of weights (connections) in the network.

### 1.2 Backward Pass (Training)
Training is vastly more expensive than prediction because it requires multiple passes over the entire dataset.

For a single training example (Stochastic Gradient Descent):
1. **Forward Pass:** $\mathcal{O}(W)$
2. **Error Calculation & Backpropagation:** $\mathcal{O}(W)$
3. **Weight Updating:** $\mathcal{O}(W)$

Therefore, one complete training step for one sample is $\mathcal{O}(W)$.

For a dataset of size $N$, running for $E$ Epochs:

**Total Training Time:** $\mathcal{O}(E \times N \times W)$

#### The Scaling Bottleneck
If you have a 1,000-pixel image ($I=1000$), a hidden layer of 500 neurons ($H=500$), and 10 output classes ($O=10$):
- $W = (1000 \times 500) + (500 \times 10) = 505,000$ weights.
- Training on $1,000,000$ images for $100$ epochs requires $\sim 5 \times 10^{13}$ operations.
This is why modern deep learning relies on GPU parallelization (CUDA) rather than standard CPU loops.

---

## 2. Space Complexity

### 2.1 Model Size (Inference)
The memory required to store the model is simply the storage of its weights and biases:
- Weights: $I \times H$ and $H \times O$
- Biases: $H$ and $O$

**Space Complexity:** $\mathcal{O}(W)$

### 2.2 Memory During Training
During training, the algorithm must temporarily store the intermediate activations (the outputs of the hidden layers) for every node, because the backpropagation calculus requires the forward-pass activations to compute the gradients.

For a batch of size $B$:
- The network must hold a matrix of size $B \times H$ in memory during the backward pass.
- In this pure Python implementation (which updates sample-by-sample, i.e., $B=1$), the space complexity overhead during training is minimal ($\mathcal{O}(H + O)$).
