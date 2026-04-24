from core.auth import create_user, validate_user
from pathlib import Path
import shutil

if Path("data").exists():
    shutil.rmtree("data")

print("[TEST 1] Create new user...")
assert create_user("john_doe", "secure_password_123") is True
print()

print("[TEST 2] Duplicate user rejected...")
assert create_user("john_doe", "another_password") is False
print()

print("[TEST 3] Validate with correct password...")
assert validate_user("john_doe", "secure_password_123") is True
print()

print("[TEST 4] Validate with wrong password...")
assert validate_user("john_doe", "wrong_password") is False
print()

print("[TEST 5] Non-existent user rejected...")
assert validate_user("jane_doe", "any_password") is False
print()

print("[TEST 6] Create second user...")
assert create_user("alice", "password_abc") is True
print()

print("[TEST 7] Validate both users...")
assert validate_user("john_doe", "secure_password_123") is True
assert validate_user("alice", "password_abc") is True
print()

print("[SUCCESS] All auth tests passed!")

        elif choice == "3":
            print("[OK] Exiting interactive mode...")
            break

        else:
            print("[ERROR] Invalid option. Please select 1-3")


if __name__ == "__main__":
    print("\nWould you like to:")
    print("A) Run automated tests only")
    print("B) Run automated tests + interactive mode")

    mode = get_input("\nSelect mode (A/B): ").upper()

    if mode == "B":
        interactive_menu()