import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.lop_controller import LopController
from controllers.mon_hoc_controller import MonHocController

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class UpdateLopHoc(ctk.CTkToplevel):
    def __init__(self, parent, controller: LopController, editable: bool = True):
        super().__init__(parent)
        self.parent = parent
        self.editable = editable
        self.controller = controller
        self.mon_hoc_controller = MonHocController()
        self.title("Cập Nhập Thông Tin Lớp Học")
        self.geometry("500x350")
        self.configure(bg="#f5f5f5")
        self.center_window(500, 350)

        self.attributes('-topmost', True)

        self.create_input_row("Mã Lớp Học:", "ma_lop_entry")
        self.create_input_row("Mã Môn Học:", "ma_mon_entry")
        self.create_input_row("Số Lượng SV:", "so_luong_entry")
        self.create_input_row("Học Kỳ:", "hoc_ky_entry")
        self.create_input_row("Năm Học:", "nam_entry")

        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Hủy", font=("Verdana", 14, "bold"), text_color="#7b7d7d", fg_color="white",
                      border_color="#3084ee", border_width=1, hover_color="#d5ebf5", command=self.destroy).pack(
            side="left", padx=10, pady=5)

        self.save_button = ctk.CTkButton(button_frame, text="Lưu", font=("Verdana", 14, "bold"), command=self.xac_nhan)
        self.save_button.pack(side="right", padx=10, pady=5)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 40
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_input_row(self, label_text, entry_attr):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(padx=10, pady=10, fill="x")

        label = ctk.CTkLabel(frame, text=label_text, width=80, anchor="w")
        label.pack(side="left", padx=10)

        if entry_attr == "ma_mon_entry":
            mon_list = [mon_hoc["ma_mon"] for mon_hoc in (self.mon_hoc_controller.select_all())]
            entry = ttk.Combobox(frame, values=mon_list, state="readonly", width=45)
            entry.set("Chọn-")

        else:
            if entry_attr == "hoc_ky_entry":
                entry = ctk.CTkComboBox(frame, values=["1", "2", "3"], state="readonly", width=300)
                entry.set("Chọn-")
            else:
                if entry_attr == "nam_entry":
                    entry = ctk.CTkComboBox(frame, values=self.get_recent_years(4), state="readonly", width=300)
                    entry.set("Chọn-")

                else:
                    entry = ctk.CTkEntry(frame, width=300)

        entry.pack(side="left", padx=10)

        setattr(self, entry_attr, entry)

    def get_recent_years(self, n):
        current_year = datetime.now().year
        return [str(current_year + i) for i in range(n)]

    def xac_nhan(self):
        ma_lop = self.ma_lop_entry.get().strip()
        ma_mon = self.ma_mon_entry.get().strip()
        so_luong = self.so_luong_entry.get().strip()
        hoc_ky = self.hoc_ky_entry.get().strip()
        nam = self.nam_entry.get().strip()

        if not ma_lop or not ma_mon or not so_luong or not hoc_ky or not nam:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            self.attributes('-topmost', True)
            return

        if not so_luong.isdigit() or int(so_luong) <= 0:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", "Số lượng sinh viên phải là số nguyên dương!")
            self.attributes('-topmost', True)
            return

        try:
            success, message = self.controller.update_class(ma_lop, ma_mon, int(so_luong), int(hoc_ky), int(nam))
            self.attributes('-topmost', False)
            if success:
                messagebox.showinfo("Thành công", message)
                self.parent.update_treeview()
                self.destroy()
            else:
                messagebox.showerror("Lỗi", message)
                self.attributes('-topmost', True)
        except Exception as e:
            self.attributes('-topmost', False)
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật lớp học: {str(e)}")
            self.attributes('-topmost', True)

    def set_data(self, ma_lop, ten_mon, ma_mon, so_luong, hoc_ky, nam, ma_gv):
        self.ma_lop_entry.insert(0, ma_lop)
        self.ma_lop_entry.configure(state="disabled")
        self.ma_mon_entry.set(str(ma_mon))
        self.so_luong_entry.insert(0, so_luong)
        self.hoc_ky_entry.set(str(hoc_ky))
        self.nam_entry.set(str(nam))

        if not self.editable:
            self.no_edit()

    def no_edit(self):
        for attr in ("ma_mon_entry", "so_luong_entry", "hoc_ky_entry", "nam_entry"):
            widget = getattr(self, attr)
            widget.configure(state="disabled")
        self.save_button.configure(state="disabled")