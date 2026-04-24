from app.create_md import create_md_file
from core.auth import create_user
from pathlib import Path
import shutil
import json

if Path("data").exists():
    shutil.rmtree("data")

print("[SETUP] Creating test user...")
create_user("test_user", "secure_password_123")
print()

print("[TEST 1] Create file with correct password...")
content = "# My Secret Document\nThis is encrypted content."
assert create_md_file("test_user", "secure_password_123", content) is True
print()

print("[TEST 2] Verify .enc file exists on disk...")
enc_file_path = Path("data/files/test_user.enc")
assert enc_file_path.exists()
print(f"[OK] File verified: {enc_file_path}")
print()

print("[TEST 3] Verify file structure...")
with open(enc_file_path, "r") as f:
    payload = json.load(f)
assert all(key in payload for key in ["username", "salt", "nonce", "tag", "ciphertext"])
assert payload["username"] == "test_user"
print("[OK] Payload structure verified")
print()

print("[TEST 4] Reject creation with wrong password...")
assert create_md_file("test_user", "wrong_password", "content") is False
print("[OK] Correctly rejected")
print()

print("[TEST 5] Create file for second user...")
create_user("another_user", "password_456")
assert create_md_file("another_user", "password_456", "# Another Document") is True
assert Path("data/files/another_user.enc").exists()
print("[OK] Second file created")
print()

print("[TEST 6] Reject creation for non-existent user...")
assert create_md_file("non_existent_user", "any_password", "content") is False
print("[OK] Correctly rejected")
print()

print("[SUCCESS] All create_md tests passed!")
