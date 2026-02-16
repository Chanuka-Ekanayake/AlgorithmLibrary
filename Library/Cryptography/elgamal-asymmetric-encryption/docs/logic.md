# Algorithm Logic: ElGamal Cryptosystem

## 1. The Mathematical Foundation

ElGamal security is built on the **Discrete Logarithm Problem (DLP)**.

- It is easy to calculate .
- It is computationally "hard" to find if you only know , , and .

This is a "trapdoor function"—a mathematical operation that is easy to do in one direction but virtually impossible to reverse without a specific piece of information (the private key).

---

## 2. Key Components

The system uses a **Finite Cyclic Group** defined by a large prime and a generator .

- **Private Key ():** A secret random integer known only to the receiver.
- **Public Key ():** Calculated as . This is shared with the world.

---

## 3. The Encryption Logic (Probabilistic)

To encrypt a message , the sender chooses a **new, random ephemeral key ** for every transaction.

1. **Shared Secret ():** The sender calculates . Because , the secret is actually .
2. **Ciphertext Part 1 ():** The sender calculates . This "masks" the ephemeral key.
3. **Ciphertext Part 2 ():** The sender obscures the message: .

Because is random, will look different every time it is encrypted, preventing pattern analysis attacks.

---

## 4. The Decryption Logic

The receiver uses their private key to "unmask" the shared secret from the ciphertext part .

1. **Recover Secret:** The receiver calculates .

   > (Since , this is , which is the exact same secret the sender used!)

2. **Remove Mask:** The receiver calculates the **Modular Multiplicative Inverse** of the secret () and multiplies it by .
3. **Result:** .

---

## 5. Why it fits the Marketplace

In your 2026 marketplace, ElGamal is used for **Digital Envelopes**:

- **License Keys:** When a user buys a software model, the system encrypts the license key using the user's ElGamal public key.
- **Privacy:** Only the user's local machine (holding the private key) can decrypt the license, ensuring that even if your marketplace database is breached, the license keys remain secure.
