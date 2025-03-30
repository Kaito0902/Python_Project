import customtkinter as ctk
from tkinter import ttk, messagebox
from views.giang_vien.insert_giang_vien import ThemGiangVienWindow
from controllers.giang_vien_controller import GiangVienController

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class GiangVienFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.controller = GiangVienController()
        self.parent = parent
        self.pack(pady=20, padx=20, fill="both", expand=True)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):

        ctk.CTkLabel(self, text="QUẢN LÝ GIẢNG VIÊN", font=("Arial", 18, "bold")).pack(pady=10)

        search_frame = ctk.CTkFrame(self, fg_color="white")
        search_frame.pack(pady=5, padx=20, fill="x")

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm...", width=300)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", self.tim_kiem_giang_vien)

        btn_frame = ctk.CTkFrame(search_frame, fg_color="white")
        btn_frame.pack(side="right")

        ctk.CTkButton(btn_frame, fg_color="green", text="Thêm", text_color="white", command=self.them_giang_vien, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, fg_color="orange", text="Sửa", text_color="white", command=self.sua_giang_vien, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, fg_color="red", text="Xóa",  text_color="white", command=self.xoa_giang_vien, width=80).pack(side="left", padx=5)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, borderwidth=1, relief="solid", font=("Arial", 14))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        columns = ("Mã GV", "Tên GV", "Khoa", "Email", "SĐT")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", style="Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_row_click)

    def them_giang_vien(self):
        ThemGiangVienWindow(self, self.controller)

    def sua_giang_vien(self):
        if not hasattr(self, "selected_gv"):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn giảng viên trước!")
            return
        # sửa

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
            khoa = giang_vien.get("khoa", "")
            email = giang_vien.get("email", "")
            sdt = giang_vien.get("sdt", "")
            self.tree.insert("", "end", values=(ma_gv, ten_gv, khoa, email, sdt))

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
