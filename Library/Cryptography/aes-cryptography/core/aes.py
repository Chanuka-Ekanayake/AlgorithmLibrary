import struct
from typing import List

# FIPS-197 AES standard S-box
S_BOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# FIPS-197 AES standard Inverse S-box
INV_S_BOX = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

# Round constants (Rcon) for Key Expansion
RC = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a]


# --- Galois Field GF(2^8) Multiplication Helpers ---

def gmul_2(x: int) -> int:
    """Multiplies x by 2 in GF(2^8) modulo x^8 + x^4 + x^3 + x + 1."""
    return ((x << 1) ^ 0x1b) & 0xff if (x & 0x80) else (x << 1) & 0xff


def gmul_3(x: int) -> int:
    """Multiplies x by 3 in GF(2^8)."""
    return gmul_2(x) ^ x


def gmul_9(x: int) -> int:
    """Multiplies x by 9 in GF(2^8)."""
    return gmul_2(gmul_2(gmul_2(x))) ^ x


def gmul_11(x: int) -> int:
    """Multiplies x by 11 in GF(2^8)."""
    g2 = gmul_2(x)
    return gmul_2(gmul_2(g2)) ^ g2 ^ x


def gmul_13(x: int) -> int:
    """Multiplies x by 13 in GF(2^8)."""
    g2 = gmul_2(x)
    g4 = gmul_2(g2)
    return gmul_2(g4) ^ g4 ^ x


def gmul_14(x: int) -> int:
    """Multiplies x by 14 in GF(2^8)."""
    g2 = gmul_2(x)
    g4 = gmul_2(g2)
    return gmul_2(g4) ^ g4 ^ g2


# --- State Conversion Helpers ---

def bytes_to_state(data: bytes) -> List[List[int]]:
    """Converts a 16-byte block into a 4x4 column-major state matrix."""
    return [list(data[i:i+4]) for i in range(0, 16, 4)]


def state_to_bytes(state: List[List[int]]) -> bytes:
    """Converts a 4x4 column-major state matrix back to a 16-byte block."""
    return bytes(b for col in state for b in col)


class AES:
    """
    Modular, pure-Python implementation of the AES block cipher.
    Supports AES-128, AES-192, and AES-256.
    """

    def __init__(self, key: bytes):
        """
        Initializes the AES instance with a key of length 16, 24, or 32 bytes.
        """
        if len(key) == 16:
            self.num_rounds = 10
            self.nk = 4  # Key words length
        elif len(key) == 24:
            self.num_rounds = 12
            self.nk = 6
        elif len(key) == 32:
            self.num_rounds = 14
            self.nk = 8
        else:
            raise ValueError("AES key must be exactly 16, 24, or 32 bytes in length.")

        self.round_keys = self._key_expansion(key)

    def _key_expansion(self, key: bytes) -> List[List[List[int]]]:
        """
        Expands the master key into the required list of round keys.
        """
        # Convert initial key bytes to a list of nk 4-byte words
        words = []
        for i in range(self.nk):
            words.append(list(key[i*4 : (i+1)*4]))

        total_words = 4 * (self.num_rounds + 1)

        for i in range(self.nk, total_words):
            temp = list(words[i - 1])
            if i % self.nk == 0:
                # RotWord: cyclical shift left by 1 byte
                temp = temp[1:] + temp[:1]
                # SubWord: byte substitution using S-Box
                temp = [S_BOX[b] for b in temp]
                # XOR with Round Constant (RC)
                temp[0] ^= RC[i // self.nk]
            elif self.nk > 6 and i % self.nk == 4:
                # Extra SubWord step for AES-256 (nk > 6)
                temp = [S_BOX[b] for b in temp]

            # w[i] = w[i-nk] ^ temp
            prev_word = words[i - self.nk]
            new_word = [prev_word[j] ^ temp[j] for j in range(4)]
            words.append(new_word)

        # Slice the expanded words list into 4-word round keys (each word becomes a column in the key matrix)
        round_keys = []
        for r in range(self.num_rounds + 1):
            round_keys.append(words[r*4 : (r+1)*4])

        return round_keys

    # --- State Transformation Functions ---

    @staticmethod
    def add_round_key(state: List[List[int]], round_key: List[List[int]]) -> None:
        """XORs the state matrix with the current round key."""
        for c in range(4):
            for r in range(4):
                state[c][r] ^= round_key[c][r]

    @staticmethod
    def sub_bytes(state: List[List[int]]) -> None:
        """Substitutes each byte in the state matrix with its corresponding S-Box entry."""
        for c in range(4):
            for r in range(4):
                state[c][r] = S_BOX[state[c][r]]

    @staticmethod
    def inv_sub_bytes(state: List[List[int]]) -> None:
        """Substitutes each byte in the state matrix with its corresponding Inverse S-Box entry."""
        for c in range(4):
            for r in range(4):
                state[c][r] = INV_S_BOX[state[c][r]]

    @staticmethod
    def shift_rows(state: List[List[int]]) -> None:
        """Cyclically shifts the rows of the state matrix to the left by row index offsets."""
        # Row 0: No shift
        # Row 1: Shift left by 1
        t = state[0][1]
        state[0][1] = state[1][1]
        state[1][1] = state[2][1]
        state[2][1] = state[3][1]
        state[3][1] = t

        # Row 2: Shift left by 2
        t0, t1 = state[0][2], state[1][2]
        state[0][2] = state[2][2]
        state[1][2] = state[3][2]
        state[2][2] = t0
        state[3][2] = t1

        # Row 3: Shift left by 3 (Equivalent to shift right by 1)
        t = state[3][3]
        state[3][3] = state[2][3]
        state[2][3] = state[1][3]
        state[1][3] = state[0][3]
        state[0][3] = t

    @staticmethod
    def inv_shift_rows(state: List[List[int]]) -> None:
        """Cyclically shifts the rows of the state matrix to the right by row index offsets."""
        # Row 0: No shift
        # Row 1: Shift right by 1
        t = state[3][1]
        state[3][1] = state[2][1]
        state[2][1] = state[1][1]
        state[1][1] = state[0][1]
        state[0][1] = t

        # Row 2: Shift right by 2
        t0, t1 = state[0][2], state[1][2]
        state[0][2] = state[2][2]
        state[1][2] = state[3][2]
        state[2][2] = t0
        state[3][2] = t1

        # Row 3: Shift right by 3 (Equivalent to shift left by 1)
        t = state[0][3]
        state[0][3] = state[1][3]
        state[1][3] = state[2][3]
        state[2][3] = state[3][3]
        state[3][3] = t

    @staticmethod
    def mix_columns(state: List[List[int]]) -> None:
        """Multiplies each column of the state matrix by the fixed polynomial matrix in GF(2^8)."""
        for c in range(4):
            s0, s1, s2, s3 = state[c][0], state[c][1], state[c][2], state[c][3]
            state[c][0] = gmul_2(s0) ^ gmul_3(s1) ^ s2 ^ s3
            state[c][1] = s0 ^ gmul_2(s1) ^ gmul_3(s2) ^ s3
            state[c][2] = s0 ^ s1 ^ gmul_2(s2) ^ gmul_3(s3)
            state[c][3] = gmul_3(s0) ^ s1 ^ s2 ^ gmul_2(s3)

    @staticmethod
    def inv_mix_columns(state: List[List[int]]) -> None:
        """Multiplies each column of the state matrix by the inverse polynomial matrix in GF(2^8)."""
        for c in range(4):
            s0, s1, s2, s3 = state[c][0], state[c][1], state[c][2], state[c][3]
            state[c][0] = gmul_14(s0) ^ gmul_11(s1) ^ gmul_13(s2) ^ gmul_9(s3)
            state[c][1] = gmul_9(s0) ^ gmul_14(s1) ^ gmul_11(s2) ^ gmul_13(s3)
            state[c][2] = gmul_13(s0) ^ gmul_9(s1) ^ gmul_14(s2) ^ gmul_11(s3)
            state[c][3] = gmul_11(s0) ^ gmul_13(s1) ^ gmul_9(s2) ^ gmul_14(s3)

    # --- Core Single-Block Operations ---

    def encrypt_block(self, plaintext: bytes) -> bytes:
        """Encrypts a single 16-byte block."""
        if len(plaintext) != 16:
            raise ValueError("Plaintext block must be exactly 16 bytes.")

        state = bytes_to_state(plaintext)

        # Initial Round
        self.add_round_key(state, self.round_keys[0])

        # Main Rounds
        for r in range(1, self.num_rounds):
            self.sub_bytes(state)
            self.shift_rows(state)
            self.mix_columns(state)
            self.add_round_key(state, self.round_keys[r])

        # Final Round (No MixColumns)
        self.sub_bytes(state)
        self.shift_rows(state)
        self.add_round_key(state, self.round_keys[self.num_rounds])

        return state_to_bytes(state)

    def decrypt_block(self, ciphertext: bytes) -> bytes:
        """Decrypts a single 16-byte block."""
        if len(ciphertext) != 16:
            raise ValueError("Ciphertext block must be exactly 16 bytes.")

        state = bytes_to_state(ciphertext)

        # Initial Round
        self.add_round_key(state, self.round_keys[self.num_rounds])
        self.inv_shift_rows(state)
        self.inv_sub_bytes(state)

        # Main Rounds
        for r in range(self.num_rounds - 1, 0, -1):
            self.add_round_key(state, self.round_keys[r])
            self.inv_mix_columns(state)
            self.inv_shift_rows(state)
            self.inv_sub_bytes(state)

        # Final Round
        self.add_round_key(state, self.round_keys[0])

        return state_to_bytes(state)

    # --- Multi-Block Modes and Padding ---

    @staticmethod
    def pad(data: bytes) -> bytes:
        """Applies PKCS#7 padding to align data to 16-byte block boundary."""
        pad_len = 16 - (len(data) % 16)
        return data + bytes([pad_len] * pad_len)

    @staticmethod
    def unpad(data: bytes) -> bytes:
        """Removes PKCS#7 padding. Throws ValueError if padding is invalid."""
        if not data:
            raise ValueError("Data is empty. Cannot unpad.")
        pad_len = data[-1]
        if pad_len < 1 or pad_len > 16:
            raise ValueError("Invalid PKCS#7 padding length value.")
        if len(data) < pad_len:
            raise ValueError("Invalid PKCS#7 padding: overall length is too short.")
        # Verify all padding bytes have the correct value
        for i in range(len(data) - pad_len, len(data)):
            if data[i] != pad_len:
                raise ValueError("Invalid PKCS#7 padding byte sequence.")
        return data[:-pad_len]

    def encrypt_ecb(self, plaintext: bytes) -> bytes:
        """Encrypts data in ECB (Electronic Codebook) mode with PKCS#7 padding."""
        padded_data = self.pad(plaintext)
        ciphertext = bytearray()
        for i in range(0, len(padded_data), 16):
            block = padded_data[i : i+16]
            ciphertext.extend(self.encrypt_block(block))
        return bytes(ciphertext)

    def decrypt_ecb(self, ciphertext: bytes) -> bytes:
        """Decrypts data in ECB (Electronic Codebook) mode and removes PKCS#7 padding."""
        if len(ciphertext) % 16 != 0:
            raise ValueError("Ciphertext length must be a multiple of 16 bytes in ECB mode.")
        plaintext = bytearray()
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i : i+16]
            plaintext.extend(self.decrypt_block(block))
        return self.unpad(bytes(plaintext))

    def encrypt_cbc(self, plaintext: bytes, iv: bytes) -> bytes:
        """Encrypts data in CBC (Cipher Block Chaining) mode with PKCS#7 padding."""
        if len(iv) != 16:
            raise ValueError("Initialization Vector (IV) must be exactly 16 bytes.")
        padded_data = self.pad(plaintext)
        ciphertext = bytearray()
        prev_block = iv
        for i in range(0, len(padded_data), 16):
            block = padded_data[i : i+16]
            # XOR with previous ciphertext block (or IV)
            xor_block = bytes(b ^ p for b, p in zip(block, prev_block))
            enc_block = self.encrypt_block(xor_block)
            ciphertext.extend(enc_block)
            prev_block = enc_block
        return bytes(ciphertext)

    def decrypt_cbc(self, ciphertext: bytes, iv: bytes) -> bytes:
        """Decrypts data in CBC (Cipher Block Chaining) mode and removes PKCS#7 padding."""
        if len(iv) != 16:
            raise ValueError("Initialization Vector (IV) must be exactly 16 bytes.")
        if len(ciphertext) % 16 != 0:
            raise ValueError("Ciphertext length must be a multiple of 16 bytes in CBC mode.")
        plaintext = bytearray()
        prev_block = iv
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i : i+16]
            dec_block = self.decrypt_block(block)
            # XOR with previous ciphertext block (or IV)
            plain_block = bytes(d ^ p for d, p in zip(dec_block, prev_block))
            plaintext.extend(plain_block)
            prev_block = block
        return self.unpad(bytes(plaintext))
