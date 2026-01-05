#!/usr/bin/env python3
"""
AES-128-CBC File Encryption/Decryption Tool
Implements AES-128 in CBC mode from scratch using only Python Standard Library.
"""

import os
import hashlib
import struct


class AES128:
    """AES-128 implementation from scratch."""
    
    # AES S-Box
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
    
    # Inverse S-Box
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
    
    # Round constants for key expansion
    RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
    
    def __init__(self, key):
        """
        Initialize AES-128 with a 128-bit key.
        
        Args:
            key: bytes, 16-byte key
        """
        if len(key) != 16:
            raise ValueError("Key must be exactly 16 bytes (128 bits)")
        self.key = key
        self.round_keys = self._key_expansion(key)
    
    def _key_expansion(self, key):
        """Expand the 128-bit key into 11 round keys (44 words)."""
        # Convert key bytes to words (4 bytes each)
        w = []
        for i in range(4):
            w.append(key[i*4:(i+1)*4])
        
        # Generate remaining words
        for i in range(4, 44):
            temp = w[i-1]
            if i % 4 == 0:
                # RotWord, SubWord, XOR with Rcon
                temp = self._rot_word(temp)
                temp = self._sub_word(temp)
                temp[0] ^= self.RCON[(i // 4) - 1]
            w.append(self._xor_words(w[i-4], temp))
        
        # Convert words to round keys (11 keys of 16 bytes each)
        round_keys = []
        for i in range(11):
            round_key = b''
            for j in range(4):
                round_key += bytes(w[i*4 + j])
            round_keys.append(round_key)
        
        return round_keys
    
    def _rot_word(self, word):
        """Rotate word left by one byte."""
        return bytearray([word[1], word[2], word[3], word[0]])
    
    def _sub_word(self, word):
        """Apply S-Box substitution to each byte of word."""
        return bytearray([self.S_BOX[b] for b in word])
    
    def _xor_words(self, word1, word2):
        """XOR two words."""
        return bytearray([a ^ b for a, b in zip(word1, word2)])
    
    def _sub_bytes(self, state):
        """Substitute bytes using S-Box."""
        for i in range(4):
            for j in range(4):
                state[i][j] = self.S_BOX[state[i][j]]
    
    def _inv_sub_bytes(self, state):
        """Inverse substitute bytes using inverse S-Box."""
        for i in range(4):
            for j in range(4):
                state[i][j] = self.INV_S_BOX[state[i][j]]
    
    def _shift_rows(self, state):
        """Shift rows of state matrix."""
        # Row 0: no shift
        # Row 1: shift left by 1
        state[1][0], state[1][1], state[1][2], state[1][3] = \
            state[1][1], state[1][2], state[1][3], state[1][0]
        # Row 2: shift left by 2
        state[2][0], state[2][1], state[2][2], state[2][3] = \
            state[2][2], state[2][3], state[2][0], state[2][1]
        # Row 3: shift left by 3
        state[3][0], state[3][1], state[3][2], state[3][3] = \
            state[3][3], state[3][0], state[3][1], state[3][2]
    
    def _inv_shift_rows(self, state):
        """Inverse shift rows of state matrix."""
        # Row 0: no shift
        # Row 1: shift right by 1
        state[1][0], state[1][1], state[1][2], state[1][3] = \
            state[1][3], state[1][0], state[1][1], state[1][2]
        # Row 2: shift right by 2
        state[2][0], state[2][1], state[2][2], state[2][3] = \
            state[2][2], state[2][3], state[2][0], state[2][1]
        # Row 3: shift right by 3
        state[3][0], state[3][1], state[3][2], state[3][3] = \
            state[3][1], state[3][2], state[3][3], state[3][0]
    
    def _gf_multiply(self, a, b):
        """Galois Field multiplication."""
        result = 0
        for _ in range(8):
            if b & 1:
                result ^= a
            a <<= 1
            if a & 0x100:
                a ^= 0x11b  # AES irreducible polynomial
            b >>= 1
        return result & 0xff
    
    def _mix_columns(self, state):
        """Mix columns transformation."""
        for j in range(4):
            s0, s1, s2, s3 = state[0][j], state[1][j], state[2][j], state[3][j]
            state[0][j] = self._gf_multiply(0x02, s0) ^ self._gf_multiply(0x03, s1) ^ s2 ^ s3
            state[1][j] = s0 ^ self._gf_multiply(0x02, s1) ^ self._gf_multiply(0x03, s2) ^ s3
            state[2][j] = s0 ^ s1 ^ self._gf_multiply(0x02, s2) ^ self._gf_multiply(0x03, s3)
            state[3][j] = self._gf_multiply(0x03, s0) ^ s1 ^ s2 ^ self._gf_multiply(0x02, s3)
    
    def _inv_mix_columns(self, state):
        """Inverse mix columns transformation."""
        for j in range(4):
            s0, s1, s2, s3 = state[0][j], state[1][j], state[2][j], state[3][j]
            state[0][j] = self._gf_multiply(0x0e, s0) ^ self._gf_multiply(0x0b, s1) ^ \
                          self._gf_multiply(0x0d, s2) ^ self._gf_multiply(0x09, s3)
            state[1][j] = self._gf_multiply(0x09, s0) ^ self._gf_multiply(0x0e, s1) ^ \
                          self._gf_multiply(0x0b, s2) ^ self._gf_multiply(0x0d, s3)
            state[2][j] = self._gf_multiply(0x0d, s0) ^ self._gf_multiply(0x09, s1) ^ \
                          self._gf_multiply(0x0e, s2) ^ self._gf_multiply(0x0b, s3)
            state[3][j] = self._gf_multiply(0x0b, s0) ^ self._gf_multiply(0x0d, s1) ^ \
                          self._gf_multiply(0x09, s2) ^ self._gf_multiply(0x0e, s3)
    
    def _add_round_key(self, state, round_key):
        """XOR state with round key."""
        for i in range(4):
            for j in range(4):
                state[i][j] ^= round_key[i + j*4]
    
    def _bytes_to_state(self, block):
        """Convert 16-byte block to 4x4 state matrix (column-major order)."""
        state = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                state[j][i] = block[i*4 + j]
        return state
    
    def _state_to_bytes(self, state):
        """Convert 4x4 state matrix to 16-byte block (column-major order)."""
        block = bytearray(16)
        for i in range(4):
            for j in range(4):
                block[i*4 + j] = state[j][i]
        return bytes(block)
    
    def encrypt_block(self, block):
        """Encrypt a single 16-byte block."""
        if len(block) != 16:
            raise ValueError("Block must be exactly 16 bytes")
        
        state = self._bytes_to_state(block)
        
        # Initial round
        self._add_round_key(state, self.round_keys[0])
        
        # 9 main rounds
        for round_num in range(1, 10):
            self._sub_bytes(state)
            self._shift_rows(state)
            self._mix_columns(state)
            self._add_round_key(state, self.round_keys[round_num])
        
        # Final round (no MixColumns)
        self._sub_bytes(state)
        self._shift_rows(state)
        self._add_round_key(state, self.round_keys[10])
        
        return self._state_to_bytes(state)
    
    def decrypt_block(self, block):
        """Decrypt a single 16-byte block."""
        if len(block) != 16:
            raise ValueError("Block must be exactly 16 bytes")
        
        state = self._bytes_to_state(block)
        
        # Initial round
        self._add_round_key(state, self.round_keys[10])
        
        # 9 main rounds
        for round_num in range(9, 0, -1):
            self._inv_shift_rows(state)
            self._inv_sub_bytes(state)
            self._add_round_key(state, self.round_keys[round_num])
            self._inv_mix_columns(state)
        
        # Final round (no InvMixColumns)
        self._inv_shift_rows(state)
        self._inv_sub_bytes(state)
        self._add_round_key(state, self.round_keys[0])
        
        return self._state_to_bytes(state)


def pkcs7_pad(data, block_size=16):
    """Apply PKCS7 padding to data."""
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding


def pkcs7_unpad(data):
    """Remove PKCS7 padding from data."""
    if len(data) == 0:
        raise ValueError("Cannot unpad empty data")
    padding_length = data[-1]
    if padding_length < 1 or padding_length > 16:
        raise ValueError("Invalid padding length")
    if data[-padding_length:] != bytes([padding_length] * padding_length):
        raise ValueError("Invalid padding")
    return data[:-padding_length]


def generate_key():
    """Generate a random 128-bit key."""
    return os.urandom(16)


def key_to_hex(key):
    """Convert 128-bit key bytes to hexadecimal string."""
    return key.hex()


def hex_to_key(hex_string):
    """Convert hexadecimal string to 128-bit key bytes."""
    try:
        key_bytes = bytes.fromhex(hex_string)
        if len(key_bytes) != 16:
            raise ValueError("Key must be exactly 32 hex characters (128 bits)")
        return key_bytes
    except ValueError as e:
        raise ValueError(f"Invalid hex key: {e}")


def encrypt_file(input_filename):
    """
    Encrypt a file using AES-128-CBC with a randomly generated 128-bit key.
    Encrypts the original file in place.
    
    Args:
        input_filename: Path to the file to encrypt
    
    Returns:
        str: The 128-bit key in hexadecimal format (32 hex characters)
    """
    # Generate random 128-bit key
    key = generate_key()
    key_hex = key_to_hex(key)
    
    # Generate random IV
    iv = os.urandom(16)
    
    # Read input file
    with open(input_filename, 'rb') as f:
        plaintext = f.read()
    
    # Apply PKCS7 padding
    padded_plaintext = pkcs7_pad(plaintext)
    
    # Initialize AES
    aes = AES128(key)
    
    # Encrypt in CBC mode
    ciphertext = bytearray()
    previous_block = iv
    
    for i in range(0, len(padded_plaintext), 16):
        block = padded_plaintext[i:i+16]
        # XOR with previous ciphertext block (or IV for first block)
        xored_block = bytes([a ^ b for a, b in zip(block, previous_block)])
        # Encrypt the XORed block
        encrypted_block = aes.encrypt_block(xored_block)
        ciphertext.extend(encrypted_block)
        previous_block = encrypted_block
    
    # Write IV + ciphertext to original file (overwrite)
    with open(input_filename, 'wb') as f:
        f.write(iv)
        f.write(bytes(ciphertext))
    
    print(f"File encrypted successfully: {input_filename}")
    print(f"\n{'='*60}")
    print("IMPORTANT: Save this 128-bit key to decrypt the file:")
    print(f"{'='*60}")
    print(f"Key (hex): {key_hex}")
    print(f"{'='*60}\n")
    
    return key_hex


def decrypt_file(input_filename, key_hex):
    """
    Decrypt a file encrypted with AES-128-CBC.
    Decrypts the file in place (overwrites encrypted file with decrypted content).
    
    Args:
        input_filename: Path to the encrypted file
        key_hex: 128-bit key in hexadecimal format (32 hex characters)
    
    Output:
        Overwrites the encrypted file with decrypted content
    """
    # Convert hex key to bytes
    key = hex_to_key(key_hex)
    
    # Read encrypted file
    with open(input_filename, 'rb') as f:
        encrypted_data = f.read()
    
    if len(encrypted_data) < 16:
        raise ValueError("Encrypted file too short (missing IV)")
    
    # Extract IV (first 16 bytes) and ciphertext
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    
    if len(ciphertext) % 16 != 0:
        raise ValueError("Ciphertext length must be multiple of 16 bytes")
    
    # Initialize AES
    aes = AES128(key)
    
    # Decrypt in CBC mode
    plaintext = bytearray()
    previous_block = iv
    
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        # Decrypt the block
        decrypted_block = aes.decrypt_block(block)
        # XOR with previous ciphertext block (or IV for first block)
        xored_block = bytes([a ^ b for a, b in zip(decrypted_block, previous_block)])
        plaintext.extend(xored_block)
        previous_block = block
    
    # Remove PKCS7 padding
    try:
        unpadded_plaintext = pkcs7_unpad(bytes(plaintext))
    except ValueError as e:
        # Debug: show last few bytes to help diagnose
        last_bytes = bytes(plaintext[-20:]) if len(plaintext) >= 20 else bytes(plaintext)
        raise ValueError(f"Decryption failed - padding error: {e}. Last bytes (hex): {last_bytes.hex()}. This might indicate wrong key or corrupted file.")
    
    # Write decrypted file (overwrite original encrypted file)
    with open(input_filename, 'wb') as f:
        f.write(unpadded_plaintext)
    
    # Print decrypted text to console
    try:
        decrypted_text = unpadded_plaintext.decode('utf-8')
        print(f"\n{'='*60}")
        print("DECRYPTED TEXT:")
        print(f"{'='*60}")
        print(decrypted_text)
        print(f"{'='*60}\n")
    except UnicodeDecodeError:
        print(f"\n{'='*60}")
        print("DECRYPTED DATA (binary file - cannot display as text):")
        print(f"{'='*60}")
        print(f"File size: {len(unpadded_plaintext)} bytes")
        print(f"First 100 bytes (hex): {unpadded_plaintext[:100].hex()}")
        print(f"{'='*60}\n")
    
    print(f"File decrypted successfully: {input_filename}")


# Example usage
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Encrypt: python aes_encrypt.py encrypt <input_file>")
        print("  Decrypt: python aes_encrypt.py decrypt <encrypted_file> <128_bit_key_hex>")
        print("\nExample:")
        print("  python aes_encrypt.py encrypt teksts.txt")
        print("  python aes_encrypt.py decrypt teksts.txt a1b2c3d4e5f6789012345678901234ab")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    filename = sys.argv[2]
    
    if mode == 'encrypt':
        encrypt_file(filename)
    elif mode == 'decrypt':
        if len(sys.argv) < 4:
            print("Error: Decrypt mode requires the 128-bit key in hex format")
            print("Usage: python aes_encrypt.py decrypt <encrypted_file> <128_bit_key_hex>")
            sys.exit(1)
        key_hex = sys.argv[3]
        decrypt_file(filename, key_hex)
    else:
        print(f"Unknown mode: {mode}")
        print("Use 'encrypt' or 'decrypt'")
        sys.exit(1)

