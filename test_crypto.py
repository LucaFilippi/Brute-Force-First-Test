from core.crypto import generate_salt, derive_key, encrypt, decrypt

# Generate a salt
salt = generate_salt()
print(f"[OK] Salt generated: {salt.hex()}")

# Derive a key from password "teste123"
password = "test123"
key = derive_key(password, salt)
print(f"[OK] Key derived: {key.hex()}")

# Encrypt the plaintext "secret content"
plaintext = "secret content"
data_bytes = plaintext.encode()
ciphertext, nonce, tag = encrypt(data_bytes, key)
print(f"[OK] Text encrypted")
print(f"  - Ciphertext: {ciphertext.hex()}")
print(f"  - Nonce: {nonce.hex()}")
print(f"  - Tag: {tag.hex()}")

# Decrypt and print the result
decrypted = decrypt(ciphertext, tag, nonce, key)
result = decrypted.decode()
print(f"[OK] Text decrypted: {result}")

# Verify decryption worked correctly
assert result == plaintext, "Error: decrypted text does not match original"
print(f"[OK] Decryption verified")

# Encrypt the same text twice
ct1, nonce1, tag1 = encrypt(data_bytes, key)
ct2, nonce2, tag2 = encrypt(data_bytes, key)

assert nonce1 != nonce2, "Nonces should be different!"
assert ct1 != ct2, "Ciphertexts should be different!"
print("[OK] Confirmed: same data, different results on each encryption")

print(f"\n[SUCCESS] All tests passed!")
