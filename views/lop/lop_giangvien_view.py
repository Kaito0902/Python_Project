import tkinter as ttk
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from tkinter import ttk

from controllers.lop_controller import LopController
    
class LopGiangVienFrame(ctk.CTkFrame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#ffffff")
        self.app = app
        self.lop_controller = LopController()

        content_frame = ctk.CTkFrame(self, fg_color="#ffffff", width=824, height=600)
        content_frame.pack(side="top", fill="both", expand=True)

        header_frame = ctk.CTkFrame(content_frame, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(header_frame, text="Lớp Học Của Tôi", font=("Verdana", 18, "bold"), text_color="#ffffff")
        label_title.pack(pady=20)

        search_frame = ctk.CTkFrame(content_frame, fg_color="white")
        search_frame.pack(padx=20, pady=5, fill="x")
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm...", width=300)
        self.search_entry.pack(side="left", padx=10, pady=20)
        
        icon = ctk.CTkImage(Image.open(r"resources\images\search.png").resize((20,20)), size=(20, 20))
        btn_search = ctk.CTkButton(search_frame, image=icon, text="", width=20, height=20, fg_color="#ffffff", hover_color="#ffffff", command=None)
        btn_search.pack(side="left", pady=20)

        btn_frame = ctk.CTkFrame(search_frame, fg_color="white")
        btn_frame.pack(side="right")

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

        self.tree = ttk.Treeview(tree_frame, columns=("Mã Lớp", "Mã Môn", "Số Lượng", "Học Kỳ", "Năm", "Mã GV"), show="headings", style="Treeview")

        self.tree.heading("Mã Lớp", text="Mã Lớp")
        self.tree.heading("Mã Môn", text="Mã Môn")
        self.tree.heading("Số Lượng", text="Số Lượng")
        self.tree.heading("Học Kỳ", text="Học Kỳ")
        self.tree.heading("Năm", text="Năm")
        self.tree.heading("Mã GV", text="Mã GV")

        self.tree.column("Mã Lớp", width=80, anchor="center")
        self.tree.column("Mã Môn", width=80, anchor="center")
        self.tree.column("Số Lượng", width=40, anchor="center")
        self.tree.column("Học Kỳ", width=40, anchor="center")
        self.tree.column("Năm", width=40, anchor="center")
        self.tree.column("Mã GV", width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True)  
        self.update_treeview()
        
        self.tree.bind("<Double-1>", self.deselect)

    def show_detail(self):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], 'values')
            ma_lop = values[0]
            if self.app:
                self.app.selected_ma_lop = ma_lop
                self.app.show_diemlop_frame()
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
                lop["ma_lop"], lop["ma_mon"], lop["so_luong"], lop["hoc_ky"], lop["nam"], lop["ma_gv"]
            ))

    def deselect(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.selection_remove(selected_item)



