import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username == "admin" and password == "123":
            window.destroy()
            import main_view 
    elif username == "giaovien" and password == "321":
        window.destroy()
        import giang_vien_view         
    else:
        messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()  
    screen_height = window.winfo_screenheight() 
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")  

def on_enter(e):
    btn_login["bg"] = "#56ec9b" 

def on_leave(e):
    btn_login["bg"] = "#338dfe"  

# Tạo cửa sổ 
window = tk.Tk()
window.title("Đăng Nhập")
window.geometry("600x400")
window.configure(bg="#ffffff")
window.resizable(False, False)
center_window(window, 600, 400)  

frame = tk.Frame(window, bg="#ffffff")
frame.pack(fill="both", expand=True)

# Ảnh login
image = Image.open("resources/images/login.jpg")
image = image.resize((290, 400))  
photo = ImageTk.PhotoImage(image)

img_label = tk.Label(frame, image=photo)
img_label.grid(row=0, column=0, padx=0, pady=0)

# Form login
form_frame = tk.Frame(frame, bg="#ffffff")
form_frame.grid(row=0, column=1, padx=0, pady=0)

label_title = tk.Label(form_frame, text="LOGIN", font=("Verdana", 18, "bold"), fg="#0071fe", bg="#ffffff")
label_title.grid(row=0, column=0, pady=1)

tk.Label(form_frame, text="Tên tài khoản", font=("Arial", 14, "bold"), fg="#515a51", bg="#ffffff").grid(row=2, column=0, sticky="w",padx=10, pady=10)
entry_username = tk.Entry(form_frame, font=("Arial", 12), bg="#f2f2f3", width=30)
entry_username.grid(row=3, column=0, padx=10, pady=5)

tk.Label(form_frame, text="Mật khẩu", font=("Arial", 14, "bold"), fg="#515a51", bg="#ffffff").grid(row=4, column=0, sticky="w",padx=10, pady=10)
entry_password = tk.Entry(form_frame, font=("Arial", 12), bg="#f2f2f3", width=30, show="*") 
entry_password.grid(row=5, column=0, padx=10, pady=5)

#Nút đăng nhập
btn_login = tk.Button(form_frame, text="Đăng nhập", font=("Arial", 12, "bold"), bg="#338dfe", fg="white", padx=10, pady=5, command=login, borderwidth=0, highlightthickness=0)
btn_login.grid(row=6, column=0, pady=10)
btn_login.bind("<Enter>", on_enter)
btn_login.bind("<Leave>", on_leave)

######
window.mainloop()


