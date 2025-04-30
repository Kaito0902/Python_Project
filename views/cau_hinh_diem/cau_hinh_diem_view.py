import customtkinter as ctk
from tkinter import ttk, messagebox
from .insert_cot_diem import ThemCotDiemWindow
from .update_cot_diem import SuaCotDiem
from controllers.cau_hinh_diem_controller import CauHinhDiemController


class CauHinhDiemFrame(ctk.CTkFrame):
    def __init__(self, parent, bang_diem_instance, ma_lop=None):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.bang_diem_instance = bang_diem_instance
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.ma_lop = ma_lop
        self.controller = CauHinhDiemController()
        self.create_widgets()

    def create_widgets(self):
        header_frame = ctk.CTkFrame(self, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(header_frame, text="Cấu Hình Điểm", font=("Verdana", 18, "bold"),
                                   text_color="#ffffff")
        label_title.pack(pady=20)

        search_frame = ctk.CTkFrame(self, fg_color="white")
        search_frame.pack(pady=5, padx=20, fill="x")

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm...", width=300)
        search_entry.pack(side="left", padx=10)

        btn_frame = ctk.CTkFrame(search_frame, fg_color="white")
        btn_frame.pack(side="right")

        ctk.CTkButton(btn_frame, fg_color="#4CAF50", text="Thêm", font=("Verdana", 13, "bold"), text_color="white", command=self.them_cot_diem, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, fg_color="#fbbc0e", text="Sửa", font=("Verdana", 13, "bold"), text_color="white", command=self.sua_cot_diem, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, fg_color="#F44336", text="Xóa", font=("Verdana", 13, "bold"), text_color="white", command=self.xoa_cot_diem, width=80).pack(side="left", padx=5)

        style = ttk.Style()
        style.configure("Treeview", background="#f5f5f5", foreground="black", rowheight=30, fieldbackground="lightgray")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#3084ee", foreground="black")
        style.map("Treeview", background=[("selected", "#4CAF50")], foreground=[("selected", "white")])

        columns = ("Mã Lớp", "Tên Cột Điểm", "Trọng Số")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", style="Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_row_click)
        self.load_data()


    def fill_tree(self, cau_hinh_diem_list):
        self.item_data_map = {}  # map tree item ID to full data (bao gồm id ẩn)
        for row in self.tree.get_children():
            self.tree.delete(row)

        for cau_hinh_diem in cau_hinh_diem_list:
            ma_lop = cau_hinh_diem.get("ma_lop", "")
            ten_cot_diem = cau_hinh_diem.get("ten_cot_diem", "")
            trong_so = cau_hinh_diem.get("trong_so", "")
            ma_cot_diem = cau_hinh_diem.get("id")  # Giả sử id là 'id'

            item_id = self.tree.insert("", "end", values=(ma_lop, ten_cot_diem, trong_so))
            self.item_data_map[item_id] = {
                "id": ma_cot_diem,
                "ma_lop": ma_lop,
                "ten_cot_diem": ten_cot_diem,
                "trong_so": trong_so
            }

    def load_data(self):
        self.controller = CauHinhDiemController()
        self.fill_tree(self.controller.select_all(self.ma_lop))

    def them_cot_diem(self):
        ThemCotDiemWindow(self, self.ma_lop, self.bang_diem_instance)

    def sua_cot_diem(self):
        if not hasattr(self, "selected_chd"):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột điểm cần sửa trước!")
            return
        SuaCotDiem(self, self.ma_lop, self.selected_chd, self.tree, self.controller, self.bang_diem_instance)

    def on_row_click(self, event):
        try:
            item_id = self.tree.selection()[0]
            selected_data = self.item_data_map.get(item_id)
            if selected_data:
                self.selected_chd = selected_data  # Giữ cả id và thông tin cần thiết
        except Exception:
            pass

    def xoa_cot_diem(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cột điểm để xóa!")
            return

        values = self.tree.item(selected_item,"values")
        ten_cot_diem = values[1]  # Cột thứ 3 là "Tên Cột Điểm"
        item_id = self.tree.selection()[0]
        selected_data = self.item_data_map.get(item_id)
        self.controller.delete(selected_data["id"])
        self.load_data()
        self.bang_diem_instance.refresh_columns_and_data()

        messagebox.showinfo("Thành công", f"Đã xóa cột điểm: {ten_cot_diem}")
