import tkinter as ttk
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox, ttk
from datetime import datetime

from views.lop.them_lop_view import ThemLopHoc
from views.lop.update_lop_view import UpdateLopHoc
from controllers.lop_controller import LopController
    
class LopAdminFrame(ctk.CTkFrame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#ffffff")
        self.app = app
        self.lop_controller = LopController()

        content_frame = ctk.CTkFrame(self, fg_color="#ffffff", width=824, height=600)
        content_frame.pack(side="top", fill="both", expand=True)

        header_frame = ctk.CTkFrame(content_frame, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(header_frame, text="Quản Lý Lớp Học", font=("Verdana", 18, "bold"), text_color="#ffffff")
        label_title.pack(pady=20)

        search_frame = ctk.CTkFrame(content_frame, fg_color="white")
        search_frame.pack(padx=20, pady=5, fill="x")

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm...", width=300)
        self.search_entry.pack(side="left", padx=10, pady=20)
        
        icon = ctk.CTkImage(Image.open(r"resources\images\search.png").resize((20,20)), size=(20, 20))
        ctk.CTkButton(search_frame, image=icon, text="", width=20, height=20, fg_color="#ffffff", hover_color="#ffffff", command=self.search).pack(side="left", pady=20)

        btn_frame = ctk.CTkFrame(search_frame, fg_color="white")
        btn_frame.pack(side="right")

        ctk.CTkButton(btn_frame, fg_color="#4CAF50", text="Thêm", text_color="white", font=("Verdana", 13, "bold"), command=self.add_class, width=80).pack(side="left", padx=5, pady=20)
        ctk.CTkButton(btn_frame, fg_color="#fbbc0e", text="Sửa", text_color="white", font=("Verdana", 13, "bold"), command=self.update_class, width=80).pack(side="left", padx=5, pady=20)
        ctk.CTkButton(btn_frame, fg_color="#F44336", text="Xóa",  text_color="white", font=("Verdana", 13, "bold"), command=self.delete_class, width=80).pack(side="left", padx=5, pady=20)
        ctk.CTkButton(btn_frame, fg_color="#904fd2", text="Xem chi tiết lớp học⏵",  text_color="white", font=("Verdana", 13, "bold"), command=self.show_detail, width=160).pack(side="left", padx=5, pady=20)

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

        self.tree = ttk.Treeview(tree_frame, columns=("Mã Lớp","Môn Học", "Mã Môn", "Số Lượng", "Học Kỳ", "Năm", "Mã GV"), show="headings", style="Treeview")

        self.tree.heading("Mã Lớp", text="Mã Lớp")
        self.tree.heading("Môn Học", text="Môn Học")
        self.tree.heading("Mã Môn", text="Mã Môn")
        self.tree.heading("Số Lượng", text="Số Lượng")
        self.tree.heading("Học Kỳ", text="Học Kỳ")
        self.tree.heading("Năm", text="Năm")
        self.tree.heading("Mã GV", text="Mã GV")

        self.tree.column("Mã Lớp", width=60, anchor="center")
        self.tree.column("Môn Học", width=120)
        self.tree.column("Mã Môn", width=60, anchor="center")
        self.tree.column("Số Lượng", width=40, anchor="center")
        self.tree.column("Học Kỳ", width=40, anchor="center")
        self.tree.column("Năm", width=40, anchor="center")
        self.tree.column("Mã GV", width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True)  
        self.update_treeview()

        self.tree.bind("<Double-1>", self.deselect)

    def add_class(self):
        ThemLopHoc(self, self.lop_controller)

    def update_class(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn lớp học để cập nhật!")
            return

        values = self.tree.item(sel[0], 'values')
        nam = int(values[5])
        current_year = datetime.now().year

        editable = (nam >= current_year)

        form = UpdateLopHoc(self, self.lop_controller, editable=editable)
        form.set_data(*values)

    def delete_class(self):
        selected_item = self.tree.selection()
        if selected_item:
            confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa lớp học này?")
            if not confirm:
                return
            for item in selected_item:
                values = self.tree.item(item, 'values')
                self.lop_controller.delete(values[0])
            self.update_treeview()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn lớp học để xóa!")

    def search(self):
        query = self.search_entry.get().lower()
        results = self.lop_controller.search_class(query)
        self.update_treeview(results)

    def show_detail(self):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], 'values')
            ma_lop = values[0] 
            if self.app:
                self.app.selected_ma_lop = ma_lop  
                self.app.show_classAdmin_detail_frame()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn lớp học để xem chi tiết!")

    def update_treeview(self, data=None):
        self.tree.delete(*self.tree.get_children())
        classes  = data if data is not None else self.lop_controller.select_all()
        if not classes:
            messagebox.showinfo("Thông báo", "Không có dữ liệu lớp học!")
            return
        for lop in classes :
            self.tree.insert("", "end", values=(
                lop["ma_lop"], lop["ten_mon"], lop["ma_mon"], lop["so_luong"], lop["hoc_ky"], lop["nam"], lop["ma_gv"]
            ))

    def deselect(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.selection_remove(selected_item)
