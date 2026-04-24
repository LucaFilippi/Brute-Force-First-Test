import time
from pathlib import Path
from app.create_md import decrypt_md_file

FILES_DIR = Path("data/files")


def attack(username: str, wordlist_path: str) -> tuple | None:
    """
    Tenta quebrar o arquivo criptografado do usuário testando
    cada senha da wordlist.

    Retorna (senha, conteudo) se encontrar, None caso contrário.
    """

    # Passo 1: verifica se o arquivo alvo existe
    enc_file = FILES_DIR / f"{username}.enc"
    if not enc_file.exists():
        print(f"[ERRO] Arquivo '{enc_file}' não encontrado.")
        return None

    # Passo 2: carrega a wordlist
    wordlist = Path(wordlist_path)
    if not wordlist.exists():
        print(f"[ERRO] Wordlist '{wordlist_path}' não encontrada.")
        return None

    with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
        passwords = [line.strip() for line in f if line.strip()]

    total = len(passwords)
    print(f"[INFO] Alvo:     {username}.enc")
    print(f"[INFO] Wordlist: {total} senhas carregadas")
    print(f"[INFO] Iniciando ataque...\n")

    # Passo 3: métricas
    start_time   = time.time()
    attempts     = 0

    # Passo 4: loop principal — o coração do ataque
    for password in passwords:
        attempts += 1

        # mostra progresso a cada 10 tentativas
        if attempts % 10 == 0:
            elapsed  = time.time() - start_time
            rate     = attempts / elapsed if elapsed > 0 else 0
            print(f"  [{attempts:>5}/{total}] testando: '{password:<20}' | {rate:.1f} tentativas/s")

        # tenta descriptografar — se não retornar None, achou a senha
        result = decrypt_md_file(username, password)

        if result is not None:
            elapsed = time.time() - start_time
            rate    = attempts / elapsed if elapsed > 0 else 0

            print(f"\n{'='*52}")
            print(f"  ✓  SENHA ENCONTRADA!")
            print(f"{'='*52}")
            print(f"  Senha:       {password}")
            print(f"  Tentativas:  {attempts} de {total}")
            print(f"  Tempo:       {elapsed:.2f}s")
            print(f"  Velocidade:  {rate:.1f} tentativas/s")
            print(f"{'='*52}")
            print(f"\n[CONTEÚDO DESCRIPTOGRAFADO]\n")
            print(result)
            print()

            return (password, result)

    # Passo 5: wordlist esgotada sem sucesso
    elapsed = time.time() - start_time
    print(f"\n[✗] Senha não encontrada na wordlist.")
    print(f"[INFO] {attempts} tentativas em {elapsed:.2f}s")
    return None