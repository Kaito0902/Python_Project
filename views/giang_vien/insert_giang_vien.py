import customtkinter as ctk
from tkinter import messagebox
from controllers.giang_vien_controller import GiangVienController
from controllers.khoa_controller import KhoaController

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ThemGiangVienWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller: GiangVienController):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.khoacontroller = KhoaController()
        self.title("Thêm Giảng Viên")
        self.geometry("500x280")
        self.configure(bg="#f5f5f5")
        self.center_window(500, 280)

        self.attributes('-topmost', True)

        self.create_input_row("Mã GV:", "ma_gv_entry")
        self.create_input_row("Tên GV:", "ten_gv_entry")
        self.create_khoa_row()
        self.create_input_row("Email:", "email_entry")
        self.create_input_row("SĐT:", "sdt_entry")

        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Lưu", command=self.luu_giang_vien).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Hủy bỏ", command=self.destroy).pack(side="right", padx=10, pady=5)

        self.load_khoa_options()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 40 
        self.geometry(f"{width}x{height}+{x}+{y}")

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

        self.khoa_combobox = ctk.CTkComboBox(frame, width=300, values=[])  # khởi tạo rỗng
        self.khoa_combobox.pack(side="left", padx=10)
        self.khoa_combobox.set("Chọn-")

    def load_khoa_options(self):
        khoa_list = self.khoacontroller.select_all()

        # Tạo dict ánh xạ từ tên_khoa sang ma_khoa
        self.khoa_mapping = {khoa["ten_khoa"]: khoa["ma_khoa"] for khoa in khoa_list}

        ten_khoa_list = list(self.khoa_mapping.keys())  # lấy danh sách tên khoa
        self.khoa_combobox.configure(values=ten_khoa_list)

    def luu_giang_vien(self):
        ma_gv = self.ma_gv_entry.get().strip()
        ten_gv = self.ten_gv_entry.get().strip()
        ten_khoa = self.khoa_combobox.get().strip()
        email = self.email_entry.get().strip()
        sdt = self.sdt_entry.get().strip()

        if not (ma_gv and ten_gv and email and sdt):
            self.attributes('-topmost', False)
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            self.attributes('-topmost', True)
            return

        # Lấy mã khoa từ tên khoa
        ma_khoa = self.khoa_mapping.get(ten_khoa)

        if not ma_khoa:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Không tìm thấy mã khoa tương ứng!")
            self.attributes('-topmost', True)
            return

        if self.controller.check_exists(ma_gv):
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Mã giảng viên đã tồn tại, vui lòng nhập mã khác!")
            self.attributes('-topmost', True)
            return

        try:
            success = self.controller.insert(ma_gv, ten_gv, ma_khoa, email, sdt)
            if success:
                self.attributes('-topmost', False)
                messagebox.showinfo("Thành công", "Đã lưu thông tin giảng viên!")
                self.parent.load_data()
                self.destroy()
            else:
                raise ValueError("Không thể thêm giảng viên, có thể bị sai số điện thoại hoặc sai email!")
        except Exception as e:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", f"Lỗi khi thêm giảng viên: {str(e)}")
