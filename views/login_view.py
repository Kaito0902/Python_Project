import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue") 

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username == "admin" and password == "123":
        window.destroy()
        import main  
    elif username == "giaovien" and password == "321":
        window.destroy()
        import views.lop.lop_admin_view as lop_admin_view         
    else:
        messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()  
    screen_height = window.winfo_screenheight() 
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")  

def on_enter(e):
    btn_login.configure(fg_color="#56ec9b")  

def on_leave(e):
    btn_login.configure(fg_color="#338dfe")  

# Tạo cửa sổ 
window = ctk.CTk()
window.title("Đăng Nhập")
window.geometry("600x400")
window.configure(fg_color="white")
window.resizable(False, False)
center_window(window, 600, 400)  

frame = ctk.CTkFrame(window, fg_color="white")
frame.pack(fill="both", expand=True)

# Ảnh login
image = Image.open("resources/images/login.jpg")
image = image.resize((290, 400))  
photo = ImageTk.PhotoImage(image)

img_label = ctk.CTkLabel(frame, image=photo, text="")
img_label.grid(row=0, column=0, padx=0, pady=0)

# Form login
form_frame = ctk.CTkFrame(frame, fg_color="white")
form_frame.grid(row=0, column=1, padx=20, pady=20)

label_title = ctk.CTkLabel(form_frame, text="LOGIN", font=("Verdana", 18, "bold"), text_color="#0071fe")
label_title.grid(row=0, column=0, pady=10)

ctk.CTkLabel(form_frame, text="Tên tài khoản", font=("Arial", 14, "bold"), text_color="#515a51").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_username = ctk.CTkEntry(form_frame, font=("Arial", 12), width=250, corner_radius=10)
entry_username.grid(row=2, column=0, padx=10, pady=5)

ctk.CTkLabel(form_frame, text="Mật khẩu", font=("Arial", 14, "bold"), text_color="#515a51").grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_password = ctk.CTkEntry(form_frame, font=("Arial", 12), width=250, show="*", corner_radius=10)
entry_password.grid(row=4, column=0, padx=10, pady=5)

#Nút đăng nhập
btn_login = ctk.CTkButton(form_frame, text="Đăng nhập", font=("Arial", 14, "bold"), fg_color="#338dfe", text_color="white", corner_radius=10, command=login)
btn_login.grid(row=5, column=0, pady=15)
btn_login.bind("<Enter>", on_enter)
btn_login.bind("<Leave>", on_leave)

#####
window.mainloop()
