import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.mon_hoc_controller import MonHocController

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ThemMonHocWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller: MonHocController):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.title("Thêm Môn Học")
        self.geometry("500x300")
        self.configure(bg="#f5f5f5")

        self.attributes('-topmost', True)

        self.create_input_row("Mã Môn Học:", "ma_mh_entry")
        self.create_input_row("Tên Môn Học:", "ten_mh_entry")
        self.create_input_row("Số Tín Chỉ:", "so_tin_chi_entry")
        self.create_input_row("Khoa:", "khoa_entry")

        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Lưu", command=self.luu_mon_hoc).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Hủy bỏ", command=self.destroy).pack(side="right", padx=10, pady=5)

    def create_input_row(self, label_text, entry_attr):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(pady=5, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=label_text, width=80, anchor="w")
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(side="left", padx=10)

        setattr(self, entry_attr, entry)

    def luu_mon_hoc(self):
        ma_mh = self.ma_mh_entry.get().strip()
        ten_mh = self.ten_mh_entry.get().strip()
        so_tin_chi = self.so_tin_chi_entry.get().strip()
        khoa = self.khoa_entry.get().strip()

        if not ma_mh or not ten_mh or not so_tin_chi or not khoa:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            self.attributes('-topmost', True)
            return

        if not so_tin_chi.isdigit() or int(so_tin_chi) <= 0:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Số tín chỉ phải là số nguyên dương!")
            self.attributes('-topmost', True)
            return

        try:
            success = self.controller.insert(ma_mh, ten_mh, int(so_tin_chi), khoa)
            if success:
                self.attributes('-topmost', False)
                messagebox.showinfo("Thành công", "Đã lưu thông tin môn học!")
                self.parent.load_data()
                self.destroy()
            else:
                raise ValueError("Không thể thêm môn học có thể bị trùng Mã Môn Học!")
        except Exception as e:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", f"Lỗi khi thêm môn học: {str(e)}")
            self.attributes('-topmost', True)
