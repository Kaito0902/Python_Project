import customtkinter as ctk
from tkinter import ttk, messagebox
from views.mon_hoc.insert_mon_hoc import ThemMonHocWindow
from controllers.mon_hoc_controller import MonHocController

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class MonHocFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.controller = MonHocController()
        self.parent = parent
        self.pack(pady=20, padx=20, fill="both", expand=True)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        ctk.CTkLabel(self, text="QUẢN LÝ MÔN HỌC", font=("Arial", 18, "bold")).pack(pady=10)

        search_frame = ctk.CTkFrame(self, fg_color="white")
        search_frame.pack(pady=5, padx=20, fill="x")

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm...", width=300)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", self.tim_kiem_mon_hoc)

        btn_frame = ctk.CTkFrame(search_frame, fg_color="white")
        btn_frame.pack(side="right")

        ctk.CTkButton(btn_frame, fg_color="green", text="Thêm", text_color="white", command=self.them_mon_hoc, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, fg_color="orange", text="Sửa", text_color="white", command=self.sua_mon_hoc, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, fg_color="red", text="Xóa",  text_color="white", command=self.xoa_mon_hoc, width=80).pack(side="left", padx=5)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, borderwidth=1, relief="solid", font=("Arial", 14))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        columns = ("Mã Môn", "Tên Môn", "Số Tín Chỉ", "Khoa")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", style="Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_row_click)

    def them_mon_hoc(self):
        ThemMonHocWindow(self, self.controller)

    def sua_mon_hoc(self):
        if not hasattr(self, "selected_mh"):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn môn học trước!")
            return
        # sửa

    def xoa_mon_hoc(self):
        if not hasattr(self, "selected_mh"):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn môn học trước!")
            return

        confirm = messagebox.askyesno("Xác nhận",
                                      f"Bạn có chắc chắn muốn xóa môn học {self.selected_mh['ten_mh']} không?")
        if confirm:
            self.controller.delete(self.selected_mh["ma_mh"])
            self.load_data()
            messagebox.showinfo("Thành công", "Xóa môn học thành công!")

    def fill_tree(self, mon_hoc_list):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for mon_hoc in mon_hoc_list:
            ma_mh = mon_hoc.get("ma_mon", "")
            ten_mh = mon_hoc.get("ten_mon", "")
            so_tin_chi = mon_hoc.get("so_tin_chi", "")
            khoa = mon_hoc.get("khoa", "")
            self.tree.insert("", "end", values=(ma_mh, ten_mh, so_tin_chi, khoa))

    def load_data(self):
        self.fill_tree(self.controller.select_all())

    def on_row_click(self, event):
        try:
            item = self.tree.selection()[0]
            values = self.tree.item(item, "values")
            self.selected_mh = {
                "ma_mh": values[0],
                "ten_mh": values[1],
                "so_tin_chi": values[2],
                "khoa": values[3]
            }
        except Exception:
            pass

    def tim_kiem_mon_hoc(self, event=None):
        keyword = self.search_entry.get().strip()
        if keyword:
            result = self.controller.select_by(keyword)
            self.fill_tree(result)
        else:
            self.load_data()
