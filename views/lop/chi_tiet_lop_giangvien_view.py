import tkinter as ttk
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

from controllers.lop_controller import LopController
    
class ChiTietLopGiangVienFrame(ctk.CTkFrame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#ffffff")
        self.app = app
        self.lop_controller = LopController()

        # Nội dung trang
        content_frame = ctk.CTkFrame(self, fg_color="#ffffff", width=824, height=600)
        content_frame.pack(side="top", fill="both", expand=True)

        # Header 
        header_frame = ctk.CTkFrame(content_frame, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(header_frame, text="Thông tin Lớp Học", font=("Verdana", 18, "bold"), text_color="#ffffff")
        label_title.pack(pady=20)

        btn_frame = ctk.CTkFrame(content_frame, fg_color="white")
        btn_frame.pack(padx=20, pady=5, fill="x")
       
        ctk.CTkButton(btn_frame, fg_color="#904fd2", hover_color="#616262", text="◀ Quay lại",  text_color="white", font=("Verdana", 13, "bold"), command=self.back_to_lop_GV, width=80).pack(side="left", padx=5, pady=20)
        ctk.CTkButton(btn_frame, fg_color="#f89924", hover_color="#616262", text="Xuất danh sách ☰",  text_color="white", font=("Verdana", 13, "bold"), command=None, width=100).pack(side="right", padx=5, pady=20)
        ctk.CTkButton(btn_frame, fg_color="#4CAF50", hover_color="#616262", text="Nhập điểm", text_color="white", font=("Verdana", 13, "bold"), command=None, width=80).pack(side="right", padx=5, pady=20)

        detail_frame = ctk.CTkFrame(content_frame, fg_color="white")
        detail_frame.pack(padx=20, pady=10)
        
        ctk.CTkLabel(detail_frame, text="Lớp :", font=("Verdana", 15, "bold"), text_color="black").grid(row=0, column=0, padx=10)
        ctk.CTkLabel(detail_frame, text="Môn :", font=("Verdana", 15, "bold"), text_color="black").grid(row=0, column=3, padx=10)
        ctk.CTkLabel(detail_frame, text="Số lượng SV :", font=("Verdana", 15, "bold"), text_color="black").grid(row=0, column=9, padx=10)

        # Style TreeView
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

        # Frame chứa Treeview
        tree_frame = ctk.CTkFrame(content_frame, fg_color="white")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("Mã Lớp", "Mã Môn", "Số Lượng", "Học Kỳ", "Năm", "Mã GV"), show="headings", style="Treeview")

        # Thiết lập tiêu đề cột
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

    def back_to_lop_GV(self):
        if self.app:
            self.app.show_classGV_frame()

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
