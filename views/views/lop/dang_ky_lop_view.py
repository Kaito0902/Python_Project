import customtkinter as ctk
from tkinter import messagebox
from controllers.lop_controller import LopController
from controllers.sinh_vien_controller import SinhVienController

class DangKySinhVienVaoLopView(ctk.CTkToplevel):
    def __init__(self, parent, lop_controller: LopController, sv_controller: SinhVienController, ma_lop):
        super().__init__(parent)
        self.parent = parent
        self.lop_controller = lop_controller
        self.sv_controller = sv_controller
        self.ma_lop = ma_lop
        self.title("Đăng ký sinh viên vào lớp")
        self.geometry("300x100")
        self.configure(bg="#ffffff")
        self.center_window(300, 100)

        self.attributes('-topmost', True)

        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(frame, text="Nhập Mã Sinh Viên ", width=80, anchor="w").pack(side="left", padx=10)
        self.entry_mssv = ctk.CTkEntry(frame, width=200)
        self.entry_mssv.pack(side="left", padx=10)

        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Hủy", font=("Verdana", 14, "bold"), text_color="#7b7d7d", fg_color="white", border_color="#3084ee", border_width=1, hover_color="#d5ebf5", command=self.destroy).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Lưu", font=("Verdana", 14, "bold"), command=self.xac_nhan).pack(side="right", padx=10, pady=5)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 40 
        self.geometry(f"{width}x{height}+{x}+{y}")

    def xac_nhan(self):
        mssv = self.entry_mssv.get().strip()

        if not mssv:
            self.attributes('-topmost', False)
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã Sinh Viên!")
            self.attributes('-topmost', True)
            return

        sv = self.sv_controller.model.get_by_mssv(mssv)
        if not sv:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", f"Không tìm thấy sinh viên có mã : {mssv}")
            self.attributes('-topmost', True)
            return

        if not self.lop_controller.is_class_available(self.ma_lop):
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Lớp học đã đủ số lượng sinh viên!")
            self.attributes('-topmost', True)
            return

        if self.lop_controller.is_student_registered(mssv, self.ma_lop):
            self.attributes('-topmost', False)
            messagebox.showwarning("Thông báo", "Sinh viên đã đăng ký lớp học này!")
            self.attributes('-topmost', True)
            return

        success = self.lop_controller.register_student_to_class(mssv, self.ma_lop)
        self.attributes('-topmost', False)
        if success:
            messagebox.showinfo("Thành công", "Đăng ký sinh viên vào lớp thành công!")
            self.parent.update_treeview()
            self.destroy()
        else:
            messagebox.showerror("Lỗi", "Không thể đăng ký sinh viên vào lớp!")
            self.attributes('-topmost', True)