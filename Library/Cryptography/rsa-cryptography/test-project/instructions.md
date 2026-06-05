# Running the RSA Test Project

This test project demonstrates how to generate an RSA key pair, encrypt a string message, and decrypt it back using the `core` library.

## Prerequisites
- Python 3.x

## Instructions
1. Open your terminal or command prompt.
2. Navigate to the `test-project` directory:
   ```bash
   cd Library/Cryptography/rsa-cryptography/test-project
   ```
3. Run the python script:
   ```bash
   python app.py
   ```
4. The script will generate a 1024-bit key pair (this may take a few seconds), and then prompt you to enter a message to encrypt.
5. It will output the truncated public and private keys, the encrypted numerical representation, and the successfully decrypted message.
