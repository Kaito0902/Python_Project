import tkinter as ttk
import customtkinter as ctk
from datetime import datetime 
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry

from views.lop.dang_ky_lop_view import DangKyLop
from controllers.lop_controller import LopController
from controllers.sinh_vien_controller import SinhVienController
    
class LopView(ctk.CTk):

    lop_controller = LopController()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 40
        self.geometry(f"{width}x{height}+{x}+{y}")

    def open_login(self):
        self.destroy()
        # import login_view

    def open_student(self):
        self.destroy()
        from views.sinh_vien_view import StudentView
        app = StudentView()   
        app.mainloop()
    
    def open_register_window(self):
        DangKyLop(self, update_callback=self.update_treeview)

    def on_logout_enter(self, e):
        self.btn_logout.configure(fg_color="#e8473d")  

    def on_logout_leave(self, e):
        self.btn_logout.configure(fg_color="#98c2f7") 

    def open_menu(self):
        if self.class_menu.winfo_ismapped():
            self.class_menu.grid_remove()
        else:
            self.class_menu.grid()

    # Hàm xử lý thêm xóa sửa tìm
    def delete_student(self):
        selected_item = self.tree.selection()
        if selected_item:
            for item in selected_item:
                values = self.tree.item(item, 'values')
                self.delete_student_db(values[0])
            self.update_treeview()
        else:
            messagebox.showwarning("Cảnh báo", "Chọn sinh viên để xóa")

    def search_student(self):
        query = self.entry_search.get().lower()
        results = self.search_student_db(query)
        self.update_treeview(results)

    # Hàm xử lý TreeView
    def get_form_data(self):
        return {
            "ma_lop": self.entry_search.get().strip(),

        }

    def update_treeview(self, data=None):
        self.tree.delete(*self.tree.get_children()) 
        classes = data if data is not None else self.lop_controller.get_all_class()

        print("📌 Dữ liệu lấy từ DB:", classes)  

        if not classes:
            messagebox.showinfo("Thông báo", "Không có dữ liệu lớp học!")
            return

        for lop in classes:
            self.tree.insert("", "end", values=(
                lop.ma_lop, lop.ma_mon, lop.so_luong, lop.hoc_ky, lop.nam, lop.ma_gv
            ))

    def on_treeview_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])  
            values = item["values"]

            # Kiểm tra nếu có đủ dữ liệu
            if len(values) < 8:
                return

            self.entry_search.delete(0, "end")

            print("📌 Dữ liệu đã được gán vào Entry!")

    def deselect_student(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.selection_remove(selected_item)  
            self.clear_entries()  

    def clear_entries(self):
        self.entry_search.delete(0, ctk.END)

    def __init__(self):
        super().__init__()

        # Tạo cửa sổ
        self.title("Quản lý lớp học")
        self.geometry("1024x600")
        self.configure(fg_color="#ffffff") 
        self.center_window(1024, 600)

        # Frame menu
        menu_frame = ctk.CTkFrame(self, fg_color="#3084ee", width=200, height=600)
        menu_frame.pack(side="left", fill="y")

        # Logo
        image = Image.open(r"C:\Users\ACER\PycharmProjects\Python_project\resources\images\avatar.png").resize((80, 80))
        photo = ctk.CTkImage(light_image=image, size=(80, 80))
        img_label = ctk.CTkLabel(menu_frame, image=photo, text="", fg_color="#ffffff")
        img_label.grid(row=0, column=0, pady=5)


        # Nút tài khoản
        btn_account = ctk.CTkButton(menu_frame, text="Tài khoản", font=("Arial", 17, "bold"),fg_color="#98c2f7", text_color="white", width=150, height=40)
        btn_account.grid(row=2, column=0, pady=5)

        # Nút môn học
        btn_subjects = ctk.CTkButton(menu_frame, text="Môn học", font=("Arial", 17, "bold"),fg_color="#98c2f7", text_color="white", width=150, height=40)
        btn_subjects.grid(row=3, column=0, pady=5)

        # Nút lớp học
        btn_class = ctk.CTkButton(menu_frame, text="Lớp học", font=("Arial", 17, "bold"),fg_color="#98c2f7", text_color="white", width=150, height=40, command=self.open_menu)
        btn_class.grid(row=4, column=0, pady=5)

        # Frame lựa chọn trong lớp học
        self.class_menu = ctk.CTkFrame(menu_frame, fg_color="#83b5f5", width=150)
        self.class_menu.grid(row=5, column=0, pady=0)
        self.class_menu.grid_remove()  # Ẩn ban đầu

        # Các lựa chọn trong lớp học
        btn_class_list = ctk.CTkButton(self.class_menu, text="Danh sách lớp học", font=("Arial", 14, "bold"),fg_color="#98c2f7", text_color="white", width=130, height=35)
        btn_class_list.pack(fill='x', pady=2)

        btn_student = ctk.CTkButton(self.class_menu, text="Sinh viên lớp học", font=("Arial", 14, "bold"),fg_color="#98c2f7", text_color="white", width=130, height=35, command=self.open_student)
        btn_student.pack(fill='x', pady=2)

        # Nút thống kê
        btn_statistic = ctk.CTkButton(menu_frame, text="Thống kê", font=("Arial", 17, "bold"),fg_color="#98c2f7", text_color="white", width=150, height=40)
        btn_statistic.grid(row=6, column=0, pady=5)

        # Nút đăng xuất
        self.btn_logout = ctk.CTkButton(menu_frame, text="Đăng xuất", font=("Arial", 17, "bold"),fg_color="#98c2f7", text_color="white", width=150, height=40, command=self.open_login)
        self.btn_logout.grid(row=7, column=0, pady=5)
        self.btn_logout.bind("<Enter>", self.on_logout_enter)
        self.btn_logout.bind("<Leave>", self.on_logout_leave)

        # Nội dung trang
        content_frame = ctk.CTkFrame(self, fg_color="#ffffff", width=824, height=600)
        content_frame.pack(side="right", fill="both", expand=True)

        # Header Frame
        header_frame = ctk.CTkFrame(content_frame, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(header_frame, text="Thông Tin Lớp Học", font=("Verdana", 18, "bold"), text_color="#ffffff")
        label_title.pack(pady=20)

        # Form Frame
        form_frame = ctk.CTkFrame(content_frame, fg_color="#ffffff")
        form_frame.pack( pady=35)

        self.btn_register = ctk.CTkButton(form_frame, text="Đăng ký lớp học", font=("Verdana", 13, "bold"), command=self.open_register_window, fg_color="#af4cab", text_color="white", width=100, height=40).grid(row=0, column=0, padx=5, pady=5)
        
        self.entry_search = ctk.CTkEntry(form_frame, width=300, height=30, border_width=1, fg_color="white", text_color="black")
        self.entry_search.grid(row=0, column=1, padx=5, pady=5)

        self.btn_add_class = ctk.CTkButton(form_frame, text="Thêm", font=("Verdana", 13, "bold"), command=None, fg_color="#4CAF50", text_color="white", width=100, height=40).grid(row=0, column=2, padx=5, pady=5)
        self.btn_update_class = ctk.CTkButton(form_frame, text="Cập nhập", font=("Verdana", 13, "bold"), command=None, fg_color="#fbbc0e", text_color="white", width=100, height=40).grid(row=0, column=3, padx=5, pady=5)
        self.btn_delete_class = ctk.CTkButton(form_frame, text="Xóa", font=("Verdana", 13, "bold"), command=None, fg_color="#F44336", text_color="white", width=100, height=40).grid(row=0, column=4, padx=5, pady=5)

        # Style TreeView
        style = ttk.Style()
        style.configure("Treeview",
                        background="#f5f5f5",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="lightgray")

        style.configure("Treeview.Heading",
                        font=("Arial", 12, "bold"),
                        background="#3084ee",
                        foreground="black")

        style.map("Treeview",
                background=[("selected", "#4CAF50")],
                foreground=[("selected", "white")])

        # Frame chứa Treeview
        tree_frame = ctk.CTkFrame(content_frame, fg_color="white")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("Mã Lớp", "Mã Môn", "Số Lượng", "Học Kỳ", "Năm", "Mã GV"), show="headings", style="Treeview")

        # Thiết lập tiêu đề cột
        self.tree.heading("Mã Lớp", text="Mã Lớp")
        self.tree.heading("Mã Môn", text="Mã Môn")
        self.tree.heading("Số Lượng", text="Số Lượng")
        self.tree.heading("Học Kỳ", text="Học Kỳ")
        self.tree.heading("Năm", text="Năm")
        self.tree.heading("Mã GV", text="Mã GV")

        self.tree.column("Mã Lớp", width=80, anchor="center")
        self.tree.column("Mã Môn", width=80, anchor="center")
        self.tree.column("Số Lượng", width=40, anchor="center")
        self.tree.column("Học Kỳ", width=40, anchor="center")
        self.tree.column("Năm", width=40, anchor="center")
        self.tree.column("Mã GV", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)  

        self.update_treeview()
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)
        self.tree.bind("<Double-1>", self.deselect_student)

if __name__ == "__main__":
    app = LopView()
    app.mainloop()

