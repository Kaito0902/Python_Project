import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class SuaGiangVien(ctk.CTkToplevel):
    def __init__(self, parent, tree):
        super().__init__(parent)
        self.tree = tree
        self.title = "Sửa Giảng Viên"
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

        ctk.CTkButton(button_frame, text="Sửa", command=self.sua_giang_vien).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Hủy bỏ", command=self.destroy).pack(side="right", padx=10, pady=5)

    def create_input_row(self, label_text, entry_attr):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(pady=5, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=label_text, width=80, anchor="w")
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(side="left", padx=10)

        setattr(self, entry_attr, entry)

    def sua_giang_vien(self):
        ma_gv = self.ma_gv_entry.get()
        ten_gv = self.ten_gv_entry.get()
        khoa = self.khoa_entry.get()
        email = self.email_entry.get()
        sdt = self.sdt_entry.get()

        if not ma_gv or not ten_gv or not email or not sdt:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return
        selected_item = self.tree.selection()[0]
        self.tree.item(selected_item, values=(ma_gv, ten_gv, email, sdt))
        messagebox.showinfo("Thành công", "Đã cập nhật thông tin giảng viên")

        self.destroy()




