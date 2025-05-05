import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage

from controllers.login_controller import LoginController
from controllers.log_controller import LogController

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class LoginView(ctk.CTk):
    def __init__(self, on_login_success):
        super().__init__()
        self.title("Đăng Nhập")
        self.geometry("600x400")
        self.configure(fg_color="white")
        self.resizable(False, False)
        self.center_window(600, 400)

        self.on_login_success = on_login_success
        self.login_controller = LoginController()
        self.log_controller = LogController()

        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(fill="both", expand=True)

        # Ảnh login
        image = Image.open(r"D:\Downloads\sever nro\icon\Python_Project-master1\resources\images\login.jpg")
        photo = CTkImage(image, size=(290, 400))
        img_label = ctk.CTkLabel(frame, image=photo, text="")
        img_label.grid(row=0, column=0, padx=0, pady=0)

        # Form login
        form_frame = ctk.CTkFrame(frame, fg_color="white")
        form_frame.grid(row=0, column=1, padx=20, pady=20)

        label_title = ctk.CTkLabel(form_frame, text="LOGIN", font=("Verdana", 18, "bold"), text_color="#0071fe")
        label_title.grid(row=0, column=0, pady=10)

        ctk.CTkLabel(form_frame, text="Tên tài khoản", font=("Arial", 14, "bold"), text_color="#515a51").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_username = ctk.CTkEntry(form_frame, font=("Arial", 12), width=250, corner_radius=10)
        self.entry_username.insert(0, "admin")
        self.entry_username.grid(row=2, column=0, padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="Mật khẩu", font=("Arial", 14, "bold"), text_color="#515a51").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.entry_password = ctk.CTkEntry(form_frame, font=("Arial", 12), width=250, show="*", corner_radius=10)
        self.entry_password.insert(0, "admin123")
        self.entry_password.grid(row=4, column=0, padx=10, pady=5)

        self.btn_login = ctk.CTkButton(form_frame, text="Đăng nhập", font=("Arial", 14, "bold"), fg_color="#338dfe",
                                       text_color="white", corner_radius=10, command=self.login)
        self.btn_login.grid(row=5, column=0, pady=15)
        self.btn_login.bind("<Enter>", lambda e: self.btn_login.configure(fg_color="#56ec9b"))
        self.btn_login.bind("<Leave>", lambda e: self.btn_login.configure(fg_color="#338dfe"))

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.login_controller.dang_nhap(username, password):
            ma_nguoi_dung = self.login_controller.lay_ma_nguoi_dung(username, password)
            self.log_controller.ghi_nhat_ky(ma_nguoi_dung["ma_nguoi_dung"], "Đăng nhập hệ thống")
            self.after(100, lambda: [self.destroy(), self.on_login_success()])
        else:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
