import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path

# garante que imports funcionam a partir da raiz do projeto
sys.path.insert(0, str(Path(__file__).parent))

from core.auth import create_user, validate_user
from app.create_md import create_md_file, decrypt_md_file

# ── Paleta & constantes ────────────────────────────────────────────────────────
BG        = "#0d0d0d"
PANEL     = "#141414"
BORDER    = "#222222"
ACCENT    = "#00ff88"
ACCENT2   = "#00cc66"
DANGER    = "#ff4455"
TEXT      = "#e8e8e8"
MUTED     = "#555555"
FONT_MONO = ("Courier New", 11)
FONT_HEAD = ("Courier New", 22, "bold")
FONT_SUB  = ("Courier New", 10)
FONT_BTN  = ("Courier New", 11, "bold")
FONT_LBL  = ("Courier New", 10)


def styled_entry(parent, show=None):
    e = tk.Entry(
        parent, show=show,
        bg=PANEL, fg=TEXT, insertbackground=ACCENT,
        relief="flat", bd=0,
        highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT,
        font=FONT_MONO, width=28,
    )
    return e


def styled_btn(parent, text, command, color=ACCENT, danger=False):
    fg = BG if not danger else "#fff"
    bg = color if not danger else DANGER
    b = tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=fg, activebackground=ACCENT2, activeforeground=BG,
        relief="flat", bd=0, cursor="hand2",
        font=FONT_BTN, padx=18, pady=8,
    )
    return b


def labeled_entry(parent, label, show=None, pady=4):
    tk.Label(parent, text=label, bg=PANEL, fg=MUTED, font=FONT_LBL, anchor="w").pack(fill="x", padx=32)
    e = styled_entry(parent, show=show)
    e.pack(padx=32, pady=(0, pady), ipady=6, fill="x")
    return e


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔐 SecureVault")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.geometry("460x540")
        self.current_user = None
        self.current_pass = None
        self._frame = None
        self.show_frame(LoginScreen)

    def show_frame(self, FrameClass):
        if self._frame:
            self._frame.destroy()
        self._frame = FrameClass(self)
        self._frame.pack(fill="both", expand=True)


# ── Tela de Login / Registro ───────────────────────────────────────────────────
class LoginScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._build()

    def _build(self):
        # header
        tk.Label(self, text="SecureVault", bg=BG, fg=ACCENT, font=FONT_HEAD).pack(pady=(48, 4))
        tk.Label(self, text="encrypted markdown storage", bg=BG, fg=MUTED, font=FONT_SUB).pack(pady=(0, 36))

        # painel
        panel = tk.Frame(self, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
        panel.pack(padx=40, fill="x")

        tk.Label(panel, text="", bg=PANEL).pack(pady=8)

        self.user_e = labeled_entry(panel, "USERNAME")
        self.pass_e = labeled_entry(panel, "PASSWORD", show="•")

        tk.Label(panel, text="", bg=PANEL).pack(pady=4)

        btn_row = tk.Frame(panel, bg=PANEL)
        btn_row.pack(padx=32, fill="x", pady=(0, 24))

        styled_btn(btn_row, "LOGIN", self._login).pack(side="left", expand=True, fill="x", padx=(0, 6))
        styled_btn(btn_row, "REGISTER", self._register, color=BORDER).pack(side="left", expand=True, fill="x", padx=(6, 0))

        tk.Label(panel, text="", bg=PANEL).pack()

        # rodapé
        tk.Label(self, text="AES-256-GCM · PBKDF2-SHA256", bg=BG, fg=MUTED, font=FONT_SUB).pack(pady=(24, 0))

    def _login(self):
        u, p = self.user_e.get().strip(), self.pass_e.get()
        if not u or not p:
            messagebox.showwarning("Atenção", "Preencha usuário e senha.")
            return
        if validate_user(u, p):
            self.master.current_user = u
            self.master.current_pass = p
            self.master.show_frame(DashboardScreen)
        else:
            messagebox.showerror("Acesso negado", "Usuário ou senha incorretos.")

    def _register(self):
        u, p = self.user_e.get().strip(), self.pass_e.get()
        if not u or not p:
            messagebox.showwarning("Atenção", "Preencha usuário e senha.")
            return
        if len(p) < 6:
            messagebox.showwarning("Senha fraca", "Use ao menos 6 caracteres.")
            return
        if create_user(u, p):
            self.master.current_user = u
            self.master.current_pass = p
            self.master.show_frame(DashboardScreen)
        else:
            messagebox.showerror("Erro", "Usuário já existe.")


# ── Dashboard ──────────────────────────────────────────────────────────────────
class DashboardScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._build()

    def _build(self):
        u = self.master.current_user

        # header
        header = tk.Frame(self, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
        header.pack(fill="x")
        tk.Label(header, text=f"  🔐 SecureVault", bg=PANEL, fg=ACCENT, font=FONT_BTN).pack(side="left", pady=14, padx=8)
        tk.Label(header, text=f"logged in as {u}", bg=PANEL, fg=MUTED, font=FONT_SUB).pack(side="left")
        styled_btn(header, "LOGOUT", self._logout, color=BORDER).pack(side="right", padx=12, pady=8)

        # botões principais
        center = tk.Frame(self, bg=BG)
        center.pack(expand=True)

        tk.Label(center, text="What would you like to do?", bg=BG, fg=MUTED, font=FONT_SUB).pack(pady=(0, 24))

        styled_btn(center, "✎  CREATE MARKDOWN", self._go_create).pack(fill="x", pady=6, ipady=6)
        styled_btn(center, "🔓  VIEW MARKDOWN",   self._go_view,  color="#1a1a2e").pack(fill="x", pady=6, ipady=6)

    def _logout(self):
        self.master.current_user = None
        self.master.current_pass = None
        self.master.show_frame(LoginScreen)

    def _go_create(self):
        self.master.show_frame(CreateScreen)

    def _go_view(self):
        self.master.show_frame(ViewScreen)


# ── Criar Markdown ─────────────────────────────────────────────────────────────
class CreateScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._build()

    def _build(self):
        tk.Label(self, text="Create Markdown", bg=BG, fg=ACCENT, font=("Courier New", 16, "bold")).pack(pady=(32, 4))
        tk.Label(self, text="content will be encrypted with your password", bg=BG, fg=MUTED, font=FONT_SUB).pack(pady=(0, 16))

        panel = tk.Frame(self, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
        panel.pack(padx=40, fill="both", expand=True)

        tk.Label(panel, text="CONTENT", bg=PANEL, fg=MUTED, font=FONT_LBL, anchor="w").pack(fill="x", padx=16, pady=(16, 4))

        self.text = tk.Text(
            panel, bg=BG, fg=TEXT, insertbackground=ACCENT,
            relief="flat", bd=0, font=FONT_MONO,
            highlightthickness=1, highlightbackground=BORDER,
            wrap="word", height=10,
        )
        self.text.pack(padx=16, fill="both", expand=True, ipady=4)

        btn_row = tk.Frame(panel, bg=PANEL)
        btn_row.pack(fill="x", padx=16, pady=16)
        styled_btn(btn_row, "BACK", lambda: self.master.show_frame(DashboardScreen), color=BORDER).pack(side="left")
        styled_btn(btn_row, "ENCRYPT & SAVE", self._save).pack(side="right")

    def _save(self):
        content = self.text.get("1.0", "end").strip()
        if not content:
            messagebox.showwarning("Atenção", "Escreva algum conteúdo antes de salvar.")
            return
        u = self.master.current_user
        p = self.master.current_pass
        if create_md_file(u, p, content):
            messagebox.showinfo("Sucesso", "Arquivo criptografado e salvo!")
            self.master.show_frame(DashboardScreen)
        else:
            messagebox.showerror("Erro", "Não foi possível salvar o arquivo.")


# ── Ver Markdown ───────────────────────────────────────────────────────────────
class ViewScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._build()

    def _build(self):
        tk.Label(self, text="View Markdown", bg=BG, fg=ACCENT, font=("Courier New", 16, "bold")).pack(pady=(32, 4))
        tk.Label(self, text="confirm your password to decrypt", bg=BG, fg=MUTED, font=FONT_SUB).pack(pady=(0, 20))

        panel = tk.Frame(self, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
        panel.pack(padx=40, fill="x")

        tk.Label(panel, text="", bg=PANEL).pack(pady=6)
        self.pass_e = labeled_entry(panel, "CONFIRM PASSWORD", show="•")

        btn_row = tk.Frame(panel, bg=PANEL)
        btn_row.pack(fill="x", padx=32, pady=(8, 20))
        styled_btn(btn_row, "BACK", lambda: self.master.show_frame(DashboardScreen), color=BORDER).pack(side="left")
        styled_btn(btn_row, "DECRYPT", self._decrypt).pack(side="right")

        tk.Label(panel, text="", bg=PANEL).pack()

        # área de resultado
        self.result_frame = tk.Frame(self, bg=BG)
        self.result_frame.pack(padx=40, fill="both", expand=True, pady=(16, 0))

    def _decrypt(self):
        p = self.pass_e.get()
        u = self.master.current_user

        # limpa resultado anterior
        for w in self.result_frame.winfo_children():
            w.destroy()

        result = decrypt_md_file(u, p)

        if result is None:
            # senha errada → GCM rejeitou → mostra aviso visual
            tk.Label(
                self.result_frame,
                text="⚠  DECRYPTION FAILED",
                bg=BG, fg=DANGER, font=("Courier New", 12, "bold")
            ).pack(pady=(8, 4))
            tk.Label(
                self.result_frame,
                text="Wrong password — AES-GCM tag mismatch",
                bg=BG, fg=MUTED, font=FONT_SUB
            ).pack()
        else:
            tk.Label(
                self.result_frame,
                text="✓  DECRYPTED SUCCESSFULLY",
                bg=BG, fg=ACCENT, font=("Courier New", 12, "bold")
            ).pack(pady=(8, 8))
            box = tk.Text(
                self.result_frame,
                bg=PANEL, fg=TEXT, font=FONT_MONO,
                relief="flat", bd=0,
                highlightthickness=1, highlightbackground=BORDER,
                wrap="word", height=8, state="normal",
            )
            box.insert("1.0", result)
            box.config(state="disabled")
            box.pack(fill="both", expand=True, ipady=6)


if __name__ == "__main__":
    app = App()
    app.mainloop()