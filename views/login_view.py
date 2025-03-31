import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from tkinter import messagebox
from controllers.login_controller import LoginController

class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Đăng nhập")
        self.geometry("400x300")

        self.controller = LoginController()

        # Label và Entry Username
        self.label_username = ctk.CTkLabel(self, text="Tên đăng nhập:")
        self.label_username.pack(pady=10)
        self.entry_username = ctk.CTkEntry(self)
        self.entry_username.pack(pady=5)

        # Label và Entry Password
        self.label_password = ctk.CTkLabel(self, text="Mật khẩu:")
        self.label_password.pack(pady=10)
        self.entry_password = ctk.CTkEntry(self, show="*")
        self.entry_password.pack(pady=5)

        # Nút đăng nhập
        self.button_login = ctk.CTkButton(self, text="Đăng nhập", command=self.dang_nhap)
        self.button_login.pack(pady=20)

    def dang_nhap(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        user = self.controller.dang_nhap(username, password)
        
        if user:
            messagebox.showinfo("Thành công", f"Đăng nhập thành công! Vai trò: {user['vai_tro']}")
            self.destroy()  # Đóng cửa sổ đăng nhập
            # TODO: Mở giao diện chính
        else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu")

if __name__ == "__main__":
    app = LoginView()
    app.mainloop()
