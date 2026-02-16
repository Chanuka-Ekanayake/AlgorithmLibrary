"""
ElGamal Asymmetric Cryptosystem
Based on the Discrete Logarithm Problem (DLP).
Provides non-deterministic encryption where the same plaintext 
yields different ciphertexts each time it is encrypted.
"""

import random
from typing import Tuple, Dict, Any

class ElGamal:
    """
    Implements Key Generation, Encryption, and Decryption 
    using the ElGamal algorithm.
    """

    def __init__(self, p: int = 7919, g: int = 2):
        """
        Args:
            p: A large prime number (defines the cyclic group).
            g: A generator (primitive root) for the group.
        """
        self.p = p
        self.g = g

    def generate_keys(self) -> Dict[str, Any]:
        """
        Generates a Public/Private key pair.
        Public Key: (p, g, y)
        Private Key: x
        """
        # Private key x: Randomly chosen such that 1 < x < p-1
        private_key = random.randint(2, self.p - 2)
        
        # Public key component y: g^x mod p
        public_key_y = pow(self.g, private_key, self.p)
        
        return {
            "public": (self.p, self.g, public_key_y),
            "private": private_key
        }

    def encrypt(self, plaintext: int, public_key: Tuple[int, int, int]) -> Tuple[int, int]:
        """
        Encrypts an integer message.
        Ciphertext is a pair (a, b).
        """
        p_key, g_key, y = public_key

        # Ensure that the provided public key matches this instance's group parameters.
        if p_key != self.p or g_key != self.g:
            raise ValueError("Public key parameters (p, g) do not match this ElGamal instance.")

        if plaintext >= self.p:
            raise ValueError(f"Plaintext must be smaller than prime p ({self.p})")

        # Ephemeral key k: Randomly chosen for each encryption
        # This ensures the encryption is non-deterministic (probabilistic).
        k = random.randint(2, self.p - 2)

        # a = g^k mod p
        a = pow(self.g, k, self.p)

        # b = (y^k * M) mod p
        # y^k mod p is the shared secret
        shared_secret = pow(y, k, self.p)
        b = (shared_secret * plaintext) % self.p
        return (a, b)

    def decrypt(self, ciphertext: Tuple[int, int], private_key: int) -> int:
        """
        Decrypts a ciphertext pair (a, b).
        M = b * (a^x)^-1 mod p
        """
        a, b = ciphertext
        
        # Recover shared secret: a^x mod p
        s = pow(a, private_key, self.p)
        
        # Use Fermat's Little Theorem for the modular inverse: s^(p-2) mod p
        # This works because p is prime.
        s_inv = pow(s, self.p - 2, self.p)
        
        # Plaintext M = b * s_inv mod p
        plaintext = (b * s_inv) % self.p
        
        return plaintext