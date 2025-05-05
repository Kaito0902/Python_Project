import tkinter as ttk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from views.diem.diem_cuoi_ky import NhapDiemChiTietFrame
from controllers.diem_controller import DiemController

class LopMonHocFrame(ctk.CTkFrame):
    def __init__(self, master=None, app=None, ma_mon=None, ten_mon=None, so_luong=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#ffffff")
        self.app = app
        self.ma_mon = ma_mon
        self.ten_mon = ten_mon
        self.so_luong = so_luong
        self.controller = DiemController()

        content_frame = ctk.CTkFrame(self, fg_color="#ffffff", width=824, height=600)
        content_frame.pack(side="top", fill="both", expand=True)

        # Tiêu đề
        header_frame = ctk.CTkFrame(content_frame, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(
            header_frame,
            text="Danh sách lớp môn học",
            font=("Verdana", 18, "bold"),
            text_color="#ffffff"
        )
        label_title.pack(pady=30, padx=20, anchor="w")  # Căn trái

        # Nút "Chọn nhập điểm" dưới tiêu đề
        button_frame = ctk.CTkFrame(content_frame, fg_color="white")
        button_frame.pack(fill="x", padx=20)

        self.btn_chon_nhap_diem = ctk.CTkButton(
            button_frame,
            text="Chọn nhập điểm",
            fg_color="#904fd2",
            text_color="white",
            font=("Verdana", 13, "bold"),
            command=self.on_chon_nhap_diem
        )
        self.btn_chon_nhap_diem.pack(side="right", pady=10)

        # Bảng dữ liệu
        tree_frame = ctk.CTkFrame(content_frame, fg_color="white")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

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

        self.tree = ttk.Treeview(tree_frame, columns=("ma_lop", "ma_mon", "so_luong"), show="headings", style="Treeview")
        self.tree.heading("ma_lop", text="Mã lớp")
        self.tree.heading("ma_mon", text="Mã môn")
        self.tree.heading("so_luong", text="Số lượng SV")

        self.tree.column("ma_lop", width=120, anchor="center")
        self.tree.column("ma_mon", width=120, anchor="center")
        self.tree.column("so_luong", width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.load_data()

    def load_data(self):
        data = self.controller.get_danh_sach_lop_va_so_luong_sv(self.ma_mon)
        if data:
            for row in self.tree.get_children():
                self.tree.delete(row)
            for row in data:
                self.tree.insert('', 'end', values=row)
        else:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị.")

    def on_chon_nhap_diem(self):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            ma_lop = values[0]
            ma_mon = values[1]
            so_luong = values[2]

            # Ẩn frame hiện tại
            self.pack_forget()

            nhap_diem_chi_tiet_frame = NhapDiemChiTietFrame(
                master=self.master,
                app=self.app,
                ma_mon=ma_mon,
                ten_mon=self.ten_mon,
                so_luong=so_luong,
                ma_lop=ma_lop
            )
            nhap_diem_chi_tiet_frame.pack(fill="both", expand=True)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một môn học để nhập điểm!")
