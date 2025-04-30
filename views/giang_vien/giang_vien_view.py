from PIL import Image
import customtkinter as ctk
from tkinter import ttk, messagebox
from views.giang_vien.insert_giang_vien import ThemGiangVienWindow
from views.giang_vien.update_giang_vien import SuaGiangVienWindow
from controllers.giang_vien_controller import GiangVienController
from controllers.khoa_controller import KhoaController


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class GiangVienFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.controller = GiangVienController()
        self.khoa_controller = KhoaController()
        self.parent = parent
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        header_frame = ctk.CTkFrame(self, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(header_frame, text="Quản Lý Giảng Viên", font=("Verdana", 18, "bold"), text_color="#ffffff")
        label_title.pack(pady=20)

        search_frame = ctk.CTkFrame(self, fg_color="white")
        search_frame.pack(pady=5, padx=20, fill="x")

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm...", width=300)
        self.search_entry.pack(side="left", padx=10, pady=20)
        self.search_entry.bind("<KeyRelease>", self.tim_kiem_giang_vien)

        icon = ctk.CTkImage(Image.open(r"resources\images\search.png").resize(
                (20, 20)), size=(20, 20))
        btn_search = ctk.CTkButton(search_frame, image=icon, text="", width=20, height=20, fg_color="#ffffff",
                                   hover_color="#ffffff", command=None)
        btn_search.pack(side="left", pady=20)

        btn_frame = ctk.CTkFrame(search_frame, fg_color="white")
        btn_frame.pack(side="right")

        ctk.CTkButton(btn_frame, fg_color="#4CAF50", text="Thêm", font=("Verdana", 13, "bold"), text_color="white", command=self.them_giang_vien, width=80).pack(side="left", padx=5,pady=20)
        ctk.CTkButton(btn_frame, fg_color="#fbbc0e", text="Sửa", font=("Verdana", 13, "bold"), text_color="white", command=self.sua_giang_vien, width=80).pack(side="left", padx=5,pady=20)
        ctk.CTkButton(btn_frame, fg_color="#F44336", text="Xóa", font=("Verdana", 13, "bold"),  text_color="white", command=self.xoa_giang_vien, width=80).pack(side="left", padx=5,pady=20)

        style = ttk.Style()
        style.configure("Treeview", background="#f5f5f5", foreground="black", rowheight=30, fieldbackground="lightgray")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#3084ee", foreground="black")
        style.map("Treeview", background=[("selected", "#4CAF50")], foreground=[("selected", "white")])

        columns = ("Mã GV", "Tên GV", "Khoa", "Email", "SĐT")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", style="Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            
        self.tree.column("Mã GV", width=60, anchor="center")
        self.tree.column("Tên GV", width=120, anchor="center")
        self.tree.column("Khoa", width=80, anchor="center")
        self.tree.column("Email", width=120, anchor="center")
        self.tree.column("SĐT", width=100, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_row_click)

    def them_giang_vien(self):
        ThemGiangVienWindow(self, self.controller)

    def sua_giang_vien(self):
        if not hasattr(self, "selected_gv"):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn giảng viên trước!")
            return
        SuaGiangVienWindow(self, self.tree, self.controller)

    def xoa_giang_vien(self):
        if not hasattr(self, "selected_gv"):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn giảng viên trước!")
            return

        confirm = messagebox.askyesno("Xác nhận",
                                      f"Bạn có chắc chắn muốn xóa giảng viên {self.selected_gv['ten_gv']} không?")
        if confirm:
            self.controller.delete(self.selected_gv["ma_gv"])
            self.load_data()
            messagebox.showinfo("Thành công", "Xóa giảng viên thành công!")

    def fill_tree(self, giang_vien_list):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for giang_vien in giang_vien_list:
            ma_gv = giang_vien.get("ma_gv", "")
            ten_gv = giang_vien.get("ho_ten", "")
            id_khoa = giang_vien.get("khoa", "")

            # Dùng KhoaController lấy tên khoa
            khoa_info = self.khoa_controller.select_by_id(id_khoa)
            ten_khoa = khoa_info.get("ten_khoa", "") if khoa_info else ""

            email = giang_vien.get("email", "")
            sdt = giang_vien.get("sdt", "")
            self.tree.insert("", "end", values=(ma_gv, ten_gv, ten_khoa, email, sdt))

    def load_data(self):
        self.fill_tree(self.controller.select_all())

    def on_row_click(self, event):
        try:
            item = self.tree.selection()[0]
            values = self.tree.item(item, "values")
            self.selected_gv = {
                "ma_gv": values[0],
                "ten_gv": values[1],
                "khoa": values[2],
                "email": values[3],
                "sdt": values[4]
            }
        except Exception:
            pass

    def tim_kiem_giang_vien(self, event=None):
        keyword = self.search_entry.get().strip()
        if keyword:
            result = self.controller.select_by(keyword)
            self.fill_tree(result)
        else:
            self.load_data()
