import customtkinter as ctk
from tkinter import messagebox
from controllers.lop_controller import LopController
from controllers.giang_vien_controller import GiangVienController

class PhanCongGvView(ctk.CTkToplevel):
    def __init__(self, parent, lop_controller: LopController, gv_controller : GiangVienController , ma_lop):
        super().__init__(parent)
        self.parent = parent
        self.lop_controller = lop_controller
        self.gv_controller = gv_controller
        self.ma_lop = ma_lop
        self.title("Phân công Giảng Viên giảng dạy")
        self.geometry("300x100")
        self.configure(bg="#ffffff")
        self.center_window(300, 100)

        self.attributes('-topmost', True)

        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(frame, text="Nhập Mã Giảng Viên ", width=80, anchor="w").pack(side="left", padx=10)
        self.entry_gv = ctk.CTkEntry(frame, width=200)
        self.entry_gv.pack(side="left", padx=10)

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
        ma_gv = self.entry_gv.get().strip()

        if not ma_gv:
            self.attributes('-topmost', False)
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã Giáo Viên!")
            self.attributes('-topmost', True)
            return

        if not self.gv_controller.select_by(ma_gv):
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", f"Không tìm thấy giảng viên có mã : {ma_gv}")
            self.attributes('-topmost', True)
            return
        
        success = self.lop_controller.phan_cong_gv(self.ma_lop, ma_gv)
        self.attributes('-topmost', False)
        if success:
            messagebox.showinfo("Thành công", f"Đã phân công giảng viên {ma_gv} cho lớp {self.ma_lop}.")
            self.parent.thong_tin_lop(self.ma_lop)
            self.parent.update_treeview()
            self.destroy()
 
        else:
            messagebox.showerror("Lỗi", "Không thể phân công giảng viên!")
            self.attributes('-topmost', True)