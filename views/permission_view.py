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
        self.configure(fg_color="#ffffff")
        self.pack(fill="both", expand=True)
        
        # --- Header Frame ---
        header_frame = ctk.CTkFrame(self, fg_color="#646765", height=100)
        header_frame.pack(fill="x")
        label_title = ctk.CTkLabel(
            header_frame, text="Quản Lý Phân Quyền",
            font=("Verdana", 18, "bold"), text_color="#ffffff"
        )
        label_title.pack(pady=20)
        
        # --- Các nút thao tác ---
        btn_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        btn_frame.pack(pady=20, padx=20)
        
        btn_add_role = ctk.CTkButton(
            btn_frame, text="Thêm Vai Trò", font=("Verdana", 13, "bold"), fg_color="#4CAF50",
            text_color="white", command=self.open_add_role_form, width=120
        )
        btn_add_role.grid(row=0, column=0, padx=5)
        
        btn_edit_role = ctk.CTkButton(
            btn_frame, text="Sửa Vai Trò", font=("Verdana", 13, "bold"), fg_color="#fbbc0e",
            text_color="white", command=self.open_edit_role_form, width=120
        )
        btn_edit_role.grid(row=0, column=1, padx=5)
        
        btn_delete_role = ctk.CTkButton(
            btn_frame, text="Xóa Vai Trò", font=("Verdana", 13, "bold"), fg_color="#F44336",
            text_color="white", command=self.delete_role, width=120
        )
        btn_delete_role.grid(row=0, column=2, padx=5)
        
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
            if col in ["Xem", "Thêm", "Sửa", "Xóa"]:
                self.tree.column(col, anchor="center", width=70, minwidth=50, stretch=False)
            else:
                self.tree.column(col, anchor="center", width=180)
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
        """Mở form nhập vai trò & chọn phân quyền (dùng cho thêm)."""
        self.add_window = tk.Toplevel(self)
        self.add_window.title("Thêm Vai Trò Mới")
        self.add_window.geometry("650x550")
        self.add_window.transient(self)
        self.add_window.grab_set()
        self.add_window.focus_force()
        
        # --- Header của form ---
        header_frame = ctk.CTkFrame(self.add_window, fg_color="#646765", height=80)
        header_frame.pack(fill="x")
        label_title = ctk.CTkLabel(
            header_frame, text="Thêm Vai Trò Mới",
            font=("Verdana", 18, "bold"), text_color="white"
        )
        label_title.pack(pady=15)
        
        form_frame = ctk.CTkFrame(self.add_window, fg_color="white")
        form_frame.pack(fill="x", padx=20, pady=10)
        
        # --- Nhập tên vai trò ---
        label_role = ctk.CTkLabel(form_frame, text="Tên Vai Trò:", font=("Verdana", 13, "bold"))
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
        
        # --- Header bảng quyền sử dụng grid ---
        header_perm = ctk.CTkFrame(form_frame, fg_color="#DADADA", height=40)
        header_perm.pack(fill="x", padx=10, pady=(15, 0))
        header_perm.grid_columnconfigure(0, minsize=150)
        for i in range(1, 5):
            header_perm.grid_columnconfigure(i, minsize=60)
        ctk.CTkLabel(header_perm, text="Module", font=("Arial", 12, "bold"),
                     anchor="w").grid(row=0, column=0, padx=10, sticky="nsew")
        for i, col in enumerate(columns, start=1):
            ctk.CTkLabel(header_perm, text=col.upper(), font=("Arial", 12, "bold"),
                         anchor="center").grid(row=0, column=i, padx=10, sticky="nsew")
        
        # --- Các dòng dữ liệu (mỗi dòng cho một module) ---
        for module in modules:
            row_frame = ctk.CTkFrame(form_frame, fg_color="lightgray")
            row_frame.pack(fill="x", padx=10, pady=3)
            row_frame.grid_columnconfigure(0, minsize=150)
            for i in range(1, 5):
                row_frame.grid_columnconfigure(i, minsize=60)
            ctk.CTkLabel(row_frame, text=module, font=("Arial", 12),
                         anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
            for i, col in enumerate(columns, start=1):
                chk = tk.Checkbutton(row_frame, variable=self.checkboxes[module][col],
                                     text="", width=2)
                chk.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
        
        # --- Nút hành động ---
        btn_frame = ctk.CTkFrame(form_frame, fg_color="white")
        btn_frame.pack(fill="x", pady=15)
        btn_add = ctk.CTkButton(btn_frame, fg_color="#4CAF50", text="Thêm",
                                text_color="white", command=self.add_role,
                                width=150, height=40)
        btn_cancel = ctk.CTkButton(btn_frame, fg_color="#F44336", text="Hủy",
                                   text_color="white", command=self.add_window.destroy,
                                   width=150, height=40)
        btn_add.pack(side="right", expand=True, padx=10)
        btn_cancel.pack(side="left", expand=True, padx=10)
    
    def add_role(self):
        """Gửi dữ liệu vai trò và phân quyền lên Controller để lưu vào database."""
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
        
    def open_edit_role_form(self):
        """Mở form sửa vai trò sử dụng giao diện giống form thêm vai trò (các checkbox được pre-populate)."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn vai trò cần sửa", parent=self)
            return
        values = self.tree.item(selected_item[0], "values")
        if not values:
            messagebox.showwarning("Cảnh báo", "Dữ liệu không hợp lệ!", parent=self)
            return
        # Giả sử cột đầu tiên chứa tên vai trò
        old_role = values[0]
        # Lấy chi tiết vai trò (bao gồm cấu hình quyền trên các module) từ controller.
        # Phương thức này cần được hiện thực trong PermissionController (ví dụ: get_role_details)
        role_details = self.controller.get_role_details(old_role)
        if not role_details:
            messagebox.showwarning("Cảnh báo", "Không tìm thấy dữ liệu cho vai trò này!", parent=self)
            return
        
        self.edit_window = tk.Toplevel(self)
        self.edit_window.title("Sửa Vai Trò")
        self.edit_window.geometry("650x550")
        self.edit_window.transient(self)
        self.edit_window.grab_set()
        self.edit_window.focus_force()
        
        # --- Header của form ---
        header_frame = ctk.CTkFrame(self.edit_window, fg_color="#646765", height=80)
        header_frame.pack(fill="x")
        label_title = ctk.CTkLabel(
            header_frame, text="Sửa Vai Trò",
            font=("Verdana", 18, "bold"), text_color="white"
        )
        label_title.pack(pady=15)
        
        form_frame = ctk.CTkFrame(self.edit_window, fg_color="white")
        form_frame.pack(fill="x", padx=20, pady=10)
        
        # --- Nhập tên vai trò (pre-populate) ---
        label_role = ctk.CTkLabel(form_frame, text="Tên Vai Trò:", font=("Verdana", 13, "bold"))
        label_role.pack(pady=5)
        self.entry_vai_tro = ctk.CTkEntry(form_frame, width=250)
        self.entry_vai_tro.pack(pady=5)
        self.entry_vai_tro.insert(0, old_role)
        
        # --- Tạo danh sách checkbox phân quyền (pre-populate theo role_details) ---
        columns = ["xem", "them", "sua", "xoa"]
        modules = ["mon_hoc", "lop_hoc", "giang_vien", "khoa", "diem", "sinh_vien"]
        # Sử dụng một dict riêng cho form sửa
        self.edit_checkboxes = defaultdict(lambda: {col: tk.BooleanVar() for col in columns})
        for module in modules:
            perms = role_details.get(module, {})  # role_details là dict có key là module
            for col in columns:
                var = tk.BooleanVar()
                # Pre-populate: nếu dữ liệu tồn tại và có giá trị truthy, set là True
                var.set(bool(perms.get(col, 0)))
                self.edit_checkboxes[module][col] = var
        
        # --- Header bảng quyền sử dụng grid ---
        header_perm = ctk.CTkFrame(form_frame, fg_color="#DADADA", height=40)
        header_perm.pack(fill="x", padx=10, pady=(15, 0))
        header_perm.grid_columnconfigure(0, minsize=150)
        for i in range(1, 5):
            header_perm.grid_columnconfigure(i, minsize=60)
        ctk.CTkLabel(header_perm, text="Module", font=("Arial", 12, "bold"),
                     anchor="w").grid(row=0, column=0, padx=10, sticky="nsew")
        for i, col in enumerate(columns, start=1):
            ctk.CTkLabel(header_perm, text=col.upper(), font=("Arial", 12, "bold"),
                         anchor="center").grid(row=0, column=i, padx=10, sticky="nsew")
        
        # --- Các dòng dữ liệu (mỗi dòng cho một module) ---
        for module in modules:
            row_frame = ctk.CTkFrame(form_frame, fg_color="lightgray")
            row_frame.pack(fill="x", padx=10, pady=3)
            row_frame.grid_columnconfigure(0, minsize=150)
            for i in range(1, 5):
                row_frame.grid_columnconfigure(i, minsize=60)
            ctk.CTkLabel(row_frame, text=module, font=("Arial", 12),
                         anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
            for i, col in enumerate(columns, start=1):
                chk = tk.Checkbutton(row_frame, variable=self.edit_checkboxes[module][col],
                                     text="", width=2)
                chk.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
        
        # --- Nút hành động ---
        btn_frame = ctk.CTkFrame(form_frame, fg_color="white")
        btn_frame.pack(fill="x", pady=15)
        btn_save = ctk.CTkButton(btn_frame, fg_color="#4CAF50", text="Lưu",
                                 text_color="white", command=lambda: self.submit_edit_role(old_role),
                                 width=150, height=40)
        btn_cancel = ctk.CTkButton(btn_frame, fg_color="#F44336", text="Hủy",
                                   text_color="white", command=self.edit_window.destroy,
                                   width=150, height=40)
        btn_save.pack(side="right", expand=True, padx=10)
        btn_cancel.pack(side="left", expand=True, padx=10)
    
    def submit_edit_role(self, old_role):
        """Xử lý lưu lại thông tin chỉnh sửa vai trò."""
        new_role = self.entry_vai_tro.get().strip()
        if not new_role:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên vai trò!", parent=self.edit_window)
            return
        
        # Thu thập cấu hình quyền từ các checkbox
        updated_permissions = {}
        for module, perms in self.edit_checkboxes.items():
            updated_permissions[module] = {col: perms[col].get() for col in ["xem", "them", "sua", "xoa"]}
        
        try:
            # Gọi method update_role ở controller.
            # nhận vào (old_role, new_role, updated_permissions)
            self.controller.update_role(old_role, new_role, updated_permissions)
            messagebox.showinfo("Thành công", "Vai trò đã được cập nhật!", parent=self.edit_window)
            self.edit_window.destroy()
            self.load_roles()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật vai trò: {str(e)}", parent=self.edit_window)
    
    def delete_role(self):
        """Xóa vai trò dựa trên lựa chọn trong treeview (với kiểm tra ràng buộc)."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn vai trò cần xóa!", parent=self)
            return
        values = self.tree.item(selected[0], "values")
        if not values:
            messagebox.showwarning("Cảnh báo", "Dữ liệu không hợp lệ!", parent=self)
            return
        role_name = values[0]
        # Không cho phép xóa vai trò admin hoặc giảng viên
        if role_name.lower() in ["admin", "giang_vien"]:
            messagebox.showwarning("Cảnh báo", "Không thể xóa vai trò admin hoặc giảng viên!", parent=self)
            return
        # Kiểm tra xem có tài khoản nào đang sử dụng vai trò này hay không
        if self.controller.is_role_used(role_name):
            messagebox.showwarning("Cảnh báo", "Vai trò này đang được sử dụng. Vui lòng xóa tài khoản có vai trò này trước!", parent=self)
            return
        # Xác nhận xóa
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa vai trò {role_name}?", parent=self):
            return
        try:
            self.controller.delete_role(role_name)
            messagebox.showinfo("Thành công", f"Vai trò {role_name} đã được xóa!", parent=self)
            self.load_roles()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa vai trò: {str(e)}", parent=self)

