import customtkinter as ctk
from tkinter import messagebox
from controllers.mon_hoc_controller import MonHocController
from controllers.khoa_controller import KhoaController

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class SuaMonHocWindow(ctk.CTkToplevel):
    def __init__(self, parent, tree, controller: MonHocController):
        super().__init__(parent)
        self.parent = parent
        self.tree = tree
        self.controller = controller
        self.khoacontroller = KhoaController()
        self.title("Sửa Môn Học")
        self.geometry("500x250")
        self.configure(bg="#f5f5f5")
        self.center_window(500, 250)

        self.attributes('-topmost', True)

        self.create_input_row("Mã Môn Học:", "ma_mh_entry")
        self.create_input_row("Tên Môn Học:", "ten_mh_entry")
        self.create_input_row("Số Tín Chỉ:", "so_tin_chi_entry")
        self.create_khoa_row()

        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Sửa", command=self.sua_mon_hoc).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Hủy bỏ", command=self.destroy).pack(side="right", padx=10, pady=5)

        self.load_khoa_options()
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

        label = ctk.CTkLabel(frame, text=label_text, width=100, anchor="w")
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(side="left", padx=10)

        setattr(self, entry_attr, entry)

    def create_khoa_row(self):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(pady=5, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text="Khoa:", width=100, anchor="w")
        label.pack(side="left", padx=10)

        self.khoa_combobox = ctk.CTkComboBox(frame, width=300, values=[])
        self.khoa_combobox.pack(side="left", padx=10)
        self.khoa_combobox.set("Chọn-")

    def load_khoa_options(self):
        khoa_list = self.khoacontroller.select_all()
        self.khoa_mapping = {khoa["ten_khoa"]: khoa["ma_khoa"] for khoa in khoa_list}
        ten_khoa_list = list(self.khoa_mapping.keys())
        self.khoa_combobox.configure(values=ten_khoa_list)

    def load_selected_item(self):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            if values:
                self.ma_mh_entry.insert(0, values[0])
                self.ten_mh_entry.insert(0, values[1])
                self.so_tin_chi_entry.insert(0, values[2])
                self.khoa_combobox.set(values[3])  # Set tên khoa vào combobox

    def sua_mon_hoc(self):
        ma_mh = self.ma_mh_entry.get().strip()
        ten_mh = self.ten_mh_entry.get().strip()
        so_tin_chi = self.so_tin_chi_entry.get().strip()
        ten_khoa = self.khoa_combobox.get().strip()

        if not (ma_mh and ten_mh and so_tin_chi and ten_khoa):
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            self.attributes('-topmost', True)
            return

        selected_item = self.tree.selection()
        if selected_item:
            old_values = self.tree.item(selected_item[0], "values")
            ma_mh_cu = old_values[0]

            if self.controller.check_exists_for_update(ma_mh, ma_mh_cu):
                self.attributes('-topmost', False)
                messagebox.showerror("Lỗi", "Mã môn học đã tồn tại, vui lòng nhập mã khác!")
                self.attributes('-topmost', True)
                return

        if not so_tin_chi.isdigit() or int(so_tin_chi) <= 0:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Số tín chỉ phải là số nguyên dương!")
            self.attributes('-topmost', True)
            return

        selected_item = self.tree.selection()
        if not selected_item:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Vui lòng chọn môn học cần sửa!")
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
            success = self.controller.update(ma_mh, ten_mh, int(so_tin_chi), ma_khoa)
            if success:
                self.attributes('-topmost', False)
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin môn học!")
                self.parent.load_data()  # reload lại dữ liệu
                self.destroy()
            else:
                raise ValueError("Không thể cập nhật môn học!")
        except Exception as e:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật môn học: {str(e)}")
            self.attributes('-topmost', True)
