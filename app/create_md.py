import json
from pathlib import Path
from core.crypto import generate_salt, derive_key, encrypt, decrypt
from core.auth import validate_user

FILES_DIR = Path("data/files")


def create_md_file(username: str, password: str, content: str) -> bool:
    if not validate_user(username, password):
        return False

    salt = generate_salt()
    key  = derive_key(password, salt)
    ciphertext, nonce, tag = encrypt(content.encode(), key)

    payload = {
        "username":   username,
        "salt":       salt.hex(),
        "nonce":      nonce.hex(),
        "tag":        tag.hex(),
        "ciphertext": ciphertext.hex(),
    }

    FILES_DIR.mkdir(parents=True, exist_ok=True)
    file_path = FILES_DIR / f"{username}.enc"

    with open(file_path, "w") as f:
        json.dump(payload, f, indent=2)

    return True


def decrypt_md_file(username: str, password: str) -> str | None:
    file_path = FILES_DIR / f"{username}.enc"

    if not file_path.exists():
        return None

    with open(file_path, "r") as f:
        payload = json.load(f)

    try:
        salt       = bytes.fromhex(payload["salt"])
        nonce      = bytes.fromhex(payload["nonce"])
        tag        = bytes.fromhex(payload["tag"])
        ciphertext = bytes.fromhex(payload["ciphertext"])

        key = derive_key(password, salt)
        decrypted = decrypt(ciphertext, tag, nonce, key)
        return decrypted.decode()

    except Exception:
        # senha errada → GCM lança InvalidTag → capturamos aqui
        return None