import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.mon_hoc_controller import MonHocController

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class SuaMonHoc(ctk.CTkToplevel):
    def __init__(self, parent, tree, controller: MonHocController):
        super().__init__(parent)
        self.tree = tree
        self.controller = controller
        self.title("Sửa Môn Học")
        self.geometry("500x300")
        self.configure(bg="#f5f5f5")

        self.attributes('-topmost', True)

        self.create_input_row("Mã Môn Học:", "ma_mh_entry")
        self.create_input_row("Tên Môn Học:", "ten_mh_entry")
        self.create_input_row("Số Tín Chỉ:", "so_tin_chi_entry")
        self.create_input_row("Khoa:", "khoa_entry")

        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Sửa", command=self.sua_mon_hoc).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Hủy bỏ", command=self.destroy).pack(side="right", padx=10, pady=5)

    def create_input_row(self, label_text, entry_attr):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(pady=5, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=label_text, width=80, anchor="w")
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(side="left", padx=10)

        setattr(self, entry_attr, entry)

    def sua_mon_hoc(self):
        ma_mh = self.ma_mh_entry.get()
        ten_mh = self.ten_mh_entry.get()
        so_tin_chi = self.so_tin_chi_entry.get()
        khoa = self.khoa_entry.get()

        if not (ma_mh and ten_mh):
            self.attributes('-topmost', False)
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        selected_item = self.tree.selection()[0]
        self.tree.item(selected_item, "", "end", values=(ma_mh, ten_mh, so_tin_chi, khoa))
        messagebox.showinfo("Thành công", "Đã cập nhật thông tin môn học")
        self.destroy()