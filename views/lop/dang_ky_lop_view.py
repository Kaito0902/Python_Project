import customtkinter as ctk
import tkinter.messagebox as msg
from controllers import lop_controller

class DangKyLop(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__()
        self.title("Đăng ký lớp học cho sinh viên")
        self.geometry("400x300")

        self.label_mssv = ctk.CTkLabel(self, text="Mã sinh viên:")
        self.label_mssv.pack(pady=5)
        self.entry_mssv = ctk.CTkEntry(self)
        self.entry_mssv.pack(pady=5)

        self.label_ma_lop = ctk.CTkLabel(self, text="Mã lớp:")
        self.label_ma_lop.pack(pady=5)
        self.entry_ma_lop = ctk.CTkEntry(self)
        self.entry_ma_lop.pack(pady=5)

        self.btn_xac_nhan = ctk.CTkButton(self, text="Xác nhận", command=self.xac_nhan)
        self.btn_xac_nhan.pack(pady=10)

        self.btn_huy = ctk.CTkButton(self, text="Hủy", command=self.destroy)
        self.btn_huy.pack(pady=5)

    def xac_nhan(self):
        mssv = self.entry_mssv.get().strip()
        ma_lop = self.entry_ma_lop.get().strip()

        if not mssv or not ma_lop:
            msg.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        if not lop_controller.is_student_exist(mssv):
            msg.showerror("Lỗi", "Sinh viên không tồn tại.")
            return

        if not lop_controller.is_class_exist(ma_lop):
            msg.showerror("Lỗi", "Lớp không tồn tại.")
            return

        if lop_controller.is_class_full(ma_lop):
            msg.showerror("Lỗi", "Lớp đã đầy.")
            return

        if lop_controller.is_student_registered(mssv, ma_lop):
            msg.showinfo("Thông báo", "Sinh viên đã đăng ký lớp này.")
            return

        lop_controller.register_class(mssv, ma_lop)
        msg.showinfo("Thành công", "Đăng ký thành công.")
        self.destroy()
