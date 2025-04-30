import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from controllers.permission_controller import PermissionController
from collections import defaultdict

class PermissionView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = PermissionController()
        self.pack(fill="both", expand=True)
        
        # --- Header Frame ---
        header_frame = ctk.CTkFrame(self, fg_color="#646765", height=100)
        header_frame.pack(fill="x")
        label_title = ctk.CTkLabel(
            header_frame, text="Quản Lý Phân Quyền",
            font=("Verdana", 18, "bold"), text_color="#ffffff"
        )
        label_title.pack(pady=20)
        
        # --- Nút "Thêm Vai Trò" ---
        btn_add_role = ctk.CTkButton(
            self, text="Thêm Vai Trò", fg_color="#4CAF50",
            text_color="white", command=self.open_add_role_form, width=120
        )
        btn_add_role.pack(pady=10, padx=20)
        
        # --- Bảng danh sách quyền (Treeview) ---
        style = ttk.Style()
        style.configure("Treeview", background="#f5f5f5", foreground="black",
                        rowheight=30, fieldbackground="lightgray")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"),
                        background="#3084ee", foreground="black")
        style.map("Treeview", background=[("selected", "#4CAF50")],
                  foreground=[("selected", "white")])
        
        columns = ["Vai trò", "Module", "Xem", "Thêm", "Sửa", "Xóa"]
        self.tree = ttk.Treeview(self, columns=columns, show="headings", style="Treeview")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.load_roles()
    
    def load_roles(self):
        """Lấy dữ liệu quyền từ model và hiển thị trong bảng."""
        self.tree.delete(*self.tree.get_children())
        roles = self.controller.get_permissions()
        if not roles:
            print("Không có dữ liệu quyền hạn để hiển thị.")
            return
        for role in roles:
            self.tree.insert("", "end", values=(
                role["vai_tro"], role["module"], role["xem"],
                role["them"], role["sua"], role["xoa"]
            ))
    
    def open_add_role_form(self):
        """Mở form nhập vai trò & chọn phân quyền."""
        self.add_window = tk.Toplevel(self)
        self.add_window.title("Thêm Vai Trò Mới")
        self.add_window.geometry("650x550")
        
        # --- Header của form ---
        header_frame = ctk.CTkFrame(self.add_window, fg_color="#646765", height=80)
        header_frame.pack(fill="x")
        label_title = ctk.CTkLabel(
            header_frame, text="Thêm Vai Trò Mới", font=("Verdana", 18, "bold"),
            text_color="white"
        )
        label_title.pack(pady=15)
        
        form_frame = ctk.CTkFrame(self.add_window, fg_color="white")
        form_frame.pack(fill="x", padx=20, pady=10)
        
        # --- Nhập tên vai trò ---
        label_role = ctk.CTkLabel(form_frame, text="Tên Vai Trò:", font=("Arial", 12))
        label_role.pack(pady=5)
        self.entry_vai_tro = ctk.CTkEntry(form_frame, width=250)
        self.entry_vai_tro.pack(pady=5)
        
        # --- Tạo danh sách checkbox phân quyền ---
        columns = ["xem", "them", "sua", "xoa"]
        modules = ["mon_hoc", "lop_hoc", "giang_vien", "khoa", "diem", "sinh_vien"]
        self.checkboxes = defaultdict(lambda: {col: tk.BooleanVar() for col in columns})
        for module in modules:
            for col in columns:
                self.checkboxes[module][col] = tk.BooleanVar()
        print("🔍 Kiểm tra self.checkboxes:", self.checkboxes)
        
        # --- Header bảng quyền ---
        header_perm = ctk.CTkFrame(form_frame, fg_color="#DADADA", height=40)
        header_perm.pack(fill="x", padx=10, pady=(15, 0))
        ctk.CTkLabel(header_perm, text="Module", font=("Arial", 12, "bold"),
                     width=120, anchor="w").grid(row=0, column=0, padx=10)
        for i, col in enumerate(columns, start=1):
            ctk.CTkLabel(header_perm, text=col.upper(), font=("Arial", 12, "bold"),
                         width=80).grid(row=0, column=i, padx=10)
        
        # --- Danh sách dòng phân quyền ---
        for module_index, module in enumerate(modules):
            row_frame = ctk.CTkFrame(form_frame, fg_color="lightgray")
            row_frame.pack(fill="x", padx=10, pady=3)
            
            row_frame.grid_columnconfigure(0, weight=2)
            for col_index in range(1, len(columns) + 1):
                row_frame.grid_columnconfigure(col_index, weight=1)
            
            label_module = ctk.CTkLabel(row_frame, text=module, font=("Arial", 12),
                                        width=120, anchor="w")
            label_module.grid(row=0, column=0, padx=10, pady=5)
            
            for col_index, col in enumerate(columns, start=1):
                chk = tk.Checkbutton(row_frame, variable=self.checkboxes[module][col],
                                     text="", width=2)
                chk.grid(row=0, column=col_index, padx=30, pady=5)
        
        # --- Nút hành động ---
        btn_frame = ctk.CTkFrame(form_frame, fg_color="white")
        btn_frame.pack(fill="x", pady=15)
        btn_add = ctk.CTkButton(btn_frame, fg_color="#4CAF50", text="Thêm",
                                text_color="white", command=self.add_role,
                                width=150, height=40)
        btn_cancel = ctk.CTkButton(btn_frame, fg_color="#F44336", text="Hủy",
                                   text_color="white", command=self.add_window.destroy,
                                   width=150, height=40)
        btn_add.pack(side="left", expand=True, padx=10)
        btn_cancel.pack(side="left", expand=True, padx=10)
    
    def add_role(self):
        """Gửi dữ liệu vai trò và phân quyền từ form lên Controller để lưu vào database."""
        ten_vai_tro = self.entry_vai_tro.get().strip()
        if not ten_vai_tro:
            tk.messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên vai trò!")
            return
        
        print("🔍 Debug danh sách checkboxes:", self.checkboxes)
        for module in self.checkboxes:
            if "xem" not in self.checkboxes[module]:
                print(f"❌ Lỗi: Module {module} không có key 'xem'!")
                tk.messagebox.showerror("Lỗi", f"Module {module} không có quyền 'xem'. Vui lòng kiểm tra lại!")
                return
        
        # Nếu vai trò chưa tồn tại, thêm mới vào bảng vai_tro
        if not self.controller.is_role_exists(ten_vai_tro):
            self.controller.add_new_role(ten_vai_tro)
        
        try:
            self.controller.add_permissions(ten_vai_tro, self.checkboxes)
            tk.messagebox.showinfo("Thành công", f"Đã cập nhật vai trò '{ten_vai_tro}' cùng quyền hạn!")
        except Exception as e:
            tk.messagebox.showerror("Lỗi", f"❌ Có lỗi khi thêm quyền: {e}")
            print(f"❌ Lỗi khi thêm quyền: {e}")
            return
        
        self.add_window.destroy()
        self.load_roles()