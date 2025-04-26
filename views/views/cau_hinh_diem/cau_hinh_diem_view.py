import customtkinter as ctk
from tkinter import ttk, messagebox
from .insert_cot_diem import ThemCotDiemWindow
class CauHinhDiemFrame(ctk.CTkFrame):
    def __init__(self, parent, bang_diem_instance=None):
        super().__init__(parent)
        self.bang_diem_instance = bang_diem_instance
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="white")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(main_frame, text="CẤU HÌNH ĐIỂM", font=("Arial", 18, "bold")).pack(pady=10)

        search_frame = ctk.CTkFrame(main_frame, fg_color="white")
        search_frame.pack(pady=5, padx=20, fill="x")

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm...", width=300)
        search_entry.pack(side="left", padx=10)

        btn_frame = ctk.CTkFrame(search_frame, fg_color="white")
        btn_frame.pack(side="right")

        ctk.CTkButton(btn_frame, text="Thêm", command=self.them_cot_diem, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Sửa", command=self.sua_cot_diem, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Xóa", command=self.xoa_cot_diem, width=80).pack(side="left", padx=5)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, borderwidth=1, relief="solid", font=("Arial", 14))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        columns = ("ID", "Mã Lớp", "Tên Cột Điểm", "Trọng Số")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", style="Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

    def them_cot_diem(self):
        print("Thêm cột điểm")
        ThemCotDiemWindow(self, self.tree, self.add_column_callback)

    def add_column_callback(self, ten_cot_diem, trong_so):
        if self.bang_diem_instance:
            try:
                trong_so_value = int(trong_so.strip('%'))
            except ValueError:
                trong_so_value = 0
            self.bang_diem_instance.add_new_column(ten_cot_diem, trong_so_value)

    def sua_cot_diem(self):
        print("Sửa cột điểm")

    def xoa_cot_diem(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cột điểm để xóa!")
            return

        values = self.tree.item(selected_item, "values")
        ten_cot_diem = values[2]  # Cột thứ 3 là "Tên Cột Điểm"

        self.tree.delete(selected_item)

        if self.bang_diem_instance:
            self.bang_diem_instance.remove_column(ten_cot_diem)

        messagebox.showinfo("Thành công", f"Đã xóa cột điểm: {ten_cot_diem}")
