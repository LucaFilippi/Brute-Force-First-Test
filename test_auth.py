from core.auth import create_user, validate_user
from pathlib import Path
import shutil

# Clean up data directory for fresh test
if Path("data/users.json").exists():
    shutil.rmtree("data")

# Test 1: Create a new user
print("[TEST 1] Creating a new user...")
result = create_user("john_doe", "secure_password_123")
assert result is True, "Failed to create user"
print()

# Test 2: Try to create the same user again (should fail)
print("[TEST 2] Trying to create duplicate user...")
result = create_user("john_doe", "another_password")
assert result is False, "Should not create duplicate user"
print()

# Test 3: Validate user with correct password
print("[TEST 3] Validating user with correct password...")
result = validate_user("john_doe", "secure_password_123")
assert result is True, "Failed to validate user with correct password"
print()

# Test 4: Validate user with incorrect password
print("[TEST 4] Validating user with incorrect password...")
result = validate_user("john_doe", "wrong_password")
assert result is False, "Should not validate with wrong password"
print()

# Test 5: Try to validate non-existent user
print("[TEST 5] Validating non-existent user...")
result = validate_user("jane_doe", "any_password")
assert result is False, "Should not validate non-existent user"
print()

# Test 6: Create another user and validate both
print("[TEST 6] Creating second user...")
result = create_user("alice", "password_abc")
assert result is True, "Failed to create second user"
print()

# Test 7: Validate both users
print("[TEST 7] Validating both users...")
result1 = validate_user("john_doe", "secure_password_123")
result2 = validate_user("alice", "password_abc")
assert result1 is True and result2 is True, "Failed to validate both users"
print()

print("[SUCCESS] All auth tests passed!")
print("[INFO] Data saved to: data/users.json")


def get_input(prompt: str) -> str:
    """Lê input do usuário. Lança SystemExit se não houver terminal disponível."""
    try:
        value = input(prompt).strip()
        return value
    except (EOFError, KeyboardInterrupt):
        # EOFError  → sem terminal real (ex: ambiente de chat, pipe, CI)
        # KeyboardInterrupt → usuário pressionou Ctrl+C
        print("\n[INFO] Sem terminal disponível ou interrompido pelo usuário.")
        raise SystemExit(0)


def interactive_menu():
    """Modo interativo para testar as funções de autenticação manualmente."""
    print("\n" + "=" * 50)
    print("INTERACTIVE AUTH TEST MODE")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Create a new user")
        print("2. Validate user login")
        print("3. Exit")

        choice = get_input("\nSelect option (1-3): ")

        if choice == "1":
            username = get_input("Enter username: ")
            if not username:
                print("[ERROR] Username cannot be empty")
                continue
            password = get_input("Enter password: ")
            if not password:
                print("[ERROR] Password cannot be empty")
                continue
            create_user(username, password)

        elif choice == "2":
            username = get_input("Enter username: ")
            if not username:
                print("[ERROR] Username cannot be empty")
                continue
            password = get_input("Enter password: ")
            validate_user(username, password)

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