import unittest
import sys
import os

# Add parent directory to system path so imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.aes import AES


class TestAESCore(unittest.TestCase):

    def test_key_sizes(self):
        # 128-bit key (16 bytes)
        aes_128 = AES(bytes([0]*16))
        self.assertEqual(aes_128.num_rounds, 10)

        # 192-bit key (24 bytes)
        aes_192 = AES(bytes([0]*24))
        self.assertEqual(aes_192.num_rounds, 12)

        # 256-bit key (32 bytes)
        aes_256 = AES(bytes([0]*32))
        self.assertEqual(aes_256.num_rounds, 14)

        # Invalid key sizes
        with self.assertRaises(ValueError):
            AES(bytes([0]*15))
        with self.assertRaises(ValueError):
            AES(bytes([0]*31))

    def test_fips_197_test_vector_aes128(self):
        """Verify AES-128 against standard FIPS 197 test vector."""
        key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
        plaintext = bytes.fromhex("00112233445566778899aabbccddeeff")
        expected_ciphertext = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")

        cipher = AES(key)
        ciphertext = cipher.encrypt_block(plaintext)
        self.assertEqual(ciphertext, expected_ciphertext)

        decrypted = cipher.decrypt_block(ciphertext)
        self.assertEqual(decrypted, plaintext)

    def test_pkcs7_padding(self):
        # Test pad
        data = b"Hello"
        padded = AES.pad(data)
        self.assertEqual(len(padded), 16)
        self.assertEqual(padded, b"Hello" + bytes([11]*11))

        # Test unpad
        unpadded = AES.unpad(padded)
        self.assertEqual(unpadded, b"Hello")

        # Test pad multiple of block size
        block_data = b"A" * 16
        padded_block = AES.pad(block_data)
        self.assertEqual(len(padded_block), 32)
        self.assertEqual(padded_block[-16:], bytes([16]*16))

        unpadded_block = AES.unpad(padded_block)
        self.assertEqual(unpadded_block, block_data)

        # Test invalid padding
        with self.assertRaises(ValueError):
            # Padding byte is 0 (invalid)
            AES.unpad(b"A" * 15 + b"\x00")
        with self.assertRaises(ValueError):
            # Padding sequence doesn't match values
            AES.unpad(b"A" * 14 + b"\x01\x02")
        with self.assertRaises(ValueError):
            # Empty input
            AES.unpad(b"")

    def test_ecb_mode(self):
        key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
        cipher = AES(key)

        message = b"This is a longer message to test ECB block cipher mode operations."
        ciphertext = cipher.encrypt_ecb(message)
        decrypted = cipher.decrypt_ecb(ciphertext)

        self.assertEqual(decrypted, message)

    def test_cbc_mode(self):
        key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
        iv = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
        cipher = AES(key)

        message = b"Testing Cipher Block Chaining (CBC) mode with standard IV."
        ciphertext = cipher.encrypt_cbc(message, iv)
        decrypted = cipher.decrypt_cbc(ciphertext, iv)

        self.assertEqual(decrypted, message)

        # Verify that changing IV changes ciphertext but can decrypt with correct IV
        iv_alt = bytes.fromhex("ffffffffffffffffffffffffffffffff")
        ciphertext_alt = cipher.encrypt_cbc(message, iv_alt)
        self.assertNotEqual(ciphertext, ciphertext_alt)
        self.assertEqual(cipher.decrypt_cbc(ciphertext_alt, iv_alt), message)


if __name__ == '__main__':
    unittest.main()
