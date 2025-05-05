import customtkinter as ctk
from tkinter import messagebox
from controllers.khoa_controller import KhoaController

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class SuaKhoaWindow(ctk.CTkToplevel):
    def __init__(self, parent, tree, controller: KhoaController):
        super().__init__(parent)
        self.parent = parent
        self.tree = tree
        self.controller = controller
        self.title("Sửa Khoa")
        self.geometry("400x220")
        self.configure(bg="#f5f5f5")
        self.center_window(400, 220)

        self.attributes('-topmost', True)

        self.create_input_row("Mã Khoa:", "ma_khoa_entry")
        self.create_input_row("Tên Khoa:", "ten_khoa_entry")
        self.create_input_row("Số điện thoại:", "so_dien_thoai_entry")
        self.create_input_row("Email:", "email_entry")

        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Sửa", command=self.sua_khoa).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Hủy bỏ", command=self.destroy).pack(side="right", padx=10, pady=5)

        self.load_selected_item()

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

    def load_selected_item(self):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            if values:
                self.ma_khoa_entry.insert(0, values[0])
                self.ten_khoa_entry.insert(0, values[1])
                self.so_dien_thoai_entry.insert(0, values[2])
                self.email_entry.insert(0, values[3])

    def sua_khoa(self):
        ma_khoa = self.ma_khoa_entry.get().strip()
        ten_khoa = self.ten_khoa_entry.get().strip()
        so_dien_thoai = self.so_dien_thoai_entry.get().strip()
        email = self.email_entry.get().strip()

        if not (ma_khoa and ten_khoa and so_dien_thoai and email):
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            self.attributes('-topmost', True)
            return

        selected_item = self.tree.selection()
        if selected_item:
            old_values = self.tree.item(selected_item[0], "values")
            ma_khoa_cu = old_values[0]

            if self.controller.check_exists_for_update(ma_khoa, ma_khoa_cu):
                self.attributes('-topmost', False)
                messagebox.showerror("Lỗi", "Mã khoa đã tồn tại, vui lòng nhập mã khác!")
                self.attributes('-topmost', True)
                return

        selected_item = self.tree.selection()
        if not selected_item:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Vui lòng chọn khoa cần sửa!")
            self.attributes('-topmost', True)
            return

        try:
            success = self.controller.update(ma_khoa, ten_khoa, so_dien_thoai, email)
            if success:
                self.attributes('-topmost', False)
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin khoa!")
                self.parent.load_data()  # Reload lại dữ liệu
                self.destroy()
            else:
                raise ValueError("Không thể cập nhật khoa!")
        except Exception as e:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật khoa: {str(e)}")
