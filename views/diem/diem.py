import tkinter as ttk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from controllers.diem_controller import DiemController

class TraCuuDiemFrame(ctk.CTkFrame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#ffffff")
        self.app = app
        self.controller = DiemController()

        content_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        content_frame.pack(fill="both", expand=True)

        # Tiêu đề
        header_frame = ctk.CTkFrame(content_frame, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(
            header_frame,
            text="Tra Cứu Điểm",
            font=("Verdana", 18, "bold"),
            text_color="#ffffff"
        )
        label_title.pack(pady=20)

        # Thanh tìm kiếm
        search_frame = ctk.CTkFrame(content_frame, fg_color="white")
        search_frame.pack(fill="x", padx=20, pady=(10, 0))

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm...", width=300)
        self.search_entry.pack(side="left", padx=(10, 5))

        search_button = ctk.CTkButton(
            search_frame,
            text="Tìm kiếm",
            fg_color="#1e90ff",
            text_color="white",
            font=("Verdana", 12),
            command=self.on_search
        )
        search_button.pack(side="left", padx=5)

        # Bảng kết quả
        tree_frame = ctk.CTkFrame(content_frame, fg_color="white")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

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

        self.tree = ttk.Treeview(tree_frame,
                                 columns=("mssv", "hoten", "tenmon", "kt", "cuoiky", "xeploai"),
                                 show="headings",
                                 style="Treeview")

        self.tree.heading("mssv", text="MSSV")
        self.tree.heading("hoten", text="Họ tên")
        self.tree.heading("tenmon", text="Tên môn")
        self.tree.heading("kt", text="Điểm kiểm tra")
        self.tree.heading("cuoiky", text="Điểm cuối kỳ")
        self.tree.heading("xeploai", text="Xếp loại")

        self.tree.column("mssv", width=100, anchor="center")
        self.tree.column("hoten", width=180, anchor="center")
        self.tree.column("tenmon", width=160, anchor="center")
        self.tree.column("kt", width=120, anchor="center")
        self.tree.column("cuoiky", width=120, anchor="center")
        self.tree.column("xeploai", width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.load_data()

    def load_data(self):
        data = self.controller.select_all()
        if data:
            for row in self.tree.get_children():
                self.tree.delete(row)
            for sv in data:
                mssv = sv.get("mssv", "")
                ho_ten = sv.get("ho_ten", "")
                ten_mon = sv.get("ten_mon", "")
                diem_kt = sv.get("diem_kiem_tra", "")
                diem_cuoiky = sv.get("diem_cuoi_ky", "")
                xep_loai = sv.get("xep_loai", "")

                self.tree.insert('', 'end', values=(mssv, ho_ten, ten_mon, diem_kt, diem_cuoiky, xep_loai))
        else:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị.")

    def on_search(self):
        keyword = self.search_entry.get().strip()
        if keyword:
            # Xử lý tìm kiếm ở đây hoặc gọi controller
            messagebox.showinfo("Tìm kiếm", f"Tìm kiếm với từ khóa: {keyword}")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm.")
