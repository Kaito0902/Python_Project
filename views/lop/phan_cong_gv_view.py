import customtkinter as ctk
from tkinter import messagebox, ttk
from controllers.lop_controller import LopController
from controllers.giang_vien_controller import GiangVienController

class PhanCongGvView(ctk.CTkToplevel):
    def __init__(self, parent, lop_controller: LopController, gv_controller : GiangVienController , ma_lop):
        super().__init__(parent)
        self.parent = parent
        self.lop_controller = lop_controller
        self.gv_controller = gv_controller
        self.ma_lop = ma_lop
        self.title("Phân công Giảng Viên giảng dạy")
        self.geometry("600x450")
        self.configure(bg="#ffffff")
        self.center_window(600, 450)

        self.attributes('-topmost', True)

        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(frame, text="Vui lòng chọn Giảng Viên giảng dạy ", font=("Arial", 14, "bold"), width=80, anchor="w").pack(padx=10)

        style = ttk.Style()
        style.configure("Treeview", background="#f5f5f5", foreground="black", rowheight=30, fieldbackground="lightgray")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#3084ee", foreground="black")
        style.map("Treeview", background=[("selected", "#4CAF50")], foreground=[("selected", "white")])

        tree_frame = ctk.CTkFrame(self, fg_color="white")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("STT","Mã GV", "Họ và Tên"), show="headings", style="Treeview", selectmode="extended")

        self.tree.heading("STT", text="STT")
        self.tree.heading("Mã GV", text="Mã GV")
        self.tree.heading("Họ và Tên", text="Họ và Tên")

        self.tree.column("STT", width=40, anchor="center")
        self.tree.column("Mã GV", width=100, anchor="center")
        self.tree.column("Họ và Tên", width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.update_treeview()

        button_frame = ctk.CTkFrame(self, fg_color="white")
        button_frame.pack(pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Hủy", font=("Verdana", 14, "bold"), text_color="#7b7d7d", fg_color="white", border_color="#3084ee", border_width=1, hover_color="#d5ebf5", command=self.destroy).pack(side="left", padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Lưu", font=("Verdana", 14, "bold"), command=self.xac_nhan).pack(side="right", padx=10, pady=5)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 40 
        self.geometry(f"{width}x{height}+{x}+{y}")

    def xac_nhan(self):
        selected_items = self.tree.selection() 

        if not selected_items:
            self.attributes('-topmost', False)
            messagebox.showwarning("Thông báo", "Vui lòng chọn Giảng viên!")
            self.attributes('-topmost', True)
            return
            
        for item in selected_items:
            values = self.tree.item(item, "values") 
            ma_gv = values[1]
            ten_gv = values[2]

        success = self.lop_controller.phan_cong_gv(self.ma_lop, ma_gv)
        self.attributes('-topmost', False)
        if success:
            messagebox.showinfo("Thành công", f"Đã phân công giảng viên {ten_gv} cho lớp {self.ma_lop}.")
            self.parent.thong_tin_lop(self.ma_lop)
            self.parent.update_treeview()
            self.destroy()
 
        else:
            messagebox.showerror("Lỗi", "Không thể phân công giảng viên!")
            self.attributes('-topmost', True)

    def update_treeview(self, data=None):
        self.tree.delete(*self.tree.get_children())

        if data is not None:
            gv_list = data
        else: gv_list = self.lop_controller.danh_sach_gv(self.ma_lop)
            
        if not gv_list:
            messagebox.showinfo("Thông báo", "Không có dữ liệu Giảng viên!")
            return
        
        for index, sv in enumerate(gv_list, start=1):
            ma_gv = sv.get("ma_gv", "")
            ho_ten = sv.get("ho_ten", "")

            self.tree.insert("", "end", values=(index, ma_gv, ho_ten))

