import customtkinter as ctk
from views.cau_hinh_diem.bang_diem_lop import BangDiemLop
from views.cau_hinh_diem.cau_hinh_diem_view import CauHinhDiemFrame
from tkinter import ttk

class QuanLyLopTabbedPane(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="QUẢN LÝ LỚP HỌC", font=("Arial", 20, "bold"), fg_color="white").pack(pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.bang_diem_tab = BangDiemLop(notebook)
        notebook.add(self.bang_diem_tab, text="Bảng Điểm Lớp")

        self.cau_hinh_tab = CauHinhDiemFrame(notebook, self.bang_diem_tab)
        notebook.add(self.cau_hinh_tab, text="Cấu Hình Điểm")

