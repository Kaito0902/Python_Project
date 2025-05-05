import customtkinter as ctk
from tkinter import messagebox
from controllers.cau_hinh_diem_controller import CauHinhDiemController

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ThemCotDiemWindow(ctk.CTkToplevel):
    def __init__(self, parent, ma_lop, bd):
        super().__init__(parent)
        self.title("Thêm Cột Điểm")
        self.geometry("500x300")
        self.configure(bg="#f5f5f5")
        self.parent = parent
        self.controller = CauHinhDiemController()
        self.ma_lop = ma_lop
        self.bd = bd

        self.attributes('-topmost', True)

        self.create_input_row("Tên Cột Điểm:", "ten_cot_diem_entry")
        self.create_trong_so_row("Trọng số:", "trong_so_option")

        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Lưu", command=self.luu_cot_diem).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Hủy bỏ", command=self.destroy).pack(side="right", padx=10, pady=5)

    def create_input_row(self, label_text, entry_attr):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(pady=5, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=label_text, width=80, anchor="w")
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(side="left", padx=10)

        setattr(self, entry_attr, entry)

    def create_trong_so_row(self, label_text, option_attr):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(pady=5, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=label_text, width=80, anchor="w")
        label.pack(side="left", padx=10)

        options = [f"{i}%" for i in range(10, 60, 10)]
        option_menu = ctk.CTkOptionMenu(frame, values=options)
        option_menu.set("10%")
        option_menu.pack(side="left", padx=10)

        setattr(self, option_attr, option_menu)

    def luu_cot_diem(self):
        ten_cot_diem = self.ten_cot_diem_entry.get().strip()
        trong_so_str = self.trong_so_option.get().strip()

        if not (ten_cot_diem and trong_so_str):
            self.attributes('-topmost', False)
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            self.attributes('-topmost', True)
            return

        if self.controller.is_ten_cot_diem_exists(self.ma_lop, ten_cot_diem):
            self.attributes('-topmost', False)
            messagebox.showwarning("Cảnh báo", "Tên cột điểm không được trùng!")
            self.attributes('-topmost', True)
            return

        try:
            trong_so = float(trong_so_str.replace("%", ""))
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Trọng số phải là số!")
            return

        tong_trong_so_hien_tai = self.controller.get_total_trong_so(self.ma_lop)
        tong_trong_so_moi = tong_trong_so_hien_tai + trong_so

        if tong_trong_so_moi > 50:
            self.attributes('-topmost', False)
            messagebox.showwarning("Cảnh báo", "Tổng trọng số không được vượt quá 50%!")
            self.destroy()
            return

        self.controller.insert(self.ma_lop, ten_cot_diem, trong_so)
        self.parent.load_data()
        self.bd.refresh_columns_and_data()
        messagebox.showinfo("Thành công", "Đã lưu cột điểm.")
        self.destroy()
