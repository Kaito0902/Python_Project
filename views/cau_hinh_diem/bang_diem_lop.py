import customtkinter as ctk
from tkinter import ttk, messagebox
from tkinter import filedialog
from controllers.chi_tiet_diem_controller import ChiTietDiemController
from controllers.lop_controller import LopController
from controllers.sinh_vien_controller import SinhVienController
from controllers.cau_hinh_diem_controller import CauHinhDiemController
from controllers.mon_hoc_controller import MonHocController


class BangDiemLop(ctk.CTkFrame):
    def __init__(self, parent, ma_lop=None):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.ma_lop = ma_lop
        self.controller = ChiTietDiemController()
        self.lopcontroller = LopController()
        self.svcontroller = SinhVienController()
        self.chdcontroller = CauHinhDiemController()
        self.moncontroller = MonHocController()

        self.cot_co_dinh = ["MSSV", "Tên Sinh Viên", "Điểm Kiểm Tra"]
        self.cot_diem_list = []

        header_frame = ctk.CTkFrame(self, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(header_frame, text="Bảng Điểm Lớp", font=("Verdana", 18, "bold"),
                                   text_color="#ffffff")
        label_title.pack(pady=20)

        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(fill="x", pady=5, padx=10)

        labels = ["Mã lớp:", "Môn học:", "Số lượng SV:"]
        values = [self.ma_lop, "", ""]
        self.info_labels = []

        for i, (label_text, value_text) in enumerate(zip(labels, values)):
            label = ctk.CTkLabel(self.info_frame, text=label_text, width=15, anchor="w")
            label.grid(row=0, column=2 * i, padx=(0, 5), pady=2, sticky="w")
            value_label = ctk.CTkLabel(self.info_frame, text=value_text, anchor="w")
            value_label.grid(row=0, column=2 * i + 1, padx=(0, 20), pady=2, sticky="w")
            self.info_labels.append((label, value_label))

        self.upload_button = ctk.CTkButton(self.info_frame, text="Tải ảnh lên", command=self.upload_image)
        self.upload_button.grid(row=0, column=6, padx=10, sticky="e")

        # Treeview
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(fill="both", expand=True)
        self.load_data()

    def create_treeview(self):

        for widget in self.tree_frame.winfo_children():
            widget.destroy()

        index_diem_kiem_tra = self.cot_co_dinh.index("Điểm Kiểm Tra")

        cot_truoc_diem_kt = self.cot_co_dinh[:index_diem_kiem_tra]
        cot_sau_diem_kt = self.cot_co_dinh[index_diem_kiem_tra:]

        columns = cot_truoc_diem_kt + [ten for ten, ts in self.cot_diem_list] + cot_sau_diem_kt

        style = ttk.Style()
        style.configure("Treeview", background="#f5f5f5", foreground="black", rowheight=30, fieldbackground="lightgray")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#3084ee", foreground="black")
        style.map("Treeview", background=[("selected", "#4CAF50")], foreground=[("selected", "white")])

        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", style="Treeview")
        self.tree.pack(fill="both", expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

    def fill_tree(self, chi_tiet_diem_list):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for sv_data in chi_tiet_diem_list:
            mssv = sv_data.get("mssv", "")
            ho_ten = sv_data.get("ho_ten", "")
            row = [mssv, ho_ten]
            for ten_cot_diem, _ in self.cot_diem_list:
                row.append(sv_data.get(ten_cot_diem, ""))
            row.append("")  # Cột "Điểm Kiểm Tra" mặc định
            self.tree.insert("", "end", values=row)

    def load_data(self):
        self.lopcontroller = LopController()
        lop_info = self.lopcontroller.get_by_ma_lop(self.ma_lop)
        ma_mon = lop_info.get("ma_mon", "") if lop_info else ""
        ten_mon = self.moncontroller.select_by_id(ma_mon)[0]["ten_mon"]

        # Lấy danh sách sinh viên
        ds_sinh_vien = self.lopcontroller.get_students_in_class(self.ma_lop)
        so_luong_sv = len(ds_sinh_vien)

        # Cập nhật label thông tin
        self.info_labels[1][1].configure(text=ten_mon)  # Môn học
        self.info_labels[2][1].configure(text=str(so_luong_sv))  # Số lượng SV

        # Lấy danh sách cột điểm theo cấu hình
        self.chdcontroller = CauHinhDiemController()
        ds_cot_diem = self.chdcontroller.select_all(self.ma_lop)
        self.cot_diem_list = [(cot["ten_cot_diem"], cot["trong_so"]) for cot in ds_cot_diem]

        # Tạo lại bảng với các cột
        self.create_treeview()

        # Lấy chi tiết điểm đã có (nếu có)
        self.controller = ChiTietDiemController()
        chi_tiet_diem_list = self.controller.select_all(self.ma_lop)

        # Duyệt sinh viên
        for sv in ds_sinh_vien:
            mssv = sv["mssv"]
            ten_sv = sv["ho_ten"]
            diem_dict = {cot["ten_cot_diem"]: "" for cot in ds_cot_diem}  # mặc định chưa có điểm

            # Gán điểm nếu có
            for diem in chi_tiet_diem_list:
                if diem["mssv"] == mssv:
                    ten_cot = diem["ten_cot_diem"]
                    diem_dict[ten_cot] = diem["diem"]

            # Chuẩn bị dòng dữ liệu
            values = [mssv, ten_sv] + [diem_dict[cot[0]] for cot in self.cot_diem_list] + [
                ""]  # "" cho cột "Điểm kiểm tra"
            self.tree.insert("", "end", values=values)

    def add_new_column(self, ten_cot_diem, trong_so):
        self.cot_diem_list.append((ten_cot_diem, trong_so))
        self.create_treeview()

    def remove_column(self, ten_cot_diem):
        self.cot_diem_list = [(ten, ts) for ten, ts in self.cot_diem_list if ten != ten_cot_diem]
        self.create_treeview()

    def refresh_columns_and_data(self):
        self.clear_table()
        self.load_data()

    def clear_table(self):
        if hasattr(self, 'tree') and self.tree:
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.tree.destroy()


    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file ảnh",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            messagebox.showinfo("Tải ảnh thành công", f"Đã chọn file:\n{file_path}")

