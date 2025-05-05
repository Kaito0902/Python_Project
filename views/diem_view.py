# views/diem_view.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from controllers.diem_controller import DiemController

class DiemView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f5f5f5")
        self.ctrl = DiemController()
        self.selected_image = None
        self._create_ui()

    def _create_ui(self):
        header = ctk.CTkFrame(self, fg_color="#646765", height=60)
        header.pack(fill="x")
        ctk.CTkLabel(
            header, text="Nhận Diện Điểm & Thống Kê",
            font=("Verdana",18,"bold"), text_color="white"
        ).pack(pady=10)

        top = ctk.CTkFrame(self, fg_color="#ffffff")
        top.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(
            top, text="Load Ảnh & Lưu",
            fg_color="#3084ee", hover_color="#2a6bcc",
            command=self._load_and_save
        ).pack()

        self.lbl_preview = ctk.CTkLabel(self, text="Chưa chọn ảnh", text_color="gray")
        self.lbl_preview.pack(pady=5)
        self.lbl_res     = ctk.CTkLabel(self, text="")
        self.lbl_res.pack(pady=5)

        mid = ctk.CTkFrame(self, fg_color="#ffffff")
        mid.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(mid, text="Mã môn:", width=80, anchor="w").grid(row=0, column=0, padx=5)
        self.combo = ctk.CTkComboBox(mid, values=[m['ma_mon'] for m in self.ctrl.lay_danh_sach_mon()], width=150)
        self.combo.grid(row=0, column=1, padx=5)

    def _load_and_save(self):
        ma_mon = self.combo.get().strip()
        if not ma_mon:
            messagebox.showwarning("Cảnh báo", "Chưa chọn mã môn!")
            return

        path = filedialog.askopenfilename(filetypes=[("Image files","*.png;*.jpg")])
        if not path:
            return

        # Hiển thị preview ảnh
        img = Image.open(path).resize((200,200))
        photo = ctk.CTkImage(light_image=img, size=(200,200))
        self.lbl_preview.configure(image=photo, text="")
        self.lbl_preview.image = photo

        # Quét và lưu
        try:
            res = self.ctrl.quet_va_luu(path, ma_mon)
        except Exception as e:
            messagebox.showerror("Lỗi lưu điểm", str(e))
            return

        # Hiển thị kết quả chi tiết
        self.lbl_res.configure(
            text=(
                f"MSSV: {res['mssv']}   "
                f"KT: {res['diem_kiem_tra']}   "
                f"CK: {res['diem_cuoi_ky']}   "
                f"TK: {res['diem_tong_ket']}   "
                f"XL: {res['xep_loai']}"
            )
        )
