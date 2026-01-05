# AES-128-CBC File Encryption Implementation - Explanation

## Overview
This project implements the **Advanced Encryption Standard (AES-128)** algorithm in **Cipher Block Chaining (CBC) mode** from scratch using only the Python Standard Library. The implementation encrypts and decrypts arbitrary files using a 128-bit key.

## Key Features

### 1. **AES-128 Algorithm Implementation**
The implementation includes all core AES operations:

- **S-Box and Inverse S-Box**: Substitution tables for byte-level substitution (256 entries each)
- **Key Expansion**: Expands a 128-bit key into 11 round keys (44 words) using:
  - RotWord (rotate word left by one byte)
  - SubWord (S-Box substitution)
  - Round constants (RCON)
  - XOR operations
- **SubBytes**: Non-linear substitution using the S-Box
- **ShiftRows**: Cyclic shift of rows in the state matrix
- **MixColumns**: Galois Field multiplication (GF(2⁸)) for diffusion
- **AddRoundKey**: XOR operation with round key
- **10 Rounds**: 9 full rounds + 1 final round (without MixColumns)

### 2. **CBC Mode (Cipher Block Chaining)**
- Each plaintext block is XORed with the previous ciphertext block before encryption
- The first block is XORed with a random **Initialization Vector (IV)**
- This ensures that identical plaintext blocks produce different ciphertext blocks
- Provides semantic security (same message encrypted twice produces different ciphertexts)

### 3. **PKCS7 Padding**
- Implements PKCS7 padding to handle files of any size
- Adds 1-16 bytes of padding so data length is a multiple of 16 bytes (AES block size)
- Padding value equals the number of padding bytes added
- Allows encryption of files not divisible by 16 bytes

### 4. **Security Features**

#### Random Key Generation
- Uses `os.urandom(16)` to generate a cryptographically secure random 128-bit key
- Key is displayed in hexadecimal format (32 hex characters)
- User must save the key to decrypt the file later

#### Random IV Generation
- Generates a new random 16-byte IV for every encryption using `os.urandom(16)`
- IV is prepended to the encrypted file (first 16 bytes)
- Ensures same plaintext produces different ciphertext each time

#### File Format
Encrypted file structure:
```
[16 bytes: IV][N×16 bytes: Encrypted data blocks]
```

## Technical Implementation Details

### AES State Representation
- Data is organized in a 4×4 byte matrix (column-major order)
- Each block is 16 bytes (128 bits)
- State transformations operate on this matrix structure

### Galois Field Arithmetic
- MixColumns uses GF(2⁸) multiplication with irreducible polynomial 0x11b
- Implements multiplication by 0x02, 0x03, 0x09, 0x0b, 0x0d, 0x0e
- Critical for achieving diffusion in the cipher

### Key Schedule
- 128-bit key (4 words) expanded to 44 words (11 round keys)
- Uses RCON values: [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
- Every 4th word undergoes RotWord, SubWord, and RCON XOR

## Usage

### Encryption
```bash
python aes_encrypt.py encrypt <filename>
```
- Encrypts the file in place (overwrites original)
- Generates and displays a random 128-bit key
- **Important**: Save the displayed key!

### Decryption
```bash
python aes_encrypt.py decrypt <filename> <128_bit_key_hex>
```
- Decrypts the file in place (overwrites encrypted file)
- Requires the exact 128-bit key used for encryption
- Displays decrypted content

### Example
```bash
# Encrypt
python aes_encrypt.py encrypt document.txt
# Output: Key (hex): a1b2c3d4e5f6789012345678901234ab

# Decrypt
python aes_encrypt.py decrypt document.txt a1b2c3d4e5f6789012345678901234ab
```

## Why Only Standard Library?

The implementation uses **only Python Standard Library** modules:
- `os` - for `os.urandom()` (cryptographically secure random number generation)
- `hashlib` - (not used in final version, but available)
- `struct` - (imported but not used in final version)

This demonstrates:
1. **Deep understanding** of the AES algorithm (not relying on libraries)
2. **Educational value** - shows how AES works internally
3. **No external dependencies** - runs on any Python installation

## Security Considerations

1. **Key Management**: The 128-bit key must be stored securely. If lost, data cannot be recovered.
2. **IV Storage**: IV is stored with ciphertext (standard practice for CBC mode)
3. **Padding Oracle**: PKCS7 padding validation could theoretically leak information, but this is a standard implementation
4. **Randomness**: Uses `os.urandom()` which provides cryptographically secure randomness

## Algorithm Flow

### Encryption:
1. Generate random 128-bit key and 16-byte IV
2. Read plaintext file
3. Apply PKCS7 padding
4. For each 16-byte block:
   - XOR with previous ciphertext (or IV for first block)
   - Apply AES encryption (10 rounds)
   - Store ciphertext block
5. Write IV + ciphertext to file

### Decryption:
1. Read encrypted file
2. Extract IV (first 16 bytes) and ciphertext
3. For each 16-byte ciphertext block:
   - Apply AES decryption (10 rounds)
   - XOR with previous ciphertext (or IV for first block)
   - Store plaintext block
4. Remove PKCS7 padding
5. Write decrypted plaintext to file

## Code Structure

- `AES128` class: Core AES implementation
  - Key expansion
  - Encryption/decryption rounds
  - All AES transformations
- `pkcs7_pad()` / `pkcs7_unpad()`: Padding functions
- `encrypt_file()`: File encryption with random key generation
- `decrypt_file()`: File decryption with key validation

## Learning Outcomes

This implementation demonstrates understanding of:
- Block cipher design principles
- AES algorithm internals (SubBytes, ShiftRows, MixColumns, AddRoundKey)
- Block cipher modes of operation (CBC)
- Padding schemes (PKCS7)
- Cryptographic key management
- Galois Field arithmetic

