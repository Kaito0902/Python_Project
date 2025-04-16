import customtkinter as ctk
from tkinter import messagebox
from controllers.giang_vien_controller import GiangVienController

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ThemGiangVienWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller: GiangVienController):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.title("Thêm Giảng Viên")
        self.geometry("500x300")
        self.configure(bg="#f5f5f5")

        self.attributes('-topmost', True)

        self.create_input_row("Mã GV:", "ma_gv_entry")
        self.create_input_row("Tên GV:", "ten_gv_entry")
        self.create_input_row("Khoa:", "khoa_entry")
        self.create_input_row("Email:", "email_entry")
        self.create_input_row("SĐT:", "sdt_entry")

        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Lưu", command=self.luu_giang_vien).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Hủy bỏ", command=self.destroy).pack(side="right", padx=10, pady=5)

    def create_input_row(self, label_text, entry_attr):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(pady=5, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=label_text, width=80, anchor="w")
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(side="left", padx=10)

        setattr(self, entry_attr, entry)

    def luu_giang_vien(self):
        ma_gv = self.ma_gv_entry.get().strip()
        ten_gv = self.ten_gv_entry.get().strip()
        khoa = self.khoa_entry.get().strip()
        email = self.email_entry.get().strip()
        sdt = self.sdt_entry.get().strip()

        if not (ma_gv and ten_gv):
            self.attributes('-topmost', False)
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            success = self.controller.insert(ma_gv, ten_gv, khoa, email, sdt)
            if success:
                self.attributes('-topmost', False)
                messagebox.showinfo("Thành công", "Đã lưu thông tin giảng viên!")
                self.parent.load_data()
                self.destroy()
            else:
                raise ValueError("Không thể thêm giảng viên, có thể bị trùng Mã GV!")
        except Exception as e:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", f"Lỗi khi thêm giảng viên: {str(e)}")

