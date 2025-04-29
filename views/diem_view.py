import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from controllers.diem_controller import DiemController

class DiemView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="#f5f5f5", corner_radius=15)
        self.ctrl = DiemController()
        self.ma_mon = None
        self.duong_dan = None
        self._tao_ui()
        self._nap_mon()

    def _tao_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="#646765", height=60)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Quét Ảnh & Quản lý Điểm", font=("Verdana",18,"bold"), text_color="white").pack(pady=10)

        # Top: chọn ảnh và preview
        top = ctk.CTkFrame(self, fg_color="#ffffff")
        top.pack(fill="x", padx=20, pady=10)
        self.lbl_preview = ctk.CTkLabel(top, text="Chưa chọn ảnh", text_color="gray")
        self.lbl_preview.grid(row=0, column=0, rowspan=2, padx=5)
        ctk.CTkButton(top, text="Chọn Ảnh", fg_color="#3084ee", hover_color="#2a6bcc", command=self._chon_anh).grid(row=0, column=1, padx=10)
        self.lbl_kq_ai = ctk.CTkLabel(top, text="", font=("Arial",14))
        self.lbl_kq_ai.grid(row=1, column=1, sticky="w")

        # Mid: chọn môn và lưu điểm
        mid = ctk.CTkFrame(self, fg_color="#ffffff")
        mid.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(mid, text="Mã môn:", width=80, anchor="w").grid(row=0, column=0, padx=5)
        self.combo = ttk.Combobox(mid, state="readonly", width=25)
        self.combo.grid(row=0, column=1, padx=5)
        ctk.CTkButton(mid, text="Lưu điểm", fg_color="#4CAF50", hover_color="#3e8e41", command=self._luu_diem).grid(row=0, column=2, padx=5)

        # Filter/search
        flt = ctk.CTkFrame(self, fg_color="#ffffff")
        flt.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(flt, text="Tìm MSSV:", width=80, anchor="w").grid(row=0, column=0, padx=5)
        self.search_var = ctk.StringVar()
        self.search_var.trace_add('write', self._loc_danh_sach)
        ctk.CTkEntry(flt, textvariable=self.search_var, width=150).grid(row=0, column=1, padx=5)

        # Treeview
        cols = ("MSSV","KT","CK","TK","Xep loai")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20)

        # Bottom: thống kê và export
        bot = ctk.CTkFrame(self, fg_color="#ffffff")
        bot.pack(fill="x", pady=10)
        self.lbl_stat = ctk.CTkLabel(bot, text="", font=("Arial",13,"italic"))
        self.lbl_stat.pack(side="left", padx=10)
        ctk.CTkButton(bot, text="Export Excel", fg_color="#4CAF50", hover_color="#3e8e41", command=self._export).pack(side="right", padx=10)