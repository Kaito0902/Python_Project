import tkinter as ttk
from tkinter import filedialog
import customtkinter as ctk
from tkinter import messagebox, ttk
import pandas as pd

from views.lop.phan_cong_gv_view import PhanCongGvView
from views.lop.dang_ky_lop_view import DangKySinhVienVaoLopView
from controllers.lop_controller import LopController
from controllers.sinh_vien_controller import SinhVienController
from controllers.giang_vien_controller import GiangVienController


class ChiTietLopAdminFrame(ctk.CTkFrame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#ffffff")
        self.app = app
        self.lop_controller = LopController()
        self.sv_controller = SinhVienController()
        self.gv_controller = GiangVienController()

        content_frame = ctk.CTkFrame(self, fg_color="#ffffff", width=824, height=600)
        content_frame.pack(side="top", fill="both", expand=True)

        header_frame = ctk.CTkFrame(content_frame, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(header_frame, text="Thông tin Lớp Học", font=("Verdana", 18, "bold"), text_color="#ffffff")
        label_title.pack(pady=20)

        btn_frame = ctk.CTkFrame(content_frame, fg_color="white")
        btn_frame.pack(padx=20, pady=5, fill="x")
       
        ctk.CTkButton(btn_frame, fg_color="#904fd2", hover_color="#616262", text="◀ Quay lại",  text_color="white", font=("Verdana", 13, "bold"), command=self.back_to_lop_admin, width=80).pack(side="left", padx=5, pady=20)
        ctk.CTkButton(btn_frame, fg_color="#f89924", hover_color="#616262", text="Xuất danh sách ☰",  text_color="white", font=("Verdana", 13, "bold"), command=self.xuat_danh_sach, width=100).pack(side="right", padx=5, pady=20)
        ctk.CTkButton(btn_frame, fg_color="#539cbd", hover_color="#616262", text="Phân công GV",  text_color="white", font=("Verdana", 13, "bold"), command=self.phan_cong_giang_vien, width=100).pack(side="right", padx=5, pady=20)
        ctk.CTkButton(btn_frame, fg_color="#f6695e", hover_color="#616262", text="Hủy đăng ký", text_color="white", font=("Verdana", 13, "bold"), command=self.huy_dang_ky, width=100).pack(side="right", padx=5, pady=20)
        ctk.CTkButton(btn_frame, fg_color="#4CAF50", hover_color="#616262", text="Đăng ký lớp học", text_color="white", font=("Verdana", 13, "bold"), command=self.dang_ky, width=120).pack(side="right", padx=5, pady=20)

        detail_frame = ctk.CTkFrame(content_frame, fg_color="#f2f2f2", corner_radius=30)
        detail_frame.pack(padx=20, pady=10)
        
        self.label_lop = ctk.CTkLabel(detail_frame, text="", font=("Arial", 15, "bold"), text_color="black")
        self.label_lop.grid(row=0, column=0, padx=40)

        self.label_mon = ctk.CTkLabel(detail_frame, text="", font=("Arial", 15, "bold"), text_color="black")
        self.label_mon.grid(row=0, column=1, padx=40)

        self.label_gv = ctk.CTkLabel(detail_frame, text="", font=("Arial", 15, "bold"), text_color="black")
        self.label_gv.grid(row=0, column=2, padx=40)

        self.label_sl = ctk.CTkLabel(detail_frame, text="", font=("Arial", 15, "bold"), text_color="black")
        self.label_sl.grid(row=0, column=3, padx=40)

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

        tree_frame = ctk.CTkFrame(content_frame, fg_color="white")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("STT", "MSSV", "Họ và Tên", "Ngày Sinh", "Khoa", "Email"), show="headings", style="Treeview")

        self.tree.heading("STT", text="STT")
        self.tree.heading("MSSV", text="MSSV")
        self.tree.heading("Họ và Tên", text="Họ và Tên")
        self.tree.heading("Ngày Sinh", text="Ngày Sinh")
        self.tree.heading("Khoa", text="Khoa")
        self.tree.heading("Email", text="Email")

        self.tree.column("STT", width=20, anchor="center")
        self.tree.column("MSSV", width=40, anchor="center")
        self.tree.column("Họ và Tên", width=140, anchor="center")
        self.tree.column("Ngày Sinh", width=40, anchor="center")
        self.tree.column("Khoa", width=140, anchor="center")
        self.tree.column("Email", width=160, anchor="center")

        self.tree.pack(fill="both", expand=True)  

        self.tree.bind("<Double-1>", self.deselect)

    def back_to_lop_admin(self):
        if self.app:
            self.app.show_classAdmin_frame()
    
    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        sv_list = self.lop_controller.get_students_in_class(self.ma_lop_hien_tai)

        for index, sv in enumerate(sv_list, start=1):
            ma_sv = sv.get("mssv", "")
            ho_ten = sv.get("ho_ten", "")
            ngay_sinh = sv.get("ngay_sinh", "")
            khoa = sv.get("khoa","")
            email = sv.get("email", "")

            if isinstance(ngay_sinh, (str,)):
                formatted_date = ngay_sinh
            else:
                try:
                    formatted_date = ngay_sinh.strftime("%d-%m-%Y")
                except:
                    formatted_date = ""

            self.tree.insert("", "end", values=(index, ma_sv, ho_ten, formatted_date, khoa, email))

    def deselect(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.selection_remove(selected_item)

    def thong_tin_lop(self, ma_lop): 
        if not ma_lop:
            return
        
        self.ma_lop_hien_tai = ma_lop
        lop = self.lop_controller.get_by_ma_lop(ma_lop)
        
        if not lop:
            messagebox.showwarning("Lỗi", f"Không tìm thấy thông tin lớp học với mã {ma_lop}.")
            return

        self.label_lop.configure(text=f"Lớp: {lop.get('ma_lop', '')}")
        self.label_mon.configure(text=f"Môn: {lop.get('ma_mon', '')}")

        ma_gv = lop.get("ma_gv")
        self.label_gv.configure(text=f"Giảng viên: {ma_gv if ma_gv else 'Chưa phân công'}")

        self.label_sl.configure(text=f"Số lượng sinh viên: {lop.get('so_luong', 0)}")

        self.update_treeview()

    def dang_ky(self):
        DangKySinhVienVaoLopView(self, lop_controller=self.lop_controller, sv_controller=self.sv_controller, ma_lop=self.ma_lop_hien_tai)

    def huy_dang_ky(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên để hủy đăng ký.")
            return

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn hủy đăng ký cho sinh viên này không?")
        if not confirm:
            return

        for item in selected:
            mssv = self.tree.item(item, "values")[1] 
            if self.lop_controller.huy_dang_ky(mssv, self.ma_lop_hien_tai):
                messagebox.showinfo("Thành công", f"Đã hủy đăng ký cho sinh viên mã {mssv}.")
            else:
                messagebox.showerror("Lỗi", f"Không thể hủy đăng ký sinh viên {mssv}.")
        
        self.update_treeview()

    def phan_cong_giang_vien(self):
        PhanCongGvView(self, lop_controller=self.lop_controller, gv_controller= self.gv_controller, ma_lop = self.ma_lop_hien_tai)

    def xuat_danh_sach(self):
        try:
            students = self.lop_controller.get_students_in_class(self.ma_lop_hien_tai)

            if not students:
                messagebox.showinfo("Thông báo", "Lớp chưa có sinh viên đăng ký.")
                return

            df = pd.DataFrame(students)
            df.columns = ["MSSV", "Họ Tên", "Ngày Sinh", "Khoa", "Email"]

            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Thành công", f"Xuất danh sách thành công!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Xuất file thất bại: {e}")