import tkinter as tk
from tkinter import messagebox
import sys
import json
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.auth import _load_users
from attacker.brute_force import attack

# Cyberpunk color palette
BG        = "#0a0e27"
PANEL     = "#0f1419"
BORDER    = "#1a1f3a"
ACCENT    = "#00ffff"
ACCENT2   = "#0099ff"
DANGER    = "#ff0066"
CRITICAL  = "#ff3300"
SUCCESS   = "#00ff00"
TEXT      = "#ffffff"
MUTED     = "#666688"
FONT_MONO = ("Courier New", 10)
FONT_HEAD = ("Courier New", 20, "bold")
FONT_SUB  = ("Courier New", 9)
FONT_BTN  = ("Courier New", 10, "bold")


def styled_entry(parent, show=None):
    e = tk.Entry(
        parent, show=show,
        bg=PANEL, fg=TEXT, insertbackground=ACCENT,
        relief="flat", bd=0,
        highlightthickness=2, highlightbackground=ACCENT, highlightcolor=DANGER,
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
        font=FONT_BTN, padx=14, pady=6,
    )
    return b


class AttackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⚔ HACKER TERMINAL")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.geometry("580x620")
        self.selected_user = None
        self.cracked_password = None
        self.cracked_content = None
        self._frame = None
        self.show_frame(TargetSelectionScreen)

    def show_frame(self, FrameClass):
        if self._frame:
            self._frame.destroy()
        self._frame = FrameClass(self)
        self._frame.pack(fill="both", expand=True)


class TargetSelectionScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=20, pady=(24, 8))

        tk.Label(header, text=">>> SYSTEM BREACH <<<", bg=BG, fg=DANGER, font=FONT_HEAD).pack()
        tk.Label(header, text="[ TARGET SELECTION MODE ]", bg=BG, fg=ACCENT, font=FONT_SUB).pack()
        tk.Label(header, text="", bg=BG).pack()

        users = _load_users()
        if not users:
            tk.Label(self, text="❌ NO TARGETS AVAILABLE", bg=BG, fg=CRITICAL, font=FONT_BTN).pack(pady=40)
            styled_btn(self, "EXIT", lambda: self.master.quit()).pack(pady=10)
            return

        panel = tk.Frame(self, bg=PANEL, highlightthickness=2, highlightbackground=BORDER)
        panel.pack(padx=20, fill="both", expand=True, pady=(0, 16))

        tk.Label(panel, text="[ AVAILABLE TARGETS ]", bg=PANEL, fg=ACCENT, font=FONT_SUB).pack(anchor="w", padx=12, pady=(12, 8))

        listbox_frame = tk.Frame(panel, bg=PANEL)
        listbox_frame.pack(padx=12, fill="both", expand=True)

        scrollbar = tk.Scrollbar(listbox_frame, bg=BORDER, highlightthickness=0)
        scrollbar.pack(side="right", fill="y")

        self.user_listbox = tk.Listbox(
            listbox_frame, bg=PANEL, fg=SUCCESS, font=FONT_MONO,
            relief="flat", bd=0, highlightthickness=0,
            yscrollcommand=scrollbar.set, height=10,
        )
        self.user_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.user_listbox.yview)

        for username in sorted(users.keys()):
            self.user_listbox.insert(tk.END, f"» {username}")

        tk.Label(panel, text="", bg=PANEL).pack(pady=4)

        btn_frame = tk.Frame(panel, bg=PANEL)
        btn_frame.pack(fill="x", padx=12, pady=(0, 12))

        styled_btn(btn_frame, "◄ CANCEL", lambda: self.master.quit(), color=BORDER).pack(side="left")
        styled_btn(btn_frame, "INITIATE ATTACK ►", self._select_target, color=CRITICAL).pack(side="right")

    def _select_target(self):
        try:
            idx = self.user_listbox.curselection()[0]
            user = self.user_listbox.get(idx).replace("» ", "")
            self.master.selected_user = user
            self.master.show_frame(WordlistSelectionScreen)
        except IndexError:
            messagebox.showwarning("⚠ WARNING", "Select a target first!")


class WordlistSelectionScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=20, pady=(24, 8))

        tk.Label(header, text=">>> WORDLIST SELECTION <<<", bg=BG, fg=ACCENT, font=FONT_HEAD).pack()
        tk.Label(header, text=f"[ TARGET: {self.master.selected_user} ]", bg=BG, fg=DANGER, font=FONT_SUB).pack()
        tk.Label(header, text="", bg=BG).pack()

        panel = tk.Frame(self, bg=PANEL, highlightthickness=2, highlightbackground=BORDER)
        panel.pack(padx=20, fill="both", expand=True, pady=(0, 16))

        tk.Label(panel, text="WORDLIST PATH", bg=PANEL, fg=MUTED, font=FONT_SUB, anchor="w").pack(fill="x", padx=16, pady=(12, 4))

        self.wordlist_entry = styled_entry(panel)
        self.wordlist_entry.insert(0, "wordlist.txt")
        self.wordlist_entry.pack(padx=16, pady=(0, 16), ipady=6, fill="x")

        tk.Label(panel, text="[ COMMON WORDLISTS ]", bg=PANEL, fg=ACCENT, font=FONT_SUB).pack(anchor="w", padx=16, pady=(4, 8))

        common = ["wordlist.txt", "rockyou.txt", "common.txt", "passwords.txt"]
        for name in common:
            tk.Button(
                panel, text=f"► {name}", bg=BORDER, fg=ACCENT,
                relief="flat", bd=0, cursor="hand2", font=FONT_SUB,
                command=lambda n=name: self.wordlist_entry.delete(0, tk.END) or self.wordlist_entry.insert(0, n)
            ).pack(anchor="w", padx=16, pady=2)

        tk.Label(panel, text="", bg=PANEL).pack()

        btn_row = tk.Frame(panel, bg=PANEL)
        btn_row.pack(fill="x", padx=16, pady=(0, 16))

        styled_btn(btn_row, "◄ BACK", lambda: self.master.show_frame(TargetSelectionScreen), color=BORDER).pack(side="left")
        styled_btn(btn_row, "START BRUTE FORCE ►", self._start_attack, color=CRITICAL).pack(side="right")

    def _start_attack(self):
        wordlist = self.wordlist_entry.get().strip()
        if not wordlist:
            messagebox.showwarning("⚠ WARNING", "Enter wordlist path!")
            return
        if not Path(wordlist).exists():
            messagebox.showerror("❌ ERROR", f"Wordlist not found: {wordlist}")
            return

        self.master.show_frame(AttackScreen)
        attack_screen = self.master._frame
        attack_screen.start_attack(self.master.selected_user, wordlist)


class AttackScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.attacking = False
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=20, pady=(16, 12))

        tk.Label(header, text=">>> BRUTE FORCE IN PROGRESS <<<", bg=BG, fg=CRITICAL, font=FONT_HEAD).pack()
        tk.Label(header, text="[ DO NOT CLOSE ]", bg=BG, fg=DANGER, font=FONT_SUB).pack()

        panel = tk.Frame(self, bg=PANEL, highlightthickness=2, highlightbackground=BORDER)
        panel.pack(padx=20, fill="both", expand=True, pady=(0, 16))

        self.status_text = tk.Text(
            panel, bg=BG, fg=SUCCESS, font=FONT_MONO,
            relief="flat", bd=0, height=14, state="normal",
            highlightthickness=0, wrap="word",
        )
        self.status_text.pack(padx=12, pady=12, fill="both", expand=True)
        self.status_text.config(state="disabled")

        btn_row = tk.Frame(panel, bg=PANEL)
        btn_row.pack(fill="x", padx=12, pady=(0, 12))

        self.cancel_btn = styled_btn(btn_row, "CANCEL", self._cancel, color=BORDER)
        self.cancel_btn.pack(side="left")

        self.done_btn = styled_btn(btn_row, "VIEW CONTENT ►", self._view_content, color=SUCCESS)
        self.done_btn.pack(side="right")
        self.done_btn.config(state="disabled")

    def log(self, text):
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, text + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")
        self.update()

    def start_attack(self, username, wordlist):
        self.attacking = True
        self.log(f"[>] TARGET: {username}")
        self.log(f"[>] WORDLIST: {wordlist}")
        self.log(f"[>] STATUS: Initializing...\n")

        thread = threading.Thread(target=self._run_attack, args=(username, wordlist), daemon=True)
        thread.start()

    def _run_attack(self, username, wordlist):
        try:
            result = attack(username, wordlist)

            if result:
                password, content = result
                self.master.cracked_password = password
                self.master.cracked_content = content

                self.log("\n" + "="*50)
                self.log("✓✓✓ PASSWORD CRACKED ✓✓✓")
                self.log("="*50)
                self.log(f"[+] PASSWORD: {password}")
                self.log("[+] DECRYPTION: SUCCESS")
                self.log("[+] STATUS: Ready to view content")
                self.log("="*50)

                self.done_btn.config(state="normal")
            else:
                self.log("\n" + "!"*50)
                self.log("✗ ATTACK FAILED")
                self.log("! Password not found in wordlist")
                self.log("!"*50)

            self.attacking = False
        except Exception as e:
            self.log(f"\n[ERROR] {str(e)}")
            self.attacking = False

    def _cancel(self):
        if self.attacking:
            messagebox.showwarning("⚠ WARNING", "Attack in progress. Please wait.")
            return
        self.master.show_frame(TargetSelectionScreen)

    def _view_content(self):
        if self.master.cracked_content:
            self.master.show_frame(ContentViewScreen)


class ContentViewScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=20, pady=(16, 12))

        tk.Label(header, text=">>> DECRYPTED CONTENT <<<", bg=BG, fg=SUCCESS, font=FONT_HEAD).pack()
        tk.Label(header, text=f"[ USER: {self.master.selected_user} ]", bg=BG, fg=ACCENT, font=FONT_SUB).pack()
        tk.Label(header, text=f"[ PASSWORD: {self.master.cracked_password} ]", bg=BG, fg=DANGER, font=FONT_SUB).pack()

        panel = tk.Frame(self, bg=PANEL, highlightthickness=2, highlightbackground=BORDER)
        panel.pack(padx=20, fill="both", expand=True, pady=(8, 16))

        content_box = tk.Text(
            panel, bg=BG, fg=TEXT, font=FONT_MONO,
            relief="flat", bd=0, state="normal",
            highlightthickness=0, wrap="word",
        )
        content_box.pack(padx=12, pady=12, fill="both", expand=True)
        content_box.insert("1.0", self.master.cracked_content)
        content_box.config(state="disabled")

        btn_row = tk.Frame(panel, bg=PANEL)
        btn_row.pack(fill="x", padx=12, pady=(0, 12))

        styled_btn(btn_row, "◄ BACK", lambda: self.master.show_frame(TargetSelectionScreen), color=BORDER).pack(side="left")
        styled_btn(btn_row, "EXIT", lambda: self.master.quit(), color=CRITICAL).pack(side="right")


if __name__ == "__main__":
    app = AttackerApp()
    app.mainloop()
