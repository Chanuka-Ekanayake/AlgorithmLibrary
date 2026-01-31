# Complexity Analysis: Huffman Coding

Huffman Coding is a greedy algorithm used for lossless data compression. Its efficiency depends on the size of the alphabet (number of unique characters) and the length of the input data.

## 1. Time Complexity

The total time complexity is divided into three main phases:

### 1.1 Frequency Counting: 

We must scan the entire input text of length  once to determine the frequency of each character.

### 1.2 Tree Construction: 

* **:** The number of unique characters in the alphabet.
* We use a **Min-Heap** (Priority Queue) to build the tree.
* Each `heappop` and `heappush` operation takes  time.
* Since we perform these operations  times to merge all nodes into a single tree, the total time is .

### 1.3 Encoding and Decoding: 

* **Encoding:** Once the tree is built, we traverse the input text and replace each character with its binary code ().
* **Decoding:** We traverse the bitstring once, moving down the tree for each bit until we hit a leaf ().

---

## 2. Space Complexity

The space complexity is:


### 2.1 Memory Breakdown

* **Frequency Map:** Stores  character-frequency pairs.
* **Huffman Tree:** A tree with  leaf nodes and  internal nodes ( total nodes).
* **Code Map:** Stores the binary string for each of the  unique characters.

---

## 3. Compression Efficiency (Information Theory)

Huffman coding is optimal for character-by-character encoding. It approaches the **Shannon Entropy** () of the source data:


* : The probability of character  appearing.
* In practice, this means Huffman coding can reduce file sizes by **20% to 80%** depending on the redundancy of the data.

---

## 4. Performance Metrics Table

| Metric | Complexity |
| --- | --- |
| **Tree Building** |  |
| **Encoding Time** |  |
| **Decoding Time** |  |
| **Auxiliary Space** |  |
| **Optimality** | Optimal for prefix-free codes |

---

## 5. Engineering Trade-offs

* **Pros:** Guaranteed optimal prefix-free code; fast encoding/decoding; zero data loss.
* **Cons:** Requires two passes over the data (one to count, one to encode); the "dictionary" (tree) must be stored along with the compressed data to allow for later decoding.