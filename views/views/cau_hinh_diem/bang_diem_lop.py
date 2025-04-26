import customtkinter as ctk
from tkinter import ttk, messagebox
from tkinter import filedialog

class BangDiemLop(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=10, pady=10)

        self.cot_co_dinh = ["MSSV", "Tên Sinh Viên", "Ngày Sinh", "Giới Tính", "Điểm Kiểm Tra"]
        self.cot_diem_list = []
        ctk.CTkLabel(self, text="BẢNG ĐIỂM LỚP", font=("Arial", 18, "bold")).pack(pady=10)

        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(fill="x", pady=5, padx=10)

        labels = ["Mã lớp:", "Môn học:", "Số lượng SV:"]
        values = ["", "", ""]
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
        self.create_treeview()

    def create_treeview(self):

        for widget in self.tree_frame.winfo_children():
            widget.destroy()

        index_diem_kiem_tra = self.cot_co_dinh.index("Điểm Kiểm Tra")

        cot_truoc_diem_kt = self.cot_co_dinh[:index_diem_kiem_tra]
        cot_sau_diem_kt = self.cot_co_dinh[index_diem_kiem_tra:]

        columns = cot_truoc_diem_kt + [ten for ten, ts in self.cot_diem_list] + cot_sau_diem_kt

        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

    def add_new_column(self, ten_cot_diem, trong_so):
        self.cot_diem_list.append((ten_cot_diem, trong_so))
        self.create_treeview()

    def remove_column(self, ten_cot_diem):
        self.cot_diem_list = [(ten, ts) for ten, ts in self.cot_diem_list if ten != ten_cot_diem]
        self.create_treeview()

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file ảnh",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            messagebox.showinfo("Tải ảnh thành công", f"Đã chọn file:\n{file_path}")

