import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def open_login():
    window.destroy()
    import login_view  

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def on_logout_enter(e):
    btn_logout["bg"] = "#e8473d"  

def on_logout_leave(e):
    btn_logout["bg"] = "#98c2f7"  

# Tạo cửa sổ 
window = tk.Tk()
window.title("Giảng viên")
window.geometry("1024x600")
window.configure(bg="#ffffff")
center_window(window, 1024, 600)

# Frame menu
menu_frame = tk.Frame(window, bg="#3084ee", width=200, height=600)
menu_frame.pack(side="left", fill="y")

# Logo
image = Image.open("resources/images/avatar.png")
image = image.resize((80, 80))
photo = ImageTk.PhotoImage(image)
img_label = tk.Label(menu_frame, image=photo, bg="#ffffff")
img_label.pack(pady=20)


#Nút tài khoản
btn_account = tk.Button(menu_frame, text="Tài khoản", font=("Arial", 12, "bold"), bg="#98c2f7", fg="white", width=15, height=2,
                        command=None, borderwidth=0, highlightthickness=0)
btn_account.pack(pady=5)

#Nút môn học
btn_subjects = tk.Button(menu_frame, text="Môn học", font=("Arial", 12, "bold"), bg="#98c2f7", fg="white", width=15, height=2,
                        command=None, borderwidth=0, highlightthickness=0)
btn_subjects.pack(pady=5)

#Nút lớp học 
btn_class = tk.Button(menu_frame, text="Lớp học", font=("Arial", 12, "bold"), bg="#98c2f7", fg="white", width=15, height=2,
                        command=None, borderwidth=0, highlightthickness=0)
btn_class.pack(pady=5)

#Nút thống kê
btn_statistic = tk.Button(menu_frame, text="Thống kê", font=("Arial", 12, "bold"), bg="#98c2f7", fg="white", width=15, height=2,
                        command=None, borderwidth=0, highlightthickness=0)
btn_statistic.pack(pady=5)

# Nút đăng xuất 
btn_logout = tk.Button(menu_frame, text="Đăng xuất", font=("Arial", 12, "bold"), bg="#98c2f7", fg="white", width=15, height=2,
                        command=open_login, borderwidth=0, highlightthickness=0)
btn_logout.pack(pady=5)
btn_logout.bind("<Enter>", on_logout_enter)
btn_logout.bind("<Leave>", on_logout_leave)

# Nội dung trang
content_frame = tk.Frame(window, bg="#ffffff", width=824, height=600)
content_frame.pack(side="right", fill="both", expand=True)

header_frame = tk.Frame(content_frame, bg="#646765", height=100)
header_frame.pack(fill="x")

label_title = tk.Label(header_frame, text="Nội dung", font=("Verdana", 18, "bold"), fg="#ffffff", bg="#646765")
label_title.pack(pady=20)

#####
window.mainloop()
