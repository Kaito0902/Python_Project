import sys
import re
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from customtkinter import CTkComboBox
from tkinter import ttk, messagebox
from PIL import Image
import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, messagebox
from tkinter import simpledialog
from controllers.account_controller import AccountController
from models.database import Database 
from session import current_user 
from controllers.log_controller import LogController


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AccountManager(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="white")
        self.controller = AccountController()
        self.log_controller = LogController()
        self.parent = parent
        self.pack(fill="both", expand=True)
        self.db = Database()
        self.all_accounts = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):

        header_frame = ctk.CTkFrame(self, fg_color="#646765", height=100)
        header_frame.pack(fill="x")

        label_title = ctk.CTkLabel(header_frame, text="Quản Lý Tài Khoản", font=("Verdana", 18, "bold"),
                                   text_color="#ffffff")
        label_title.pack(pady=20)

        search_frame = ctk.CTkFrame(self, fg_color="white")
        search_frame.pack(pady=5, padx=20, fill="x")

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm...", width=200)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", self.search_user)

        icon = ctk.CTkImage(
            Image.open(r"D:\Downloads\sever nro\icon\Python_Project-master1\resources\images\search.png").resize(
                (20, 20)), size=(20, 20))
        btn_search = ctk.CTkButton(search_frame, image=icon, text="", width=20, height=20, fg_color="#ffffff",
                                   hover_color="#ffffff", command=None)
        btn_search.pack(side="left", pady=20)
        

        btn_frame = ctk.CTkFrame(search_frame, fg_color="white")
        btn_frame.pack(side="right")

        # lưu tham chiếu các nút để phân quyền
        self.btn_add = ctk.CTkButton(btn_frame, fg_color="#4CAF50", text="Thêm", text_color="white", command=self.add_user, width=80)
        self.btn_edit = ctk.CTkButton(btn_frame, fg_color="#fbbc0e", text="Sửa", text_color="white", command=self.edit_user, width=80)
        self.btn_delete = ctk.CTkButton(btn_frame, fg_color="#F44336", text="Xóa", text_color="white", command=self.delete_user, width=80)
        self.btn_logs = ctk.CTkButton(btn_frame, fg_color="#904fd2", text="Xem nhật ký", text_color="white", command=self.view_logs, width=80)
        for w in (self.btn_add, self.btn_edit, self.btn_delete, self.btn_logs):
            w.pack(side="left", padx=5)
        

        style = ttk.Style()
        style.configure("Treeview", background="#f5f5f5", foreground="black", rowheight=30, fieldbackground="lightgray")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#3084ee", foreground="black")
        style.map("Treeview", background=[("selected", "#4CAF50")], foreground=[("selected", "white")])

        columns = ("Mã Người Dùng", "Username", "Password", "Vai trò")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", style="Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

    

    def load_data(self):
        try:
            self.tree.delete(*self.tree.get_children())  # Xóa toàn bộ Treeview
            self.all_accounts = self.controller.get_all_accounts()  
            print("Dữ liệu tài khoản:", self.all_accounts)  

            for acc in self.all_accounts:
                self.tree.insert("", "end", values=(acc['ma_nguoi_dung'], acc['username'], acc['password'], acc['vai_tro'])) 

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}", parent=self)
            

    def search_user(self, event=None):
        search_text = self.search_entry.get().lower()
        self.tree.delete(*self.tree.get_children())  # Xóa toàn bộ danh sách cũ trong Treeview

        for acc in self.all_accounts:  # Duyệt qua danh sách lưu sẵn
             if (search_text in acc['ma_nguoi_dung'].lower()):
                self.tree.insert("", "end", values=(acc['ma_nguoi_dung'], acc['username'], acc['password'], acc['vai_tro']))
                

    def add_user(self):
        if current_user.get("vai_tro_id") != "admin":
            messagebox.showwarning("Cảnh báo", "Bạn không có quyền thêm người dùng!", parent=self)
            return

        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Thêm người dùng")
        self.add_window.geometry("350x250")
        self.add_window.resizable(False, False)

        # Căn giữa cửa sổ con dựa trên cửa sổ chính
        self.update_idletasks()  # Cập nhật kích thước của cửa sổ chính
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        main_width = self.winfo_width()
        main_height = self.winfo_height()
        win_width = 350
        win_height = 250
        x_pos = main_x + (main_width - win_width) // 2
        y_pos = main_y + (main_height - win_height) // 2
        self.add_window.geometry(f"{win_width}x{win_height}+{x_pos}+{y_pos}")

        # Đảm bảo cửa sổ con luôn nằm trên cửa sổ chính
        self.add_window.transient(self)
        self.add_window.grab_set()
        self.add_window.focus_force()

        danh_sach_vai_tro = self.controller.lay_danh_sach_vai_tro()

        # Sử dụng CTkFrame để chứa các ô nhập liệu
        input_frame = ctk.CTkFrame(self.add_window, fg_color="white")
        input_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Mã người dùng
        label_ma = ctk.CTkLabel(input_frame, text="Mã người dùng:", anchor="w")
        label_ma.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ma_nguoi_dung_entry = ctk.CTkEntry(input_frame, width=200)
        ma_nguoi_dung_entry.grid(row=0, column=1, padx=10, pady=5)

        # Username
        label_username = ctk.CTkLabel(input_frame, text="Username:", anchor="w")
        label_username.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        username_entry = ctk.CTkEntry(input_frame, width=200)
        username_entry.grid(row=1, column=1, padx=10, pady=5)

        # Password
        label_password = ctk.CTkLabel(input_frame, text="Password:", anchor="w")
        label_password.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        password_entry = ctk.CTkEntry(input_frame, width=200, show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Vai trò
        label_vai_tro = ctk.CTkLabel(input_frame, text="Vai trò:", anchor="w")
        label_vai_tro.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        vai_tro_combobox = ctk.CTkComboBox(input_frame, values=danh_sach_vai_tro, width=200)
        if danh_sach_vai_tro:
            vai_tro_combobox.set(danh_sach_vai_tro[0])
        else:
            vai_tro_combobox.set("Chưa có vai trò")
        vai_tro_combobox.grid(row=3, column=1, padx=10, pady=5)

        # Khung chứa các nút hành động
        btn_frame = ctk.CTkFrame(self.add_window, fg_color="white")
        btn_frame.pack(pady=10)

        def submit():
            ma = ma_nguoi_dung_entry.get().strip()
            uname = username_entry.get().strip()
            pword = password_entry.get().strip()
            vai_tro = vai_tro_combobox.get().strip()
            # Giả sử hàm validate_user_input đã được định nghĩa và kiểm tra các điều kiện hợp lệ
            if not validate_user_input(ma, uname, pword, vai_tro, self.add_window):
                return
            if not (ma and uname and pword and vai_tro):
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!", parent=self.add_window)
                return
            try:
                self.controller.add_account(ma, uname, pword, vai_tro)
                current_ma = current_user.get("ma_nguoi_dung", None)
                if not current_ma or current_ma == "unknown":
                    print("❌ Không thể ghi nhật ký! `ma_nguoi_dung` không hợp lệ.")
                else:
                    self.log_controller.ghi_nhat_ky(current_ma, f"Thêm người dùng: {uname}")
                messagebox.showinfo("Thành công", "Người dùng đã được thêm thành công!", parent=self.add_window)
                self.add_window.destroy()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm người dùng: {e}", parent=self.add_window)

        btn_add = ctk.CTkButton(btn_frame, text="Thêm", fg_color="#4CAF50",
                                text_color="white", command=submit)
        btn_add.pack(side="left", padx=10)
        btn_cancel = ctk.CTkButton(btn_frame, text="Hủy bỏ", fg_color="#F44336",
                                text_color="white", command=self.add_window.destroy)
        btn_cancel.pack(side="right", padx=10)
 
    def edit_user(self):
        if current_user.get("vai_tro_id") != "admin":
            messagebox.showwarning("Cảnh báo", "Bạn không có quyền sửa người dùng!", parent=self)
            return

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một người dùng để sửa", parent=self)
            return

        values = self.tree.item(selected_item[0])['values']
        if not values:
            messagebox.showwarning("Cảnh báo", "Dữ liệu không hợp lệ!", parent=self)
            return

        # Giả sử thứ tự các cột: Mã người dùng, Username, Password, Vai trò
        ma_nguoi_dung_value = values[0]
        username_value = values[1]
        password_value = values[2]
        vai_tro_value = values[3]

        # Tạo cửa sổ con sử dụng CTkToplevel
        self.edit_window = ctk.CTkToplevel(self)
        self.edit_window.title("Chỉnh sửa người dùng")
        self.edit_window.geometry("350x250")
        self.edit_window.resizable(False, False)

        # Căn giữa cửa sổ con dựa trên cửa sổ chính
        self.update_idletasks()  # Cập nhật kích thước của cửa sổ chính
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        main_width = self.winfo_width()
        main_height = self.winfo_height()
        win_width, win_height = 350, 250
        x_pos = main_x + (main_width // 2) - (win_width // 2)
        y_pos = main_y + (main_height // 2) - (win_height // 2)
        self.edit_window.geometry(f"{win_width}x{win_height}+{x_pos}+{y_pos}")

        self.edit_window.transient(self)
        self.edit_window.grab_set()
        self.edit_window.focus_force()

        # Lấy danh sách vai trò để hiển thị trong combobox
        danh_sach_vai_tro = self.controller.lay_danh_sach_vai_tro()

        # Tạo khung chứa các ô nhập liệu
        input_frame = ctk.CTkFrame(self.edit_window, fg_color="white")
        input_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Hàng 1: Mã người dùng (không editable)
        label_ma = ctk.CTkLabel(input_frame, text="Mã người dùng:", anchor="w")
        label_ma.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ma_entry = ctk.CTkEntry(input_frame, width=200)
        ma_entry.grid(row=0, column=1, padx=10, pady=5)
        ma_entry.insert(0, ma_nguoi_dung_value)
        ma_entry.configure(state="disabled")

        # Hàng 2: Username
        label_username = ctk.CTkLabel(input_frame, text="Username:", anchor="w")
        label_username.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        username_entry = ctk.CTkEntry(input_frame, width=200)
        username_entry.grid(row=1, column=1, padx=10, pady=5)
        username_entry.insert(0, username_value)

        # Hàng 3: Password
        label_password = ctk.CTkLabel(input_frame, text="Password:", anchor="w")
        label_password.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        password_entry = ctk.CTkEntry(input_frame, width=200, show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=5)
        password_entry.insert(0, password_value)

        # Hàng 4: Vai trò - sử dụng CTkComboBox
        label_vaitro = ctk.CTkLabel(input_frame, text="Vai trò:", anchor="w")
        label_vaitro.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        vai_tro_combobox = ctk.CTkComboBox(input_frame, values=danh_sach_vai_tro, width=200)
        vai_tro_combobox.grid(row=3, column=1, padx=10, pady=5)
        if danh_sach_vai_tro:
            vai_tro_combobox.set(vai_tro_value)
        else:
            vai_tro_combobox.set("Chưa có vai trò")

        # Khung chứa các nút hành động
        btn_frame = ctk.CTkFrame(self.edit_window, fg_color="white")
        btn_frame.pack(pady=10)

        def submit_edit():
            new_username = username_entry.get().strip()
            new_password = password_entry.get().strip()
            new_vai_tro = vai_tro_combobox.get().strip()

            # Hàm validate_user_update được dùng để kiểm tra dữ liệu đầu vào (giữ nguyên logic)
            if not validate_user_update(new_username, new_password, new_vai_tro, self.edit_window):
                return

            if not (new_username and new_password and new_vai_tro):
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!", parent=self.edit_window)
                return

            try:
                self.controller.update_account(ma_nguoi_dung_value, new_username, new_password, new_vai_tro)
                self.log_controller.ghi_nhat_ky(current_user.get("ma_nguoi_dung", "unknown"),
                                                f"Sửa người dùng: {new_username}")
                messagebox.showinfo("Thành công", "Thông tin người dùng đã được cập nhật!", parent=self.edit_window)
                self.edit_window.destroy()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật: {e}", parent=self.edit_window)

        btn_save = ctk.CTkButton(btn_frame, text="Lưu", command=submit_edit,
                                width=150, fg_color="#4CAF50", text_color="white")
        btn_save.pack(side="left", padx=10)
        btn_cancel = ctk.CTkButton(btn_frame, text="Hủy bỏ", command=self.edit_window.destroy,
                                width=150, fg_color="#F44336", text_color="white")
        btn_cancel.pack(side="right", padx=10)

        self.edit_window.lift()
        self.edit_window.attributes('-topmost', True)

    def delete_user(self):
        if current_user.get("vai_tro_id") != "admin":
            messagebox.showwarning("Cảnh báo", "Bạn không có quyền xóa người dùng!", parent=self)
            return
        
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một người dùng để xóa",parent=self)
            return

        user_id = self.tree.item(selected_item)['values'][0]
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa người dùng ID {user_id}?",parent=self)

        if confirm:
            try:
                self.controller.delete_account(user_id)
                self.log_controller.ghi_nhat_ky(current_user.get("ma_nguoi_dung", "unknown"),f"Xóa người dùng ID: {user_id}")
                self.load_data()
                messagebox.showinfo("Thành công", "Người dùng đã bị xóa!",parent=self)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa người dùng: {e}",parent=self)


    def view_logs(self):
        # Tạo cửa sổ con
        self.log_window = tk.Toplevel(self)
        self.log_window.title("Nhật ký hệ thống")
        # Cho phép phóng to/thu nhỏ
        self.log_window.resizable(True, True)

        # Căn giữa cửa sổ con dựa trên cửa sổ chính
        self.update_idletasks()
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        main_w = self.winfo_width()
        main_h = self.winfo_height()
        # Mở cửa sổ với kích thước lớn hơn
        w, h = 900, 600
        x = main_x + (main_w - w) // 2
        y = main_y + (main_h - h) // 2
        self.log_window.geometry(f"{w}x{h}+{x}+{y}")

        self.log_window.transient(self)
        self.log_window.grab_set()
        self.log_window.focus_set()

        # Khung chính
        frame = ctk.CTkFrame(self.log_window, corner_radius=10, fg_color="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="NHẬT KÝ HỆ THỐNG", font=("Arial", 16, "bold")).pack(pady=(0,10))

        # Container cho Treeview và Scrollbar
        container = tk.Frame(frame)
        container.pack(fill="both", expand=True)

        # Scrollbar dọc
        v_scroll = ttk.Scrollbar(container, orient="vertical")
        v_scroll.pack(side="right", fill="y")

        # Scrollbar ngang
        h_scroll = ttk.Scrollbar(container, orient="horizontal")
        h_scroll.pack(side="bottom", fill="x")

        # Treeview để hiển thị log, liên kết với scrollbars
        cols = ("ID", "Mã người dùng", "Hành động", "Thời gian")
        tv = ttk.Treeview(container, columns=cols, show="headings",
                        yscrollcommand=v_scroll.set,
                        xscrollcommand=h_scroll.set)
        for c in cols:
            tv.heading(c, text=c)
            tv.column(c, anchor="center", width=200)  # bạn có thể chỉnh width theo ý thích
        tv.pack(fill="both", expand=True)

        v_scroll.config(command=tv.yview)
        h_scroll.config(command=tv.xview)

        # Đổ dữ liệu
        logs = self.log_controller.lay_nhat_ky()
        for log in logs:
            tv.insert("", "end", values=(
                log["id"], log["ma_nguoi_dung"], log["hanh_dong"], log["thoi_gian"]
            ))

        # Nút Đóng
        btn_close = ctk.CTkButton(frame, text="Đóng", command=self.log_window.destroy, width=80)
        btn_close.pack(pady=(10,0))




def validate_user_input(ma, username, password, vai_tro, parent_window):
    """
    Kiểm tra đầu vào: Không để rỗng và chỉ cho phép chữ, số, dấu gạch dưới.
    """
    if not (ma and username and password and vai_tro):
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!", parent=parent_window)
        return False
    pattern = r'^[A-Za-z0-9_]+$'
    
    if not re.match(pattern, ma):
        messagebox.showwarning("Cảnh báo", "Mã người dùng chỉ cho phép chữ, số và dấu gạch dưới!", parent=parent_window)
        return False
    if not re.match(pattern, username):
        messagebox.showwarning("Cảnh báo", "Username chỉ cho phép chữ, số và dấu gạch dưới!", parent=parent_window)
        return False
    if not re.match(pattern, vai_tro):
        messagebox.showwarning("Cảnh báo", "Vai trò chỉ cho phép chữ, số và dấu gạch dưới!", parent=parent_window)
        return False
    return True

def validate_user_update(username, password, vai_tro, parent_window):
    if not (username and password and vai_tro):
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!", parent=parent_window)
        return False
    pattern = r'^[A-Za-z0-9_]+$'
    
    if not re.match(pattern, username):
        messagebox.showwarning("Cảnh báo", "Username chỉ cho phép chữ, số và dấu gạch dưới!", parent=parent_window)
        return False
    if not re.match(pattern, vai_tro):
        messagebox.showwarning("Cảnh báo", "Vai trò chỉ cho phép chữ, số và dấu gạch dưới!", parent=parent_window)
        return False
    return True


#if __name__ == "__main__":
    # Giả sử người dùng đã đăng nhập với vai trò admin
    current_user.update({"ma_nguoi_dung": "admin", "username": "admin", "vai_tro": "giang_vien"})
    
    # Tạo cửa sổ chính
    root = ctk.CTk()
    root.title("Quản Lý Tài Khoản")
    root.geometry("1000x600")
    
    # Tạo frame chính và đặt vào cửa sổ
    app = AccountManager(root)
    
    # Chạy ứng dụng
    root.mainloop()

