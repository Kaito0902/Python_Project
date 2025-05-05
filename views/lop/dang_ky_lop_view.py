import customtkinter as ctk
from tkinter import messagebox, ttk
from controllers.lop_controller import LopController
from controllers.sinh_vien_controller import SinhVienController
from controllers.khoa_controller import KhoaController

class DangKySinhVienVaoLopView(ctk.CTkToplevel):
    def __init__(self, parent, lop_controller: LopController, sv_controller: SinhVienController, ma_lop):
        super().__init__(parent)
        self.parent = parent
        self.lop_controller = lop_controller
        self.sv_controller = sv_controller
        self.khoa_controller = KhoaController()
        self.ma_lop = ma_lop
        self.title("Đăng ký sinh viên vào lớp")
        self.geometry("600x500")
        self.configure(bg="#ffffff")
        self.center_window(600, 500)

        self.attributes('-topmost', True)

        khoa_frame = ctk.CTkFrame(self, fg_color="white")
        khoa_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(khoa_frame, text="Vui lòng chọn Khoa ", font=("Verdana", 14, "bold"), width=80, anchor="w").pack(side="left", padx=10)

        khoa_list = [khoa["ten_khoa"] for khoa in (self.khoa_controller.select_by_name())]
        khoa_list.insert(0, "Tất cả")
        self.combo_khoa = ctk.CTkComboBox(khoa_frame,  values=khoa_list, state="readonly", command=self.chon_khoa, width=300)
        self.combo_khoa.pack(side="left", padx=10)
        
        search_frame = ctk.CTkFrame(self, fg_color="white")
        search_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(search_frame, text="Nhập Mã hoặc Tên ", font=("Verdana", 14, "bold"), width=85, anchor="w").pack(side="left", padx=10)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm...", width=300)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<Return>", self.search)

        style = ttk.Style()
        style.configure("Treeview", background="#f5f5f5", foreground="black", rowheight=30, fieldbackground="lightgray")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#3084ee", foreground="black")
        style.map("Treeview", background=[("selected", "#4CAF50")], foreground=[("selected", "white")])

        tree_frame = ctk.CTkFrame(self, fg_color="white")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("STT","MSSV", "Họ và Tên"), show="headings", style="Treeview", selectmode="extended")

        self.tree.heading("STT", text="STT")
        self.tree.heading("MSSV", text="MSSV")
        self.tree.heading("Họ và Tên", text="Họ và Tên")

        self.tree.column("STT", width=40, anchor="center")
        self.tree.column("MSSV", width=80, anchor="center")
        self.tree.column("Họ và Tên", width=120)

        self.tree.pack(fill="both", expand=True)
        self.update_treeview()

        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Hủy", font=("Verdana", 14, "bold"), text_color="#7b7d7d", fg_color="white", border_color="#3084ee", border_width=1, hover_color="#d5ebf5", command=self.destroy).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Lưu", font=("Verdana", 14, "bold"), command=self.xac_nhan).pack(side="right", padx=10, pady=5)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 40 
        self.geometry(f"{width}x{height}+{x}+{y}")

    def xac_nhan(self):
        selected_items = self.tree.selection() 

        if not selected_items:
            self.attributes('-topmost', False)
            messagebox.showwarning("Thông báo", "Vui lòng chọn ít nhất một sinh viên!")
            self.attributes('-topmost', True)
            return

        if not self.lop_controller.is_class_available(self.ma_lop):
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Lớp học đã đủ số lượng sinh viên!")
            self.attributes('-topmost', True)
            return

        registered_success = []
        already_registered = []

        for item in selected_items:
            values = self.tree.item(item, "values") 
            mssv = values[1]
            
            if self.lop_controller.is_student_registered(mssv, self.ma_lop):
                already_registered.append(mssv)
                self.attributes('-topmost', False)
                messagebox.showwarning("Thông báo", f"Sinh viên {mssv} đã đăng ký lớp học này!")
                self.attributes('-topmost', True)
                continue 
            
            success = self.lop_controller.register_student_to_class(mssv, self.ma_lop)
            self.lop_controller.them()
            if success:
                registered_success.append(mssv)

        self.attributes('-topmost', False)
        if registered_success:
            messagebox.showinfo("Thành công", "Đăng ký sinh viên vào lớp thành công!")
            self.parent.update_treeview()
            self.destroy()
        else:
            messagebox.showerror("Lỗi", "Không thể đăng ký sinh viên vào lớp!")
            self.attributes('-topmost', True)

    def chon_khoa(self, event=None):
        self.update_treeview()

    def update_treeview(self, data=None):
        self.tree.delete(*self.tree.get_children())

        khoa = self.combo_khoa.get().strip()
        if data is not None:
            students = data
        else:
            if khoa == "" or khoa.lower() == "tất cả" :
                students = self.sv_controller.get_students_data()
            else:
                students = self.sv_controller.get_students_from_khoa(khoa)

        if not students:
            messagebox.showinfo("Thông báo", "Không có dữ liệu sinh viên!")
            return
        
        for index, sv in enumerate(students, start=1):
            ma_sv = sv.get("mssv", "")
            ho_ten = sv.get("ho_ten", "")

            self.tree.insert("", "end", values=(index, ma_sv, ho_ten))

    def search(self, event=None):
        query = self.search_entry.get().lower()
        results = self.sv_controller.search_student_db(query)
        self.update_treeview(results)