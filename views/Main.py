import customtkinter as ctk
from PIL import Image
from views.sinh_vien_view import StudentFrame
from views.giang_vien.giang_vien_view import GiangVienFrame
from views.khoa.khoa_view import KhoaFrame
from views.mon_hoc.mon_hoc_view import MonHocFrame
from views.lop.lop_admin_view import LopAdminFrame
from views.lop.lop_giangvien_view import LopGiangVienFrame
from views.lop.chi_tiet_lop_admin_view import ChiTietLopAdminFrame
from views.lop.chi_tiet_lop_giangvien_view import ChiTietLopGiangVienFrame
from views.cau_hinh_diem.QuanLyLopTabbedPane import QuanLyLopTabbedPane
from views.account_view import AccountManager
from session import current_user


class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Trang chủ")
        self.geometry("1024x600")
        self.configure(fg_color="#ffffff")
        self.center_window(1024, 600)
        
        self.selected_ma_lop = None
        self.init_menu()
        self.init_main_content()

    def init_menu(self):
        self.menu_frame = ctk.CTkFrame(self, fg_color="#3084ee", width=200)
        self.menu_frame.pack(side="left", fill="y")

        # Logo
        image = Image.open(r"D:\Downloads\sever nro\icon\Python_Project-master1\resources\images\logo.png").resize((200, 200))
        photo = ctk.CTkImage(light_image=image, size=(100, 100))
        img_label = ctk.CTkLabel(self.menu_frame, image=photo, text="", fg_color="#ffffff")
        img_label.grid(row=0, column=0, pady=15)

        # Nút style
        button_style = {
            "font": ("Arial", 17, "bold"),
            "fg_color": "#98c2f7",
            "text_color": "white",
            "width": 150,
            "height": 40
        }

        ctk.CTkButton(self.menu_frame, text="Tài khoản", **button_style, command=self.show_account_frame).grid(row=1, column=0, pady=5)
        ctk.CTkButton(self.menu_frame, text="Lớp học", **button_style, command=self.show_classAdmin_frame).grid(row=2, column=0, pady=5)
        # ctk.CTkButton(self.menu_frame, text="Lớp học", **button_style, command=self.show_classGV_frame).grid(row=2, column=0, pady=5)
        ctk.CTkButton(self.menu_frame, text="Môn học", **button_style, command=self.show_subject_frame).grid(row=3, column=0, pady=5)
        ctk.CTkButton(self.menu_frame, text="Giảng viên", **button_style, command=self.show_teacher_frame).grid(row=4, column=0, pady=5)
        ctk.CTkButton(self.menu_frame, text="Sinh viên", **button_style, command=self.show_student_frame).grid(row=5, column=0, pady=5)
        ctk.CTkButton(self.menu_frame, text="Khoa", **button_style, command=self.show_khoa_frame).grid(row=6, column=0, pady=5)
        ctk.CTkButton(self.menu_frame, text="Thống kê", **button_style).grid(row=7, column=0, pady=5)

        logout_btn = ctk.CTkButton(self.menu_frame, text="Đăng xuất", **button_style, command=self.destroy)
        logout_btn.grid(row=7, column=0, pady=5)

        logout_btn.bind("<Enter>", lambda e: logout_btn.configure(fg_color="#e8473d"))
        logout_btn.bind("<Leave>", lambda e: logout_btn.configure(fg_color="#98c2f7"))
    
    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 40 
        self.geometry(f"{width}x{height}+{x}+{y}")

    def init_main_content(self):
        self.main_content = ctk.CTkFrame(self, fg_color="#ffffff")
        self.main_content.pack(side="right", fill="both", expand=True)

    def show_account_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()
        account_frame = AccountManager(self.main_content)
        account_frame.pack(fill="both", expand=True)

    def show_khoa_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()
        khoa_frame = KhoaFrame(self.main_content)
        khoa_frame.pack(fill="both", expand=True)

    def show_student_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        student_frame = StudentFrame(self.main_content)
        student_frame.pack(fill="both", expand=True)

    def show_teacher_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        giang_vien_frame = GiangVienFrame(self.main_content)
        giang_vien_frame.pack(fill="both", expand=True)

    def show_subject_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        mon_hoc_frame = MonHocFrame(self.main_content)
        mon_hoc_frame.pack(fill="both", expand=True)

    def show_classAdmin_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        classAdmin_frame = LopAdminFrame(self.main_content, app=self)
        classAdmin_frame.pack(fill="both", expand=True)

    def show_classAdmin_detail_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        chi_tiet_Admin_frame = ChiTietLopAdminFrame(self.main_content, app=self)
        chi_tiet_Admin_frame.pack(fill="both", expand=True)
        chi_tiet_Admin_frame.thong_tin_lop(self.selected_ma_lop)
    
    def show_classGV_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        classGV_frame = LopGiangVienFrame(self.main_content, app=self)
        classGV_frame.pack(fill="both", expand=True)

    def show_classGV_detail_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        chi_tiet_GV_frame = ChiTietLopGiangVienFrame(self.main_content, app=self)
        chi_tiet_GV_frame.pack(fill="both", expand=True)

    def show_diemlop_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()
        bang_diem_lop_frame = QuanLyLopTabbedPane(self.main_content)
        bang_diem_lop_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    current_user.update({"ma_nguoi_dung": "admin", "username": "admin", "vai_tro_id": "admin"})
    app = MainView()
    app.mainloop()
