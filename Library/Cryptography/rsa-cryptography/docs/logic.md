# RSA Logic

The RSA algorithm involves four steps: key generation, key distribution, encryption, and decryption.

## 1. Key Generation
1. **Choose two distinct prime numbers $p$ and $q$.**
   For security purposes, the integers $p$ and $q$ should be chosen at random and should be similar in magnitude but differ in length by a few digits to make factoring harder.
2. **Compute $n = pq$.**
   $n$ is used as the modulus for both the public and private keys. Its length, usually expressed in bits, is the key length.
3. **Compute Carmichael's totient function of the product as $\lambda(n) = \text{lcm}(p-1, q-1)$, or the Euler's totient $\phi(n) = (p-1)(q-1)$.**
   We use $\phi(n)$ in our implementation for simplicity.
4. **Choose an integer $e$ such that $1 < e < \phi(n)$ and $\text{gcd}(e, \phi(n)) = 1$.**
   $e$ is released as the public key exponent. A common choice for $e$ is $65537$ because it's a prime and enables fast exponentiation.
5. **Determine $d$ as $d \equiv e^{-1} \pmod{\phi(n)}$.**
   $d$ is kept as the private key exponent. It is computed using the Extended Euclidean Algorithm.

The **public key** consists of the modulus $n$ and the public (or encryption) exponent $e$.
The **private key** consists of the modulus $n$ and the private (or decryption) exponent $d$, which must be kept secret.

## 2. Encryption
Alice transmits her public key $(n, e)$ to Bob and keeps the private key $(n, d)$ secret. Bob then wishes to send message $M$ to Alice.
He computes the ciphertext $c$:
$c \equiv M^e \pmod n$

## 3. Decryption
Alice can recover $M$ from $c$ by using her private key exponent $d$:
$M \equiv c^d \pmod n$

## Primality Testing
To generate large prime numbers, we generate random candidates and test them using the **Miller-Rabin primality test**, a probabilistic primality test.
