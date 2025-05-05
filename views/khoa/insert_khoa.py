import customtkinter as ctk
from tkinter import messagebox
from controllers.khoa_controller import KhoaController

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ThemKhoaWindow(ctk.CTkToplevel):
    def __init__(self, parent, controller: KhoaController):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.title("Thêm Khoa")
        self.geometry("400x220")
        self.configure(bg="#f5f5f5")
        self.center_window(400, 220)

        self.attributes('-topmost', True)

        self.create_input_row("Mã Khoa:", "ma_khoa_entry")
        self.create_input_row("Tên Khoa:", "ten_khoa_entry")
        self.create_input_row("Số Điện Thoại:", "so_dien_thoai_entry")
        self.create_input_row("Email:", "email_entry")

        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Lưu", command=self.luu_khoa).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Hủy bỏ", command=self.destroy).pack(side="right", padx=10, pady=5)

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

        entry = ctk.CTkEntry(frame, width=250)
        entry.pack(side="left", padx=10)

        setattr(self, entry_attr, entry)

    def luu_khoa(self):
        ma_khoa = self.ma_khoa_entry.get().strip()
        ten_khoa = self.ten_khoa_entry.get().strip()
        so_dien_thoai = self.so_dien_thoai_entry.get().strip()
        email = self.email_entry.get().strip()

        if not (ma_khoa and ten_khoa and so_dien_thoai and email):
            self.attributes('-topmost', False)
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            self.attributes('-topmost', True)
            return

        if self.controller.check_exists(ma_khoa):
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Mã khoa đã tồn tại, vui lòng nhập mã khác!")
            self.attributes('-topmost', True)
            return

        try:
            success = self.controller.insert(ma_khoa, ten_khoa, so_dien_thoai, email)
            if success:
                self.attributes('-topmost', False)
                messagebox.showinfo("Thành công", "Đã lưu thông tin khoa!")
                self.parent.load_data()
                self.destroy()
            else:
                raise ValueError("Không thể thêm khoa, có thể bị sai số điện thoại hoặc sai email!")
        except Exception as e:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", f"Lỗi khi thêm khoa: {str(e)}")
