import os
import sys


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

RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

# --- Helpers ---
def pkcs7_pad(data, block_size=16):
    pad = block_size - (len(data) % block_size)
    return data + bytes([pad]) * pad

def pkcs7_unpad(data):
    if not data:
        raise ValueError("Cannot unpad empty data")
    pad = data[-1]
    if pad < 1 or pad > 16 or data[-pad:] != bytes([pad]) * pad:
        raise ValueError("Invalid padding")
    return data[:-pad]

def generate_key():
    return os.urandom(16)

def key_to_hex(k): 
    return k.hex()

def hex_to_key(h):
    try: 
        k = bytes.fromhex(h)
    except ValueError as e: 
        raise ValueError(f"Invalid hex key: {e}")
    if len(k) != 16: 
        raise ValueError("Key must be 32 hex chars (16 bytes)")
    return k

def passphrase_to_key(text):
    raw = text.encode("utf-8")
    return raw[:16] if len(raw) >= 16 else raw.ljust(16, b"\0")

def parse_key_input(text):
    stripped = text.strip()
    is_hex = len(stripped) == 32 and all(c in "0123456789abcdefABCDEF" for c in stripped)
    if is_hex:
        k = hex_to_key(stripped)
        return k, stripped.lower(), "hex"
    k = passphrase_to_key(stripped)
    return k, k.hex(), "passphrase"

def hex_to_iv(h):
    try: 
        iv = bytes.fromhex(h)
    except ValueError as e: 
        raise ValueError(f"Invalid IV hex: {e}")
    if len(iv) != 16: 
        raise ValueError("IV must be 32 hex chars (16 bytes)")
    return iv

# --- AES primitive ---
class AES128:
    def __init__(self, key_bytes):
        if len(key_bytes) != 16:
            raise ValueError("Key must be 16 bytes")
        self.round_keys = self._expand_key(key_bytes)

    def _expand_key(self, key):
        w = [bytearray(key[i:i+4]) for i in range(0, 16, 4)]
        for i in range(4, 44):
            temp = w[i-1]
            if i % 4 == 0:
                temp = self._sub_word(self._rot_word(temp))
                temp[0] ^= RCON[(i // 4) - 1]
            w.append(self._xor_words(w[i-4], temp))
        rks = []
        for i in range(0, 44, 4):
            rk = b"".join(bytes(w[i+j]) for j in range(4))
            rks.append(rk)
        return rks

    @staticmethod
    def _rot_word(w): 
        return bytearray([w[1], w[2], w[3], w[0]])
    
    @staticmethod
    def _xor_words(a, b): 
        return bytearray([x ^ y for x, y in zip(a, b)])
    
    @staticmethod
    def _gf_mul(a, b):
        res = 0
        for _ in range(8):
            if b & 1: 
                res ^= a
            a <<= 1
            if a & 0x100: 
                a ^= 0x11b
            b >>= 1
        return res & 0xff

    def _sub_word(self, w): 
        return bytearray([S_BOX[b] for b in w])
    
    def _sub_bytes(self, s):
        for c in range(4):
            for r in range(4):
                s[c][r] = S_BOX[s[c][r]]
    
    def _inv_sub_bytes(self, s):
        for c in range(4):
            for r in range(4):
                s[c][r] = INV_S_BOX[s[c][r]]

    def _shift_rows(self, s):
        s[1][0], s[1][1], s[1][2], s[1][3] = s[1][1], s[1][2], s[1][3], s[1][0]
        s[2][0], s[2][1], s[2][2], s[2][3] = s[2][2], s[2][3], s[2][0], s[2][1]
        s[3][0], s[3][1], s[3][2], s[3][3] = s[3][3], s[3][0], s[3][1], s[3][2]

    def _inv_shift_rows(self, s):
        s[1][0], s[1][1], s[1][2], s[1][3] = s[1][3], s[1][0], s[1][1], s[1][2]
        s[2][0], s[2][1], s[2][2], s[2][3] = s[2][2], s[2][3], s[2][0], s[2][1]
        s[3][0], s[3][1], s[3][2], s[3][3] = s[3][1], s[3][2], s[3][3], s[3][0]

    def _mix_columns(self, s):
        for j in range(4):
            a0, a1, a2, a3 = s[0][j], s[1][j], s[2][j], s[3][j]
            s[0][j] = self._gf_mul(0x02, a0) ^ self._gf_mul(0x03, a1) ^ a2 ^ a3
            s[1][j] = a0 ^ self._gf_mul(0x02, a1) ^ self._gf_mul(0x03, a2) ^ a3
            s[2][j] = a0 ^ a1 ^ self._gf_mul(0x02, a2) ^ self._gf_mul(0x03, a3)
            s[3][j] = self._gf_mul(0x03, a0) ^ a1 ^ a2 ^ self._gf_mul(0x02, a3)

    def _inv_mix_columns(self, s):
        for j in range(4):
            a0, a1, a2, a3 = s[0][j], s[1][j], s[2][j], s[3][j]
            s[0][j] = self._gf_mul(0x0e, a0) ^ self._gf_mul(0x0b, a1) ^ self._gf_mul(0x0d, a2) ^ self._gf_mul(0x09, a3)
            s[1][j] = self._gf_mul(0x09, a0) ^ self._gf_mul(0x0e, a1) ^ self._gf_mul(0x0b, a2) ^ self._gf_mul(0x0d, a3)
            s[2][j] = self._gf_mul(0x0d, a0) ^ self._gf_mul(0x09, a1) ^ self._gf_mul(0x0e, a2) ^ self._gf_mul(0x0b, a3)
            s[3][j] = self._gf_mul(0x0b, a0) ^ self._gf_mul(0x0d, a1) ^ self._gf_mul(0x09, a2) ^ self._gf_mul(0x0e, a3)

    @staticmethod
    def _bytes_to_state(block):
        return [[block[r + 4 * c] for r in range(4)] for c in range(4)]

    @staticmethod
    def _state_to_bytes(state):
        out = bytearray(16)
        for c in range(4):
            for r in range(4):
                out[r + 4 * c] = state[c][r]
        return bytes(out)

    def _add_round_key(self, s, rk):
        for c in range(4):
            for r in range(4):
                s[c][r] ^= rk[c * 4 + r]

    def encrypt_block(self, block16):
        s = self._bytes_to_state(block16)
        self._add_round_key(s, self.round_keys[0])
        for rnd in range(1, 10):
            self._sub_bytes(s)
            self._shift_rows(s)
            self._mix_columns(s)
            self._add_round_key(s, self.round_keys[rnd])
        self._sub_bytes(s)
        self._shift_rows(s)
        self._add_round_key(s, self.round_keys[10])
        return self._state_to_bytes(s)

    def decrypt_block(self, block16):
        s = self._bytes_to_state(block16)
        self._add_round_key(s, self.round_keys[10])
        for rnd in range(9, 0, -1):
            self._inv_shift_rows(s)
            self._inv_sub_bytes(s)
            self._add_round_key(s, self.round_keys[rnd])
            self._inv_mix_columns(s)
        self._inv_shift_rows(s)
        self._inv_sub_bytes(s)
        self._add_round_key(s, self.round_keys[0])
        return self._state_to_bytes(s)

# --- CBC file encrypt/decrypt ---
def encrypt_file(path, key_text=None, iv_hex=None):
    if key_text:
        key, key_hex_out, key_source = parse_key_input(key_text)
    else:
        key = generate_key()
        key_hex_out = key_to_hex(key)
        key_source = "random"

    iv = hex_to_iv(iv_hex) if iv_hex else os.urandom(16)
    iv_hex_out = iv.hex()

    with open(path, "rb") as f:
        plain = f.read()

    data = pkcs7_pad(plain)
    aes = AES128(key)
    cipher = bytearray()
    prev = iv
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        xored = bytes(a ^ b for a, b in zip(block, prev))
        enc = aes.encrypt_block(xored)
        cipher.extend(enc)
        prev = enc

    # Save as hex string (dense, simple, 100% reliable!)
    encrypted_bytes = iv + cipher
    
    # Convert to hex - creates dense string of 0-9A-F characters
    hex_string = encrypted_bytes.hex()
    
    with open(path, "w", encoding='utf-8') as f:
        f.write(hex_string)

    print(f"File encrypted: {path}")
    print(f"Key (hex): {key_hex_out} [source: {key_source}]")
    print(f"IV  (hex): {iv_hex_out}")
    return key_hex_out, iv_hex_out

def decrypt_file(path, key_text):
    key, _, _ = parse_key_input(key_text)
    
    # Read hex string and convert back to bytes
    with open(path, "r", encoding='utf-8') as f:
        hex_string = f.read().strip()
    
    # Convert from hex
    raw = bytes.fromhex(hex_string)
    
    if len(raw) < 16:
        raise ValueError("Encrypted file too short (missing IV)")
    iv, cipher = raw[:16], raw[16:]
    if len(cipher) % 16:
        raise ValueError("Ciphertext length must be multiple of 16 bytes")

    aes = AES128(key)
    plain = bytearray()
    prev = iv
    for i in range(0, len(cipher), 16):
        block = cipher[i:i+16]
        dec = aes.decrypt_block(block)
        plain.extend(bytes(a ^ b for a, b in zip(dec, prev)))
        prev = block

    data = pkcs7_unpad(bytes(plain))
    with open(path, "wb") as f:
        f.write(data)

    print(f"File decrypted: {path}")
    return data

# --- Display Helper ---
def display_encrypted_string(ciphertext_bytes):
    """
    Convert raw ciphertext bytes to a dense, displayable string.
    - Keeps printable ASCII (33-126) and high-ASCII symbols (160-255)
    - Replaces control codes (0-32, 127-159) with centered dot ·
    This creates the 'hacker/alien' aesthetic without line breaks.
    """
    result = []
    for byte_val in ciphertext_bytes:
        # Keep printable ASCII (33-126) or high-ASCII (160-255)
        if (33 <= byte_val <= 126) or (160 <= byte_val <= 255):
            result.append(chr(byte_val))
        # Replace control codes (0-32, 127-159) with dot
        else:
            result.append('·')
    
    # Join into single string - no newlines should exist in this output
    dense_string = ''.join(result)
    
    # Safety check: explicitly remove any newlines that might have slipped through
    dense_string = dense_string.replace('\n', '·').replace('\r', '·').replace('\t', '·')
    
    return dense_string

# --- CLI ---
def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Encrypt: python aes_encrypt_simple.py encrypt <file> [<key_or_pass>] [<iv_hex>]")
        print("  Decrypt: python aes_encrypt_simple.py decrypt <file> <key_or_pass>")
        sys.exit(1)
    mode = sys.argv[1].lower()
    filename = sys.argv[2]
    if mode == "encrypt":
        key_arg = sys.argv[3] if len(sys.argv) >= 4 else None
        iv_arg = sys.argv[4] if len(sys.argv) >= 5 else None
        encrypt_file(filename, key_arg, iv_arg)
    elif mode == "decrypt":
        if len(sys.argv) < 4:
            print("Decrypt needs the same key/passphrase used for encryption.")
            sys.exit(1)
        key_arg = sys.argv[3]
        decrypt_file(filename, key_arg)
    else:
        print("Mode must be 'encrypt' or 'decrypt'")
        sys.exit(1)

if __name__ == "__main__":
    main()
