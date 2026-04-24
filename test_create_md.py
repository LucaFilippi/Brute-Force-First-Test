from app.create_md import create_md_file
from core.auth import create_user
from pathlib import Path
import shutil

# Clean up everything for fresh test (including users.json)
if Path("data").exists():
    shutil.rmtree("data")

# Create a test user first
print("[SETUP] Creating test user...")
create_user("test_user", "secure_password_123")
print()

# Test 1: Create markdown file with correct password
print("[TEST 1] Creating markdown file with correct password...")
content = "# My Secret Document\nThis is encrypted content."
result = create_md_file("test_user", "secure_password_123", content)
assert result is True, "Failed to create markdown file with correct password"
print()

# Test 2: Verify the .enc file exists on disk
print("[TEST 2] Verifying .enc file exists on disk...")
enc_file_path = Path("data/files/test_user.enc")
assert enc_file_path.exists(), "File .enc does not exist on disk"
print(f"[OK] File verified: {enc_file_path}")
print()

# Test 3: Verify file content is JSON
print("[TEST 3] Verifying file content structure...")
import json
with open(enc_file_path, "r") as f:
    payload = json.load(f)
assert "username" in payload, "Missing 'username' in payload"
assert "salt" in payload, "Missing 'salt' in payload"
assert "nonce" in payload, "Missing 'nonce' in payload"
assert "tag" in payload, "Missing 'tag' in payload"
assert "ciphertext" in payload, "Missing 'ciphertext' in payload"
assert payload["username"] == "test_user", "Username mismatch"
print(f"[OK] Payload structure verified")
print()

# Test 4: Try to create file with wrong password
print("[TEST 4] Trying to create file with wrong password...")
result = create_md_file("test_user", "wrong_password", "Some content")
assert result is False, "Should not create file with wrong password"
print("[OK] Creation correctly rejected with wrong password")
print()

# Test 5: Create file for another user
print("[TEST 5] Creating user and file for second user...")
create_user("another_user", "password_456")
result = create_md_file("another_user", "password_456", "# Another Document")
assert result is True, "Failed to create file for second user"
enc_file_path2 = Path("data/files/another_user.enc")
assert enc_file_path2.exists(), "Second .enc file does not exist"
print("[OK] Second file created successfully")
print()

# Test 6: Try to create file for non-existent user
print("[TEST 6] Trying to create file for non-existent user...")
result = create_md_file("non_existent_user", "any_password", "content")
assert result is False, "Should not create file for non-existent user"
print("[OK] Creation correctly rejected for non-existent user")
print()

print("[SUCCESS] All create_md tests passed!")
print(f"[INFO] Created files in: data/files/")
