from PIL import Image
import customtkinter as ctk
from tkinter import ttk, messagebox
from views.khoa.insert_khoa import ThemKhoaWindow
from views.khoa.update_khoa import SuaKhoaWindow
from controllers.khoa_controller import KhoaController

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class KhoaFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.controller = KhoaController()
        self.parent = parent
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        header_frame = ctk.CTkFrame(self, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(header_frame, text="Quản Lý Khoa", font=("Verdana", 18, "bold"), text_color="#ffffff")
        label_title.pack(pady=20)

        search_frame = ctk.CTkFrame(self, fg_color="white")
        search_frame.pack(pady=5, padx=20, fill="x")

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm...", width=300)
        self.search_entry.pack(side="left", padx=10, pady=20)
        self.search_entry.bind("<KeyRelease>", self.tim_kiem_khoa)

        icon = ctk.CTkImage(Image.open(r"D:\Downloads\sever nro\icon\Python_Project-master1\resources\images\search.png").resize(
                (20, 20)), size=(20, 20))
        btn_search = ctk.CTkButton(search_frame, image=icon, text="", width=20, height=20, fg_color="#ffffff",
                                   hover_color="#ffffff", command=None)
        btn_search.pack(side="left", pady=20)

        btn_frame = ctk.CTkFrame(search_frame, fg_color="white")
        btn_frame.pack(side="right")

        ctk.CTkButton(btn_frame, fg_color="#4CAF50", text="Thêm", font=("Verdana", 13, "bold"), text_color="white", command=self.them_khoa, width=80).pack(side="left", padx=5,pady=20)
        ctk.CTkButton(btn_frame, fg_color="#fbbc0e", text="Sửa", font=("Verdana", 13, "bold"), text_color="white", command=self.sua_khoa, width=80).pack(side="left", padx=5,pady=20)
        ctk.CTkButton(btn_frame, fg_color="#F44336", text="Xóa", font=("Verdana", 13, "bold"),  text_color="white", command=self.xoa_khoa, width=80).pack(side="left", padx=5,pady=20)

        style = ttk.Style()
        style.configure("Treeview", background="#f5f5f5", foreground="black", rowheight=30, fieldbackground="lightgray")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#3084ee", foreground="black")
        style.map("Treeview", background=[("selected", "#4CAF50")], foreground=[("selected", "white")])

        columns = ("Mã Khoa", "Tên Khoa", "SĐT", "Email")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", style="Treeview")

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.column("Mã Khoa", width=80, anchor="center")
        self.tree.column("Tên Khoa", width=150, anchor="center")
        self.tree.column("SĐT", width=100, anchor="center")
        self.tree.column("Email", width=150, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_row_click)

    def them_khoa(self):
        ThemKhoaWindow(self, self.controller)

    def sua_khoa(self):
        if not hasattr(self, "selected_khoa"):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khoa trước!")
            return
        SuaKhoaWindow(self, self.tree, self.controller)

    def xoa_khoa(self):
        if not hasattr(self, "selected_khoa"):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khoa trước!")
            return

        confirm = messagebox.askyesno("Xác nhận",
                                      f"Bạn có chắc chắn muốn xóa khoa {self.selected_khoa['ten_khoa']} không?")
        if confirm:
            self.controller.delete(self.selected_khoa["ma_khoa"])
            self.load_data()
            messagebox.showinfo("Thành công", "Xóa khoa thành công!")

    def fill_tree(self, khoa_list):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for khoa in khoa_list:
            ma_khoa = khoa.get("ma_khoa", "")
            ten_khoa = khoa.get("ten_khoa", "")
            so_dien_thoai = khoa.get("so_dien_thoai", "")
            email = khoa.get("email", "")
            self.tree.insert("", "end", values=(ma_khoa, ten_khoa, so_dien_thoai, email))

    def load_data(self):
        self.fill_tree(self.controller.select_all())

    def on_row_click(self, event):
        try:
            item = self.tree.selection()[0]
            values = self.tree.item(item, "values")
            self.selected_khoa = {
                "ma_khoa": values[0],
                "ten_khoa": values[1],
                "so_dien_thoai": values[2],
                "email": values[3]
            }
        except Exception:
            pass

    def tim_kiem_khoa(self, event=None):
        keyword = self.search_entry.get().strip()
        if keyword:
            result = self.controller.select_by(keyword)
            self.fill_tree(result)
        else:
            self.load_data()
