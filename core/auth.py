import json
import os
from pathlib import Path
from core.crypto import generate_salt, derive_key

# Fixed path for users file
USERS_FILE = Path("data/users.json")


def _load_users() -> dict:
    """Load users.json and return a dictionary. Returns empty dict if file does not exist."""
    if not USERS_FILE.exists():
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def _save_users(users: dict) -> None:
    """Save users dictionary to users.json."""
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def create_user(username: str, password: str) -> bool:
    users = _load_users()

    if username in users:
        print(f"[ERROR] User '{username}' already exists.")
        return False

    # Generate salt and derive password hash
    salt = generate_salt()
    password_hash = derive_key(password, salt)

    # Save everything as hex to store as text in JSON
    users[username] = {
        "password_hash": password_hash.hex(),
        "salt": salt.hex(),
    }

    _save_users(users)
    print(f"[OK] User '{username}' created successfully.")
    return True


def validate_user(username: str, password: str) -> bool:
    users = _load_users()

    if username not in users:
        print(f"[ERROR] User '{username}' not found.")
        return False

    # Retrieve saved salt and hash - convert from hex back to bytes
    saved_salt = bytes.fromhex(users[username]["salt"])
    saved_hash = bytes.fromhex(users[username]["password_hash"])

    # Recalculate hash with the provided password
    attempt_hash = derive_key(password, saved_salt)

    # Compare - if they match, password is correct
    if attempt_hash == saved_hash:
        print(f"[OK] Login for '{username}' validated.")
        return True
    else:
        print(f"[ERROR] Incorrect password for '{username}'.")
        return False