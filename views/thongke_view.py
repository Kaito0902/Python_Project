import customtkinter as ctk
from tkinter import ttk
from controllers.thongke_controller import ThongKeController

class ThongKeView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f5f5f5")
        self.ctrl = ThongKeController()
        self._create_ui()
        self.load_data()

    def _create_ui(self):
        ctk.CTkLabel(self, text="Thống Kê Điểm Theo Năm", font=("Verdana",16,"bold")).pack(pady=10)
        chart = ctk.CTkFrame(self, fg_color="#ffffff", height=200)
        chart.pack(fill="x", padx=20, pady=(0,10))
        ctk.CTkLabel(chart, text="[Biểu đồ năm]", text_color="gray").pack(expand=True)
        cols = ("Năm","Sĩ số","Đậu","Rớt","Điểm TB")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20)

    def load_data(self):
        for r in self.ctrl.get_stats_year():
            self.tree.insert("","end", values=(r['nam'],r['si_so'],r['dau'],r['rot'],r['diem_tb']))