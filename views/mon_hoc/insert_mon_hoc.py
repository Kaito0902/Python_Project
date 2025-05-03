import customtkinter as ctk
from tkinter import messagebox
from controllers.mon_hoc_controller import MonHocController
from controllers.khoa_controller import KhoaController

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ThemMonHocWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller: MonHocController):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.khoacontroller = KhoaController()
        self.title("Thêm Môn Học")
        self.geometry("500x300")
        self.configure(bg="#f5f5f5")

        self.attributes('-topmost', True)

        self.create_input_row("Mã Môn Học:", "ma_mh_entry")
        self.create_input_row("Tên Môn Học:", "ten_mh_entry")
        self.create_input_row("Số Tín Chỉ:", "so_tin_chi_entry")
        self.create_khoa_row()

        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Lưu", command=self.luu_mon_hoc).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Hủy bỏ", command=self.destroy).pack(side="right", padx=10, pady=5)

        self.load_khoa_options()

    def create_input_row(self, label_text, entry_attr):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(pady=5, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=label_text, width=80, anchor="w")
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(side="left", padx=10)

        setattr(self, entry_attr, entry)

    def create_khoa_row(self):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(pady=5, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text="Khoa:", width=80, anchor="w")
        label.pack(side="left", padx=10)

        self.khoa_combobox = ctk.CTkComboBox(frame, width=300, values=[])  # ban đầu chưa có dữ liệu
        self.khoa_combobox.pack(side="left", padx=10)
        self.khoa_combobox.set("Chọn-")

    def load_khoa_options(self):
        khoa_list = self.khoacontroller.select_all()

        # Mapping tên khoa -> mã khoa
        self.khoa_mapping = {khoa["ten_khoa"]: khoa["ma_khoa"] for khoa in khoa_list}

        ten_khoa_list = list(self.khoa_mapping.keys())
        self.khoa_combobox.configure(values=ten_khoa_list)

    def luu_mon_hoc(self):
        ma_mh = self.ma_mh_entry.get().strip()
        ten_mh = self.ten_mh_entry.get().strip()
        so_tin_chi = self.so_tin_chi_entry.get().strip()
        ten_khoa = self.khoa_combobox.get().strip()

        if not ma_mh or not ten_mh or not so_tin_chi or not ten_khoa:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            self.attributes('-topmost', True)
            return

        if not so_tin_chi.isdigit() or int(so_tin_chi) <= 0:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Số tín chỉ phải là số nguyên dương!")
            self.attributes('-topmost', True)
            return

        if self.controller.check_exists(ma_mh):
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Mã môn học đã tồn tại, vui lòng nhập mã khác!")
            self.attributes('-topmost', True)
            return

        # Lấy mã khoa từ tên khoa
        ma_khoa = self.khoa_mapping.get(ten_khoa)
        if not ma_khoa:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Không tìm thấy mã khoa tương ứng!")
            self.attributes('-topmost', True)
            return

        try:
            success = self.controller.insert(ma_mh, ten_mh, int(so_tin_chi), ma_khoa)
            if success:
                self.attributes('-topmost', False)
                messagebox.showinfo("Thành công", "Đã lưu thông tin môn học!")
                self.parent.load_data()
                self.destroy()
            else:
                raise ValueError("Không thể thêm môn học, có thể bị trùng Mã Môn Học!")
        except Exception as e:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", f"Lỗi khi thêm môn học: {str(e)}")
            self.attributes('-topmost', True)
