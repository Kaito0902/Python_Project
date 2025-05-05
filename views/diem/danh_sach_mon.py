import tkinter as ttk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from controllers.diem_controller import DiemController
from views.diem.diem_cuoi_ky import NhapDiemChiTietFrame
from views.diem.lop_cuoi_ky import LopMonHocFrame

class NhapDiemFrame(ctk.CTkFrame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#ffffff")
        self.app = app
        self.controller = DiemController()

        content_frame = ctk.CTkFrame(self, fg_color="#ffffff", width=824, height=600)
        content_frame.pack(side="top", fill="both", expand=True)

        # Tiêu đề
        header_frame = ctk.CTkFrame(content_frame, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(
            header_frame,
            text="Nhập điểm cuối kỳ",
            font=("Verdana", 18, "bold"),
            text_color="#ffffff"
        )
        label_title.pack(pady=30, padx=20, anchor="c")

        # Nút "Chọn nhập điểm" ngay dưới tiêu đề
        button_frame = ctk.CTkFrame(content_frame, fg_color="white")
        button_frame.pack(fill="x", padx=20)

        self.btn_chon_nhap_diem = ctk.CTkButton(
            button_frame,
            text="Xem lớp của môn học",
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

        self.tree = ttk.Treeview(tree_frame, columns=("ma_mon", "ten_mon", "so_luong"), show="headings", style="Treeview")
        self.tree.heading("ma_mon", text="Mã môn")
        self.tree.heading("ten_mon", text="Tên môn")
        self.tree.heading("so_luong", text="Số lượng SV")

        self.tree.column("ma_mon", width=100, anchor="center")
        self.tree.column("ten_mon", width=200, anchor="center")
        self.tree.column("so_luong", width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.load_data()

    def load_data(self):
        # Lấy danh sách môn học từ controller
        danh_sach_mon = self.controller.get_danh_sach_mon_va_so_luong_sv()

        # Xóa dữ liệu cũ
        self.clear_treeview()

        # Nạp dữ liệu mới
        if danh_sach_mon:
            for mon in danh_sach_mon:
                self.tree.insert('', 'end', values=(
                    mon['ma_mon'],
                    mon['ten_mon'],
                    mon['so_luong_sinh_vien']
                ))
        else:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị.")

    def clear_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def on_chon_nhap_diem(self):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            ma_mon = values[0]
            ten_mon = values[1]
            so_luong = values[2]

            # Ẩn frame hiện tại
            self.pack_forget()

            # Gọi frame nhập điểm chi tiết, truyền đủ 3 tham số
            lop_mon_hoc_frame = LopMonHocFrame(
                master=self.master,
                app=self.app,
                ma_mon=ma_mon,
                ten_mon=ten_mon,
                so_luong=so_luong
            )
            lop_mon_hoc_frame.pack(fill="both", expand=True)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một môn học để nhập điểm!")

