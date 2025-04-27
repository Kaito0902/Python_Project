import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class SuaCotDiem(ctk.CTkToplevel):
    def __init__(self, parent, tree, controller, callback=None):
        super().__init__(parent)
        self.tree = tree
        self.controller = controller
        self.callback = callback
        self.title("Sửa Cột Điểm")
        self.geometry("500x300")
        self.configure(bg="#f5f5f5")

        self.attributes('-topmost', True)

        self.create_input_row("Tên Cột Điểm:", "ten_cot_diem_entry")
        self.create_trong_so_row("Trọng số:", "trong_so_option")

        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Sửa", command=self.sua_cot_diem).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Hủy bỏ", command=self.destroy).pack(side="right", padx=10, pady=5)

        self.load_selected_item()

    def create_input_row(self, label_text, entry_attr):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(pady=5, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=label_text, width=80, anchor="w")
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(side="left", padx=10)

        setattr(self, entry_attr, entry)

    def create_trong_so_row(self, label_text, option_attr):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(pady=5, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=label_text, width=80, anchor="w")
        label.pack(side="left", padx=10)

        options = [f"{i}%" for i in range(10, 110, 10)]
        option_menu = ctk.CTkOptionMenu(frame, values=options)
        option_menu.set("10%")
        option_menu.pack(side="left", padx=10)

        setattr(self, option_attr, option_menu)

    def load_selected_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
            if values:
                # Giả sử cấu trúc treeview là: Mã cột điểm, Tên cột điểm, Trọng số
                self.ten_cot_diem_entry.insert(0, values[2])
                self.trong_so_option.set(values[3])

    def sua_cot_diem(self):
        ten_cot_diem = self.ten_cot_diem_entry.get().strip()
        trong_so = self.trong_so_option.get().strip()

        if not (ten_cot_diem and trong_so):
            self.attributes('-topmost', False)
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            self.attributes('-topmost', True)
            return

        # Lấy mã cột điểm từ item đã chọn trong treeview
        selected_item = self.tree.selection()
        if not selected_item:
            self.attributes('-topmost', False)
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột điểm cần sửa!")
            self.attributes('-topmost', True)
            return

        try:
            # Cập nhật thông tin cột điểm trong treeview
            self.tree.item(selected_item, values=("", "", ten_cot_diem, trong_so))

            self.attributes('-topmost', False)
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin cột điểm!")
            if self.callback:
                self.callback(ten_cot_diem, trong_so)
            self.destroy()

        except Exception as e:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật cột điểm: {str(e)}")

