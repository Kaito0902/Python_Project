import customtkinter as ctk
from tkinter import ttk
from controllers.thongke_controller import ThongKeController

# Mới: imports cho biểu đồ
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ThongKeView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f5f5f5")
        self.ctrl = ThongKeController()
        self._create_ui()
        self.load_data()

    def _create_ui(self):
        ctk.CTkLabel(self, text="Thống Kê Điểm Theo Năm", font=("Verdana",16,"bold")).pack(pady=10)
        # Lưu frame chart để vẽ biểu đồ
        self.chart_frame = ctk.CTkFrame(self, fg_color="#ffffff", height=200)
        self.chart_frame.pack(fill="x", padx=20, pady=(0,10))

        # Table thống kê
        cols = ("Năm","Sĩ số","Đậu","Rớt","Điểm TB")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20)

    def load_data(self):
        data = self.ctrl.get_stats_year()

        # 1) Vẽ biểu đồ
        years   = [r['nam']     for r in data]
        diem_tb = [r['diem_tb'] for r in data]

        # Tạo figure + plot
        fig, ax = plt.subplots(figsize=(4,2), dpi=100)
        ax.plot(years, diem_tb, marker='o')
        ax.set_title("Điểm TB theo năm")
        ax.set_xlabel("Năm")
        ax.set_ylabel("Điểm TB")
        fig.tight_layout()

        # Hủy canvas cũ (nếu có) rồi vẽ mới
        if hasattr(self, 'chart_canvas'):
            self.chart_canvas.get_tk_widget().destroy()
        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)

        # 2) Load dữ liệu vào treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in data:
            self.tree.insert(
                "", "end",
                values=(
                    r['nam'],
                    r['si_so'],
                    r['dau'],
                    r['rot'],
                    r['diem_tb']
                )
            )
