import struct

class ChaCha20:
    """
    Implementation of the ChaCha20 stream cipher.
    """
    
    # "expand 32-byte k" in ASCII
    CONSTANTS = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
    
    def __init__(self, key: bytes, nonce: bytes):
        """
        Initializes the ChaCha20 cipher with a 256-bit key and a 96-bit nonce.
        
        Args:
            key (bytes): A 32-byte (256-bit) secret key.
            nonce (bytes): A 12-byte (96-bit) unique nonce.
        """
        if len(key) != 32:
            raise ValueError("Key must be exactly 32 bytes (256 bits).")
        if len(nonce) != 12:
            raise ValueError("Nonce must be exactly 12 bytes (96 bits).")
            
        self.key = key
        self.nonce = nonce
        self.block_counter = 0

    def reset(self, nonce: bytes, block_counter: int = 0) -> None:
        """
        Resets the internal state of the cipher with a new nonce and block counter.

        This allows safely reusing a ChaCha20 instance. For security, the same
        (key, nonce) pair should not be reused with overlapping block counters.

        Args:
            nonce (bytes): A 12-byte (96-bit) unique nonce.
            block_counter (int): The initial 32-bit block counter value. Defaults to 0.
        """
        if len(nonce) != 12:
            raise ValueError("Nonce must be exactly 12 bytes (96 bits).")
        self.nonce = nonce
        self.block_counter = block_counter
    @staticmethod
    def _rotl32(v: int, c: int) -> int:
        """Rotates a 32-bit integer left by c bits."""
        return ((v << c) & 0xFFFFFFFF) | (v >> (32 - c))

    def _quarter_round(self, x: list, a: int, b: int, c: int, d: int) -> None:
        """Performs a ChaCha20 quarter round operation on the state vector x."""
        x[a] = (x[a] + x[b]) & 0xFFFFFFFF
        x[d] = self._rotl32(x[d] ^ x[a], 16)
        
        x[c] = (x[c] + x[d]) & 0xFFFFFFFF
        x[b] = self._rotl32(x[b] ^ x[c], 12)
        
        x[a] = (x[a] + x[b]) & 0xFFFFFFFF
        x[d] = self._rotl32(x[d] ^ x[a], 8)
        
        x[c] = (x[c] + x[d]) & 0xFFFFFFFF
        x[b] = self._rotl32(x[b] ^ x[c], 7)

    def _generate_block(self, counter: int) -> bytes:
        """Generates a 64-byte keystream block for the current counter."""
        # Unpack the 32-byte key into 8 32-bit integers (little-endian)
        key_words = list(struct.unpack('<8I', self.key))
        # Unpack the 12-byte nonce into 3 32-bit integers (little-endian)
        nonce_words = list(struct.unpack('<3I', self.nonce))
        
        # Initialize the 16-word state
        state = [
            self.CONSTANTS[0], self.CONSTANTS[1], self.CONSTANTS[2], self.CONSTANTS[3],
            key_words[0], key_words[1], key_words[2], key_words[3],
            key_words[4], key_words[5], key_words[6], key_words[7],
            counter, nonce_words[0], nonce_words[1], nonce_words[2]
        ]
        
        # Working state for the rounds
        x = list(state)
        
        # 10 double-rounds: each iteration does one column round and one diagonal round (20 rounds total)
        for i in range(0, 20, 2):
            # Column rounds
            self._quarter_round(x, 0, 4,  8, 12)
            self._quarter_round(x, 1, 5,  9, 13)
            self._quarter_round(x, 2, 6, 10, 14)
            self._quarter_round(x, 3, 7, 11, 15)
            # Diagonal rounds
            self._quarter_round(x, 0, 5, 10, 15)
            self._quarter_round(x, 1, 6, 11, 12)
            self._quarter_round(x, 2, 7,  8, 13)
            self._quarter_round(x, 3, 4,  9, 14)
            
        # Add the working state back to the original state
        for i in range(16):
            state[i] = (state[i] + x[i]) & 0xFFFFFFFF
            
        # Serialize the 16 32-bit integers into 64 bytes (little-endian)
        return struct.pack('<16I', *state)

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypts the plaintext using the ChaCha20 cipher.
        (In a stream cipher, encryption and decryption are identical).
        
        Args:
            plaintext (bytes): The data to encrypt.
            
        Returns:
            bytes: The encrypted ciphertext.
        """
        ciphertext = bytearray()
        
        # Process the plaintext in 64-byte blocks
        for i in range(0, len(plaintext), 64):
            key_stream_block = self._generate_block(self.block_counter)
            self.block_counter += 1
            
            # XOR the plaintext with the keystream
            block = plaintext[i:i+64]
            xor_block = bytes(a ^ b for a, b in zip(block, key_stream_block))
            ciphertext.extend(xor_block)
        
        return bytes(ciphertext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypts the ciphertext using the ChaCha20 cipher.
        Because ChaCha20 is symmetric via XOR, decryption is the same as encryption.
        
        Args:
            ciphertext (bytes): The data to decrypt.
            
        Returns:
            bytes: The decrypted plaintext.
        """
        return self.encrypt(ciphertext)
