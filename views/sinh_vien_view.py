import re
import tkinter as ttk
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry

from controllers.sinh_vien_controller import SinhVienController

class StudentFrame(ctk.CTkFrame):

    sinh_vien_controller = SinhVienController()

    def add_student(self):
        data = self.get_form_data()
        if not all(data.values()):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return

        if not self.validate_student_data(data):
            return

        result = self.sinh_vien_controller.add_student_db(**data)
        if result:
            messagebox.showinfo("Thành công", "Thêm sinh viên thành công.")
            self.update_treeview()
            self.clear_entries()
            self.entry_mssv.configure(state="normal")
        else:
            messagebox.showerror("Cảnh cáo", "Mã sinh viên đã tồn tại.")

    def delete_student(self):
        selected_item = self.tree.selection()
        if selected_item:
            confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sinh viên này?")
            if not confirm:
                return
            for item in selected_item:
                values = self.tree.item(item, 'values')
                self.sinh_vien_controller.delete_student_db(values[0])
            self.update_treeview()
            self.clear_entries()
        else:
            messagebox.showwarning("Cảnh báo", "Vui long chọn sinh viên để xóa.")

    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chọn sinh viên", "Vui lòng chọn sinh viên để cập nhật.")
            return

        data = self.get_form_data()
        if not all(data.values()):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return

        if not self.validate_student_data(data):
            return

        result = self.sinh_vien_controller.update_student_db(**data)
        if result:
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công.")
            self.update_treeview()
            self.clear_entries()
        else:
            messagebox.showerror("Cảnh cáo", "Cập nhật thất bại.")

    def search_student(self):
        query = self.entry_search.get().lower()
        results = self.sinh_vien_controller.search_student_db(query)
        self.update_treeview(results)

    def get_form_data(self):
        return {
            "mssv": self.entry_mssv.get().strip(),
            "ho_ten": self.entry_name.get().strip(),
            "lop": self.entry_class.get().strip(),
            "khoa": self.entry_faculty.get().strip(),
            "ngay_sinh": self.entry_birth.get_date().strftime('%Y-%m-%d'),
            "gioi_tinh": self.combo_gender.get().strip(),
            "que": self.entry_hometown.get().strip(),
            "email": self.entry_email.get().strip()
        }
    
    def validate_student_data(self, data):
        if not data["mssv"].isdigit():
            messagebox.showerror("Cảnh cáo", "Mã sinh viên chỉ được chứa số.")
            return False

        if not re.match(r"^[a-zA-ZÀ-ỹ\s]+$", data["ho_ten"]):
            messagebox.showerror("Cảnh cáo", "Họ và tên không hợp lệ!\n Không được chứa số hoặc ký tự đặc biệt.")
            return False

        if not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
            messagebox.showerror("Cảnh cáo", "Email không hợp lệ.")
            return False

        try:
            birth = datetime.strptime(data["ngay_sinh"], "%Y-%m-%d")
            age = (datetime.today() - birth).days // 365
            if age < 18:
                messagebox.showerror("Cảnh cáo", "Sinh viên phải từ 18 tuổi trở lên.")
                return False
        except:
            messagebox.showerror("Cảnh cáo", "Định dạng ngày sinh không hợp lệ.")
            return False

        return True

    def update_treeview(self, data=None):
        self.tree.delete(*self.tree.get_children())
        students = data if data is not None else self.sinh_vien_controller.get_students_data()
        if not students:
            messagebox.showinfo("Thông báo", "Không có dữ liệu sinh viên!")
            return
        for sv in students:
            self.tree.insert("", "end", values=(
                sv["mssv"], sv["ho_ten"], sv["lop"], sv["khoa"], sv["ngay_sinh"], sv["gioi_tinh"], sv["que"], sv["email"]
            ))

    def on_treeview_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            values = item["values"]
            if len(values) < 8:
                return
            self.entry_mssv.configure(state="normal")
            self.entry_mssv.delete(0, "end")
            self.entry_mssv.insert(0, values[0])
            self.entry_mssv.configure(state="disabled")
            self.entry_name.delete(0, "end")
            self.entry_name.insert(0, values[1])
            self.entry_class.delete(0, "end")
            self.entry_class.insert(0, values[2])
            self.entry_faculty.delete(0, "end")
            self.entry_faculty.insert(0, values[3])
            try:
                self.entry_birth.set_date(values[4])
            except:
                print("Lỗi khi gán ngày sinh!")
            self.combo_gender.set(values[5])
            self.entry_hometown.delete(0, "end")
            self.entry_hometown.insert(0, values[6])
            self.entry_email.delete(0, "end")
            self.entry_email.insert(0, values[7])

    def deselect_student(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.selection_remove(selected_item)
            self.clear_entries()

    def clear_entries(self):
        self.entry_mssv.configure(state="normal")
        self.entry_mssv.delete(0, ctk.END)
        self.entry_name.delete(0, ctk.END)
        self.entry_class.delete(0, ctk.END)
        self.entry_faculty.delete(0, ctk.END)
        self.entry_hometown.delete(0, ctk.END)
        self.entry_email.delete(0, ctk.END)
        self.combo_gender.set("")
        self.entry_birth.set_date(datetime.today().strftime('%Y-%m-%d'))

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#ffffff")

        # Nội dung chính
        content_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        content_frame.pack(side="top", fill="both", expand=True)

        # Header
        header_frame = ctk.CTkFrame(content_frame, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(header_frame, text="Quản Lý Sinh Viên", font=("Verdana", 18, "bold"), text_color="#ffffff")
        label_title.pack(pady=20)

        # Top Form
        top_frame = ctk.CTkFrame(content_frame, fg_color="#ffffff")
        top_frame.pack(side="top", fill="x", padx=5, pady=5)

        # Form nhập
        form_frame = ctk.CTkFrame(top_frame, fg_color="#ffffff")
        form_frame.pack(side="left", fill="both", expand=True, padx=50, pady=5)

        label_mssv = ctk.CTkLabel(form_frame, text="Mã SV", font=("Verdana", 13, "bold"))
        label_name = ctk.CTkLabel(form_frame, text="Họ và tên", font=("Verdana", 13, "bold"))
        label_class = ctk.CTkLabel(form_frame, text="Lớp", font=("Verdana", 13, "bold"))
        label_faculty = ctk.CTkLabel(form_frame, text="Khoa", font=("Verdana", 13, "bold"))
        label_birth = ctk.CTkLabel(form_frame, text="Ngày sinh", font=("Verdana", 13, "bold"))
        label_gender = ctk.CTkLabel(form_frame, text="Giới tính", font=("Verdana", 13, "bold"))
        label_hometown = ctk.CTkLabel(form_frame, text="Quê quán", font=("Verdana", 13, "bold"))
        label_email = ctk.CTkLabel(form_frame, text="Email", font=("Verdana", 13, "bold"))

        label_mssv.grid(row=1, column=1, padx=5, pady=5)
        label_name.grid(row=2, column=1, padx=5, pady=5)
        label_class.grid(row=3, column=1, padx=5, pady=5)
        label_faculty.grid(row=4, column=1, padx=5, pady=5)
        label_birth.grid(row=1, column=3, padx=5, pady=5)
        label_gender.grid(row=2, column=3, padx=5, pady=5)
        label_hometown.grid(row=3, column=3, padx=5, pady=5)
        label_email.grid(row=4, column=3, padx=5, pady=5)

        self.entry_mssv = ctk.CTkEntry(form_frame, width=150, height=30, border_width=1, fg_color="white", text_color="black")
        self.entry_name = ctk.CTkEntry(form_frame, width=150, height=30, border_width=1, fg_color="white", text_color="black")
        self.entry_class = ctk.CTkEntry(form_frame, width=150, height=30, border_width=1, fg_color="white", text_color="black")
        self.entry_faculty = ctk.CTkEntry(form_frame, width=150, height=30, border_width=1, fg_color="white", text_color="black")
        self.entry_birth = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.combo_gender = ttk.Combobox(form_frame, values=["Nam", "Nữ"], state="readonly", width=12)
        self.entry_hometown = ctk.CTkEntry(form_frame, width=150, height=30, border_width=1, fg_color="white", text_color="black")
        self.entry_email = ctk.CTkEntry(form_frame, width=150, height=30, border_width=1, fg_color="white", text_color="black")

        self.entry_mssv.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_name.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.entry_class.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.entry_faculty.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.entry_birth.grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.combo_gender.grid(row=2, column=4, padx=5, pady=5, sticky="w")
        self.entry_hometown.grid(row=3, column=4, padx=5, pady=5, sticky="w")
        self.entry_email.grid(row=4, column=4, padx=5, pady=5, sticky="w")

        # Tìm kiếm
        search_frame = ctk.CTkFrame(top_frame, fg_color="#ffffff")
        search_frame.pack(side="right", fill="both", expand=True, padx=20, pady=5)

        ctk.CTkLabel(search_frame, text="Tìm kiếm", font=("Verdana", 16, "bold")).pack(pady=5)
        self.entry_search = ctk.CTkEntry(search_frame,placeholder_text="Tìm kiếm...", width=200, height=30, border_width=1, fg_color="white", text_color="black")
        self.entry_search.pack(pady=5)
        ctk.CTkButton(search_frame, text="Tìm kiếm", font=("Verdana", 13, "bold"), command=self.search_student, fg_color="#3084ee", text_color="white").pack(pady=5)

        # Nút chức năng
        button_frame = ctk.CTkFrame(content_frame, fg_color="#ffffff")
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Thêm", font=("Verdana", 13, "bold"), command=self.add_student, fg_color="#4CAF50", text_color="white", width=100).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Sửa", font=("Verdana", 13, "bold"), command=self.update_student, fg_color="#fbbc0e", text_color="white", width=100).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Xóa", font=("Verdana", 13, "bold"), command=self.delete_student, fg_color="#F44336", text_color="white", width=100).pack(side="left", padx=5)

        # Treeview
        style = ttk.Style()
        style.configure("Treeview", background="#f5f5f5", foreground="black", rowheight=30, fieldbackground="lightgray")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#3084ee", foreground="black")
        style.map("Treeview", background=[("selected", "#4CAF50")], foreground=[("selected", "white")])

        tree_frame = ctk.CTkFrame(content_frame, fg_color="white")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("MSSV", "Họ Tên", "Lớp", "Khoa", "Ngày Sinh", "Giới Tính", "Quê", "Email"), show="headings", style="Treeview")

        self.tree.heading("MSSV", text="MSSV")
        self.tree.heading("Họ Tên", text="Họ Tên")
        self.tree.heading("Lớp", text="Lớp")
        self.tree.heading("Khoa", text="Khoa")
        self.tree.heading("Ngày Sinh", text="Ngày Sinh")
        self.tree.heading("Giới Tính", text="Giới Tính")
        self.tree.heading("Quê", text="Quê Quán")
        self.tree.heading("Email", text="Email")

        self.tree.column("MSSV", width=60, anchor="center")
        self.tree.column("Họ Tên", width=120)
        self.tree.column("Lớp", width=50, anchor="center")
        self.tree.column("Khoa", width=80, anchor="center")
        self.tree.column("Ngày Sinh", width=80, anchor="center")
        self.tree.column("Giới Tính", width=60, anchor="center")
        self.tree.column("Quê", width=80)
        self.tree.column("Email", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.update_treeview()

        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)
        self.tree.bind("<Double-1>", self.deselect_student)
