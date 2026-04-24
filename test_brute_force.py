from attacker.brute_force import attack
from core.auth import create_user
from app.create_md import create_md_file
from pathlib import Path
import shutil

# Clean up for fresh test
if Path("data").exists():
    shutil.rmtree("data")

# Cria wordlist temporária para os testes
WORDLIST = Path("data/test_wordlist.txt")
Path("data").mkdir(exist_ok=True)
WORDLIST.write_text("\n".join([
    "123456", "password", "admin", "qwerty",
    "letmein", "monkey", "dragon", "senha123",
    "gato123", "cachorro", "futebol", "brasil",
    "minhasenha", "teste123", "segredo", "root",
]))

# ── Setup ──────────────────────────────────────────────────────────────────────
print("[SETUP] Criando usuários de teste...")
create_user("fraca_user",  "senha123")         # senha ESTÁ na wordlist
create_user("forte_user",  "Xk#9mP!qL2@vN")   # senha NÃO está na wordlist
create_user("vazio_user",  "qualquer")          # sem arquivo .enc

create_md_file("fraca_user", "senha123",       "# Segredo\nDados sensíveis aqui.")
create_md_file("forte_user", "Xk#9mP!qL2@vN", "# Segredo\nEsse nunca vai cair.")
print()

# ── Test 1: senha fraca — deve ser encontrada ──────────────────────────────────
print("[TEST 1] Ataque em senha fraca (esperado: sucesso)...")
result = attack("fraca_user", str(WORDLIST))
assert result is not None,         "Deveria encontrar a senha fraca"
assert result[0] == "senha123",    "Senha encontrada errada"
assert "Dados sensíveis" in result[1], "Conteúdo descriptografado incorreto"
print("[OK] Senha fraca quebrada corretamente\n")

# ── Test 2: senha forte — wordlist não deve cobrir ─────────────────────────────
print("[TEST 2] Ataque em senha forte (esperado: falha)...")
result = attack("forte_user", str(WORDLIST))
assert result is None, "Não deveria encontrar senha forte na wordlist"
print("[OK] Senha forte resistiu ao ataque\n")

# ── Test 3: arquivo .enc inexistente ──────────────────────────────────────────
print("[TEST 3] Ataque em usuário sem arquivo .enc (esperado: erro)...")
result = attack("vazio_user", str(WORDLIST))
assert result is None, "Deveria retornar None para arquivo inexistente"
print("[OK] Arquivo inexistente tratado corretamente\n")

# ── Test 4: wordlist inexistente ──────────────────────────────────────────────
print("[TEST 4] Wordlist inexistente (esperado: erro)...")
result = attack("fraca_user", "data/nao_existe.txt")
assert result is None, "Deveria retornar None para wordlist inexistente"
print("[OK] Wordlist inexistente tratada corretamente\n")

# ── Test 5: usuário inexistente ───────────────────────────────────────────────
print("[TEST 5] Usuário inexistente (esperado: erro)...")
result = attack("fantasma", str(WORDLIST))
assert result is None, "Deveria retornar None para usuário inexistente"
print("[OK] Usuário inexistente tratado corretamente\n")

print("=" * 52)
print("  [SUCCESS] Todos os testes do brute force passaram!")
print("=" * 52)