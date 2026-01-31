# User Guide: Binary Payload Optimizer (Huffman)

This tool demonstrates how to reduce the footprint of software metadata.

## How it Works
The `HuffmanCoder` builds a frequency map of all characters in `sample_data.txt`. It then creates a custom binary tree where the most common characters (like spaces or brackets) are represented by just a few bits, while rare characters get longer codes.

## Instructions
1. Navigate to the `test-project` directory.
2. Run the application:
   ```bash
   python app.py