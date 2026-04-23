import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ITERATIONS  = 200_000
KEY_LENGTH  = 32
SALT_LENGTH = 16
NONCE_LENGTH = 12


def generate_salt() -> bytes:
    return os.urandom(SALT_LENGTH)


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode())


def encrypt(data: bytes, key: bytes) -> tuple[bytes, bytes, bytes]:
    nonce = os.urandom(NONCE_LENGTH)
    aesgcm = AESGCM(key)
    ciphertext_with_tag = aesgcm.encrypt(nonce, data, None)
    ciphertext = ciphertext_with_tag[:-16]
    tag        = ciphertext_with_tag[-16:]
    return ciphertext, nonce, tag


def decrypt(ciphertext: bytes, tag: bytes, nonce: bytes, key: bytes) -> bytes:
    aesgcm = AESGCM(key)
    ciphertext_with_tag = ciphertext + tag
    return aesgcm.decrypt(nonce, ciphertext_with_tag, None)