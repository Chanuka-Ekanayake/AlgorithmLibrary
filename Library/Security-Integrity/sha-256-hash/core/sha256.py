"""
SHA-256 Cryptographic Hash Function Core Module

A pure Python implementation of the SHA-256 algorithm.
This is meant for educational purposes to demonstrate the exact bitwise
operations, padding, and block compression math defined in FIPS 180-4.

Author: Algorithm Library
"""

# Initial hash values (first 32 bits of the fractional parts of the square roots of the first 8 primes)
H_INIT = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

# Round constants (first 32 bits of the fractional parts of the cube roots of the first 64 primes)
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

def _rotr(x: int, n: int) -> int:
    """Right rotate (circular right shift) x by n bits, constrained to 32 bits."""
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def _pad_message(message: bytes) -> bytes:
    """
    Pads the message to a multiple of 512 bits (64 bytes).
    1. Append a single '1' bit (0x80 byte).
    2. Append '0' bits until the length is 56 bytes mod 64.
    3. Append the original length in bits as a 64-bit big-endian integer.
    """
    original_bit_len = len(message) * 8
    
    # 1. Append 1 bit (0x80)
    padded = bytearray(message)
    padded.append(0x80)
    
    # 2. Append 0 bits until length is 56 mod 64
    while (len(padded) % 64) != 56:
        padded.append(0x00)
        
    # 3. Append original length in bits (64-bit integer, big endian)
    padded.extend(original_bit_len.to_bytes(8, byteorder='big'))
    
    return bytes(padded)

def sha256(message: str | bytes) -> str:
    """
    Computes the SHA-256 hash of a message.
    
    Args:
        message: The input string or bytes to hash.
        
    Returns:
        A 64-character hexadecimal string representing the 256-bit hash.
    """
    if isinstance(message, str):
        message = message.encode('utf-8')
        
    padded_message = _pad_message(message)
    
    # Initialize the current hash state to the standardized starting values
    h0, h1, h2, h3, h4, h5, h6, h7 = H_INIT
    
    # Process the message in successive 512-bit (64-byte) chunks
    for chunk_offset in range(0, len(padded_message), 64):
        chunk = padded_message[chunk_offset:chunk_offset + 64]
        
        # Break chunk into sixteen 32-bit big-endian words
        w = [0] * 64
        for i in range(16):
            w[i] = int.from_bytes(chunk[i*4 : i*4 + 4], byteorder='big')
            
        # Extend the sixteen 32-bit words into sixty-four 32-bit words
        for i in range(16, 64):
            s0 = _rotr(w[i-15], 7) ^ _rotr(w[i-15], 18) ^ (w[i-15] >> 3)
            s1 = _rotr(w[i-2], 17) ^ _rotr(w[i-2], 19) ^ (w[i-2] >> 10)
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF
            
        # Initialize working variables to current hash value
        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
        
        # Compression function main loop (64 rounds)
        for i in range(64):
            # Sigma1 calculation for e
            S1 = _rotr(e, 6) ^ _rotr(e, 11) ^ _rotr(e, 25)
            # Choose (ch) calculation
            ch = (e & f) ^ ((~e & 0xFFFFFFFF) & g)
            # Temporary word 1
            temp1 = (h + S1 + ch + K[i] + w[i]) & 0xFFFFFFFF
            
            # Sigma0 calculation for a
            S0 = _rotr(a, 2) ^ _rotr(a, 13) ^ _rotr(a, 22)
            # Majority (maj) calculation
            maj = (a & b) ^ (a & c) ^ (b & c)
            # Temporary word 2
            temp2 = (S0 + maj) & 0xFFFFFFFF
            
            # Shift variables down
            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        # Add the compressed chunk to the current hash value
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        h5 = (h5 + f) & 0xFFFFFFFF
        h6 = (h6 + g) & 0xFFFFFFFF
        h7 = (h7 + h) & 0xFFFFFFFF

    # Produce the final hash value (big-endian)
    return ''.join(f"{val:08x}" for val in (h0, h1, h2, h3, h4, h5, h6, h7))

if __name__ == "__main__":
    # Simple validation test against known expected output
    test_str = "hello world"
    # standard sha256("hello world")
    expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    
    print(f"Testing SHA-256 for: '{test_str}'")
    result = sha256(test_str)
    print(f"Calculated: {result}")
    print(f"Expected:   {expected}")
    print(f"Matches:    {result == expected}")
