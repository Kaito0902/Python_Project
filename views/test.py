import customtkinter as ctk
from views.giang_vien.giang_vien_view import GiangVienFrame
from views.mon_hoc.mon_hoc_view import MonHocFrame
from views.cau_hinh_diem.QuanLyLopTabbedPane import QuanLyLopTabbedPane

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ứng dụng chính")
        self.geometry("1000x600")
        self.content_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#f5f5f5")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(side="bottom", pady=20)

        btn1 = ctk.CTkButton(button_frame, text="Quản lý Giảng Viên", command=self.mo_quan_ly_gv, width=200, height=40)
        btn1.pack(side="left", padx=10)

        btn2 = ctk.CTkButton(button_frame, text="Quản lý Môn Học", command=self.mo_quan_ly_mh, width=200, height=40)
        btn2.pack(side="left", padx=10)

        btn3 = ctk.CTkButton(button_frame, text="Quản lý Lớp", command=self.mo_quan_ly_lop, width=200, height=40)
        btn3.pack(side="left", padx=10)

        self.current_frame = None

    def clear_content(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def mo_quan_ly_gv(self):
        self.clear_content()
        self.current_frame = GiangVienFrame(self.content_frame)

    def mo_quan_ly_mh(self):
        self.clear_content()
        self.current_frame = MonHocFrame(self.content_frame)

    def mo_quan_ly_lop(self):
        self.clear_content()
        self.current_frame = QuanLyLopTabbedPane(self.content_frame)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
