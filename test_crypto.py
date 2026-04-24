from core.crypto import generate_salt, derive_key, encrypt, decrypt

salt = generate_salt()
print(f"[OK] Salt generated: {salt.hex()}")

password = "test123"
key = derive_key(password, salt)
print(f"[OK] Key derived: {key.hex()}")

plaintext = "secret content"
data_bytes = plaintext.encode()
ciphertext, nonce, tag = encrypt(data_bytes, key)
print(f"[OK] Text encrypted")

decrypted = decrypt(ciphertext, tag, nonce, key)
result = decrypted.decode()
print(f"[OK] Text decrypted: {result}")

assert result == plaintext
print(f"[OK] Decryption verified")

# Verify different nonces and ciphertexts on each encryption
ct1, nonce1, tag1 = encrypt(data_bytes, key)
ct2, nonce2, tag2 = encrypt(data_bytes, key)

assert nonce1 != nonce2
assert ct1 != ct2
print("[OK] Each encryption produces unique nonces and ciphertexts")

print(f"\n[SUCCESS] All tests passed!")
