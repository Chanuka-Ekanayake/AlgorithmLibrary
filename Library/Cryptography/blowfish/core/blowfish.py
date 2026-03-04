"""
Blowfish Encryption Algorithm
A symmetric-key block cipher utilizing a 16-round Feistel network.
Designed for fast execution and high resistance to brute-force attacks 
via a computationally expensive key expansion phase.
"""

import struct
from typing import List

# Standard Blowfish initialization constants (derived from the fractional part of Pi).
# Note: In a full production file, these arrays contain 18 and 1024 hex values respectively.
# They are truncated here to focus on the algorithmic logic.
INITIAL_P_ARRAY = [
    0x243F6A88, 0x85A308D3, 0x13198A2E, 0x03707344, 0xA4093822, 0x299F31D0,
    0x082EFA98, 0xEC4E6C89, 0x452821E6, 0x38D01377, 0xBE5466CF, 0x34E90C6C,
    0xC0AC29B7, 0xC97C50DD, 0x3F84D5B5, 0xB5470917, 0x9216D5D9, 0x8979FB1B
]

# 4 S-Boxes, each containing 256 32-bit integers
INITIAL_S_BOXES = [
    [0xD1310BA6, 0x98DFB5AC, 0x2FFD72DBD, 0xF010408C, ...], # S-Box 0
    [0xE39ED55F, 0x2863B23C, 0x31815211, 0x2035C015, ...], # S-Box 1
    [0x04C11A53, 0x1E8BA4F4, 0x5EE3D611, 0x05CB802B, ...], # S-Box 2
    [0x36D1FC1F, 0xC56A56CD, 0x2A370501, 0x880C7A4D, ...]  # S-Box 3
]

class BlowfishCipher:
    """
    Cryptographic engine for securing 64-bit data blocks using a symmetric key.
    """
    
    def __init__(self, key: bytes):
        if not (4 <= len(key) <= 56):
            raise ValueError("Blowfish key must be between 4 and 56 bytes.")
            
        # 1. Create mutable copies of the Pi constants
        self.P = list(INITIAL_P_ARRAY)
        # Deep copy the S-boxes to ensure isolation
        self.S = [list(box) for box in INITIAL_S_BOXES]
        
        # 2. Scramble the initial state using the user's key
        self._expand_key(key)

    def _feistel_function(self, x: int) -> int:
        """
        The Cryptographic Mixer (F-Function).
        Splits a 32-bit integer into four 8-bit chunks, passes them through 
        the S-Boxes, and combines them using addition and XOR.
        """
        # Isolate the four 8-bit bytes
        d = x & 0xFF
        c = (x >> 8) & 0xFF
        b = (x >> 16) & 0xFF
        a = (x >> 24) & 0xFF
        
        # S-Box mixing with strict 32-bit boundary enforcement
        res = (self.S[0][a] + self.S[1][b]) & 0xFFFFFFFF
        res = res ^ self.S[2][c]
        res = (res + self.S[3][d]) & 0xFFFFFFFF
        
        return res

    def _expand_key(self, key: bytes) -> None:
        """
        The Key Expansion phase. This is intentionally slow to defend against 
        brute-force password guessing.
        """
        key_len = len(key)
        
        # Step 1: XOR the P-array with the rotating key bytes
        for i in range(18):
            # Construct a 32-bit chunk from the key, cycling if necessary
            key_chunk = (key[(i * 4) % key_len] << 24) | \
                        (key[(i * 4 + 1) % key_len] << 16) | \
                        (key[(i * 4 + 2) % key_len] << 8) | \
                        (key[(i * 4 + 3) % key_len])
            self.P[i] = (self.P[i] ^ key_chunk) & 0xFFFFFFFF
            
        # Step 2: Encrypt an all-zero block, and use the ciphertext to 
        # replace the P-array and S-Boxes iteratively.
        L, R = 0, 0
        
        # Replace the 18 P-array elements
        for i in range(0, 18, 2):
            L, R = self._encrypt_64bit_block(L, R)
            self.P[i] = L
            self.P[i + 1] = R
            
        # Replace the 1024 S-Box elements
        for i in range(4):
            for j in range(0, 256, 2):
                L, R = self._encrypt_64bit_block(L, R)
                self.S[i][j] = L
                self.S[i][j + 1] = R

    def _encrypt_64bit_block(self, L: int, R: int) -> tuple[int, int]:
        """Internal 16-round Feistel encryption on raw 32-bit halves."""
        for i in range(16):
            L = (L ^ self.P[i]) & 0xFFFFFFFF
            R = (R ^ self._feistel_function(L)) & 0xFFFFFFFF
            # Swap L and R
            L, R = R, L
            
        # Final swap undo and post-processing
        L, R = R, L
        R = (R ^ self.P[16]) & 0xFFFFFFFF
        L = (L ^ self.P[17]) & 0xFFFFFFFF
        
        return L, R

    def encrypt_block(self, block: bytes) -> bytes:
        """Encrypts an exact 8-byte (64-bit) payload."""
        if len(block) != 8:
            raise ValueError("Block must be exactly 8 bytes.")
            
        L, R = struct.unpack('>LL', block)
        L, R = self._encrypt_64bit_block(L, R)
        return struct.pack('>LL', L, R)

    def decrypt_block(self, block: bytes) -> bytes:
        """
        Decrypts an exact 8-byte payload. The logic is identical to encryption,
        but the P-array is applied in reverse (from P[17] down to P[0]).
        """
        if len(block) != 8:
            raise ValueError("Block must be exactly 8 bytes.")
            
        L, R = struct.unpack('>LL', block)
        
        # 16-Round Feistel decryption (Reverse P-array)
        for i in range(17, 1, -1):
            L = (L ^ self.P[i]) & 0xFFFFFFFF
            R = (R ^ self._feistel_function(L)) & 0xFFFFFFFF
            L, R = R, L
            
        L, R = R, L
        R = (R ^ self.P[1]) & 0xFFFFFFFF
        L = (L ^ self.P[0]) & 0xFFFFFFFF
        
        return struct.pack('>LL', L, R)