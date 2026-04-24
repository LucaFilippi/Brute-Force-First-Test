# SecureVault — Brute Force Educational Project

> Strong encryption is useless with weak passwords.

---

## Project Overview

SecureVault is an educational cybersecurity project that demonstrates both defensive (secure storage and authentication) and offensive (brute-force attack simulation) techniques.

It implements a real-world cryptographic workflow using:

* AES-256-GCM for file encryption
* PBKDF2-SHA256 for secure key derivation

The goal is to demonstrate how password strength directly impacts security, even when strong encryption is used.

---

## Why This Matters

Modern systems rely on strong encryption algorithms such as AES-256, which are considered secure against direct attacks.

In practice, attackers do not break encryption algorithms. Instead, they target weaker elements in the system — most commonly, user passwords.

If a password is weak, the entire system becomes vulnerable, regardless of how strong the encryption is.

This project demonstrates that:

* Strong cryptography alone is not sufficient
* Password strength is a critical security factor
* Real-world attacks focus on guessing or recovering passwords

---

## Architecture

```plaintext
SecureVault/
├── core/
│   ├── auth.py
│   ├── crypto.py
├── app/
│   ├── create_md.py
├── attacker/
│   ├── brute_force.py
├── main.py
├── main_attacker.py
├── data/
│   ├── users.json
│   └── files/
```

---

## Defensive Features

* User authentication with PBKDF2-SHA256
* Random salt per user
* AES-256-GCM encrypted markdown storage
* Password-based decryption
* Graphical user interface

---

## Offensive Features

* Dictionary-based brute force attack
* Real-time password testing
* Automatic decryption upon success

---

## Cryptography Details

### Password Hashing

* Algorithm: PBKDF2-SHA256
* Iterations: 200,000
* Salt: 16 bytes (random per user)

### File Encryption

* Algorithm: AES-256-GCM
* Key derivation: PBKDF2 (password + salt)
* Nonce: 12 bytes (random per encryption)

---

## Live Attack Example

```plaintext
[+] Testing: 123123
[+] Testing: password
[+] Testing: 123456

[SUCCESS] Password found: 123456
[DECRYPTED] "# My Secret Data"
```

---

## Performance

* PBKDF2 iterations: 200,000
* Brute force speed: ~9 attempts/second
* Encryption/Decryption: <1ms per file

---

## How to Run

### Install dependencies

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

pip install cryptography
```

---

### Run user interface

```bash
python main.py
```

---

### Run attacker interface

```bash
python main_attacker.py
```

---

## Example Workflow

1. Create a user with a password
2. Store an encrypted markdown file
3. Launch the attacker interface
4. Run a brute-force attack using a wordlist
5. Observe password discovery and data decryption

---