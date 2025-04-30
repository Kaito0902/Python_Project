import customtkinter as ctk
from tkinter import ttk, messagebox
from .insert_cot_diem import ThemCotDiemWindow
from .update_cot_diem import SuaCotDiem


class CauHinhDiemFrame(ctk.CTkFrame):
    def __init__(self, parent, bang_diem_instance=None):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.bang_diem_instance = bang_diem_instance
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        header_frame = ctk.CTkFrame(self, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(header_frame, text="Cấu Hình Điểm", font=("Verdana", 18, "bold"),
                                   text_color="#ffffff")
        label_title.pack(pady=20)

        search_frame = ctk.CTkFrame(self, fg_color="white")
        search_frame.pack(pady=5, padx=20, fill="x")

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm...", width=300)
        search_entry.pack(side="left", padx=10)

        btn_frame = ctk.CTkFrame(search_frame, fg_color="white")
        btn_frame.pack(side="right")

        ctk.CTkButton(btn_frame, fg_color="#4CAF50", text="Thêm", font=("Verdana", 13, "bold"), text_color="white", command=self.them_cot_diem, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, fg_color="#fbbc0e", text="Sửa", font=("Verdana", 13, "bold"), text_color="white", command=self.sua_cot_diem, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, fg_color="#F44336", text="Xóa", font=("Verdana", 13, "bold"), text_color="white", command=self.xoa_cot_diem, width=80).pack(side="left", padx=5)

        style = ttk.Style()
        style.configure("Treeview", background="#f5f5f5", foreground="black", rowheight=30, fieldbackground="lightgray")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#3084ee", foreground="black")
        style.map("Treeview", background=[("selected", "#4CAF50")], foreground=[("selected", "white")])

        columns = ("ID", "Mã Lớp", "Tên Cột Điểm", "Trọng Số")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", style="Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_row_click)

    def them_cot_diem(self):
        ThemCotDiemWindow(self, self.tree, self.add_column_callback)

    def add_column_callback(self, ten_cot_diem, trong_so):
        if self.bang_diem_instance:
            try:
                trong_so_value = int(trong_so.strip('%'))
            except ValueError:
                trong_so_value = 0
            self.bang_diem_instance.add_new_column(ten_cot_diem, trong_so_value)

    def sua_cot_diem(self):
        if not hasattr(self, "selected_chd"):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột điểm cần sửa trước!")
            return
        SuaCotDiem(self, self.tree, self.add_column_callback)

    def on_row_click(self, event):
        try:
            item = self.tree.selection()[0]
            values = self.tree.item(item, "values")
            self.selected_chd = {
                "ten_cot_diem": values[2],
                "trong_so": values[3]
            }
        except Exception:
            pass

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
