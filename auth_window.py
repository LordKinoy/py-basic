import customtkinter as ctk
from tkinter import messagebox
from utils import hash_password, verify_password

class AuthWindow:
    def __init__(self, master, db_manager):
        self.master = master
        self.db = db_manager
        self.launch_dashboard = None
        self.current_email = None

        self.master.title("Login Kasir Minimarket IPWIJA")
        self.master.geometry("500x500")
        self.master.minsize(400, 400)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        self.main_frame = ctk.CTkFrame(master=self.master)
        self.main_frame.pack(padx=40, pady=40, fill="both", expand=True)

        self.main_frame.grid_columnconfigure(0, weight=1)

        self.build_login()

        self.master.bind('<Control-r>', lambda event: self.build_register())
        self.master.bind('<Return>', lambda event: self.login())

    def clear_widgets(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def build_login(self):
        self.clear_widgets()

        ctk.CTkLabel(self.main_frame, text="Login", font=ctk.CTkFont(size=24, weight="bold")).grid(
            row=0, column=0, pady=(10, 20), sticky="n")

        self.username_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Username")
        self.username_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.password_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Password", show="*")
        self.password_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(self.main_frame, text="Login", command=self.login).grid(
            row=3, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(self.main_frame, text="Daftar", command=self.build_register, fg_color="#2196F3").grid(
            row=4, column=0, padx=20, pady=5, sticky="ew")

        ctk.CTkButton(self.main_frame, text="Lupa Password?", command=self.build_forgot_password,
                      fg_color="transparent", text_color="gray", hover=False).grid(
            row=5, column=0, pady=(10, 0), sticky="n")

    def build_register(self):
        self.clear_widgets()

        ctk.CTkLabel(self.main_frame, text="Registrasi", font=ctk.CTkFont(size=24, weight="bold")).grid(
            row=0, column=0, pady=(10, 20), sticky="n")

        self.username_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Username")
        self.username_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.email_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Email")
        self.email_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.password_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Password", show="*")
        self.password_entry.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.confirm_password_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Konfirmasi Password", show="*")
        self.confirm_password_entry.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(self.main_frame, text="Daftar", command=self.register, fg_color="#4CAF50").grid(
            row=5, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(self.main_frame, text="Kembali", command=self.build_login, fg_color="#9E9E9E").grid(
            row=6, column=0, padx=20, sticky="ew")

    def build_forgot_password(self):
        self.clear_widgets()

        ctk.CTkLabel(self.main_frame, text="Reset Password", font=ctk.CTkFont(size=24, weight="bold")).grid(
            row=0, column=0, pady=(10, 20), sticky="n")

        self.email_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Masukkan email Anda")
        self.email_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(self.main_frame, text="Lanjut", command=self.reset_password,
                      fg_color="#FF9800").grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(self.main_frame, text="← Kembali", command=self.build_login, fg_color="#9E9E9E").grid(
            row=3, column=0, padx=20, sticky="ew")

    def build_reset_password_form(self):
        self.clear_widgets()

        ctk.CTkLabel(self.main_frame, text="Setel Ulang Password", font=ctk.CTkFont(size=24, weight="bold")).grid(
            row=0, column=0, pady=(10, 20), sticky="n")

        self.new_password_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Password Baru", show="*")
        self.new_password_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.confirm_new_password_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Konfirmasi Password", show="*")
        self.confirm_new_password_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(self.main_frame, text="Simpan Password Baru", command=self.save_new_password,
                      fg_color="#4CAF50").grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(self.main_frame, text="← Kembali", command=self.build_login, fg_color="#9E9E9E").grid(
            row=4, column=0, padx=20, sticky="ew")

    def login(self):
        username = self.username_entry.get().strip()
        plain_password = self.password_entry.get()

        if not username or not plain_password:
            messagebox.showwarning("Peringatan", "Username dan password wajib diisi!")
            return

        user = self.db.get_user_by_username(username)

        if user:
            stored_hashed_password = user['password']

            if verify_password(plain_password, stored_hashed_password):
                messagebox.showinfo("Sukses", "Login berhasil!")

                self.master.destroy()

                if self.launch_dashboard:
                    self.launch_dashboard({
                        "id": user["id"],
                        "username": user["username"]
                    })

            else:
                messagebox.showerror("Gagal", "Password salah.")
        else:
            messagebox.showerror("Gagal", "Username tidak ditemukan.")

    def register(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_password_entry.get()

        if not all([username, email, password, confirm]):
            messagebox.showwarning("Peringatan", "Semua field wajib diisi!")
            return

        if password != confirm:
            messagebox.showerror("Error", "Password dan konfirmasi tidak cocok!")
            return

        try:
            hashed = hash_password(password)
            self.db.register_user(username, hashed, email)
            messagebox.showinfo("Sukses", "Registrasi berhasil! Silakan login.")
            self.build_login()
        except Exception:
            messagebox.showerror("Gagal", "Username atau email sudah terdaftar.")

    def reset_password(self):
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showwarning("Peringatan", "Masukkan email terlebih dahulu!")
            return

        user = self.db.get_user_by_email(email)
        if user:
            self.current_email = email
            self.build_reset_password_form()
        else:
            messagebox.showerror("Gagal", "Email tidak ditemukan!")

    def save_new_password(self):
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_new_password_entry.get()

        if not new_password or not confirm_password:
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "Password tidak cocok!")
            return

        hashed_new_password = hash_password(new_password)
        self.db.update_user_password(self.current_email, hashed_new_password)
        messagebox.showinfo("Sukses", "Password berhasil diperbarui! Silakan login.")
        self.build_login()