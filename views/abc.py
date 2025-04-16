import tkinter as tk
from tkinter import messagebox

# Hàm kiểm tra đăng nhập
def dang_nhap():
    ten = entry_username.get()
    mat_khau = entry_password.get()

    if ten == "admin" and mat_khau == "123":
        messagebox.showinfo("Đăng nhập thành công", f"Chào mừng {ten}!")
    else:
        messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

# Giao diện chính
root = tk.Tk()
root.title("Đăng nhập")
root.geometry("300x200")
root.resizable(False, False)

# Nhãn và ô nhập cho tên đăng nhập
label_username = tk.Label(root, text="Tên đăng nhập:")
label_username.pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

# Nhãn và ô nhập cho mật khẩu
label_password = tk.Label(root, text="Mật khẩu:")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Nút đăng nhập
login_button = tk.Button(root, text="Đăng nhập", command=dang_nhap)
login_button.pack(pady=10, anchor='e', padx=20)

root.mainloop()
