import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, messagebox
from tkinter import simpledialog
from controllers.account_controller import AccountController
from models.database import Database  

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AccountManager(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = AccountController()
        self.title("Quản lý Tài Khoản")
        self.geometry("900x500")
        self.configure(bg="#f5f5f5")
        self.attributes('-topmost', True)

        self.db = Database()

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="white")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(main_frame, text="QUẢN LÝ TÀI KHOẢN", font=("Arial", 18, "bold")).pack(pady=10)

        search_frame = ctk.CTkFrame(main_frame, fg_color="white")
        search_frame.pack(pady=5, padx=20, fill="x")

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm...", width=300)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", self.search_user)
        

        btn_frame = ctk.CTkFrame(search_frame, fg_color="white")
        btn_frame.pack(side="right")

        ctk.CTkButton(btn_frame, text="Thêm", command=self.add_user, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Sửa", command=self.edit_user, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Xóa", command=self.delete_user, width=80).pack(side="left", padx=5)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, borderwidth=1, relief="solid", font=("Arial", 14))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        columns = ("Mã Người Dùng", "Username", "Password", "Vai trò")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", style="Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

    def load_data(self):
        try:
            self.all_accounts = self.controller.get_all_accounts()  
            print("Dữ liệu tài khoản:", self.all_accounts)  
            self.search_user()  
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}", parent=self)
            

    def search_user(self, event=None):
        search_text = self.search_entry.get().lower()
        self.tree.delete(*self.tree.get_children())  # Xóa toàn bộ danh sách cũ trong Treeview

        for acc in self.all_accounts:  # Duyệt qua danh sách lưu sẵn
            if (search_text in acc['ma_nguoi_dung'].lower() or
                search_text in acc['username'].lower() or
                search_text in acc['vai_tro'].lower()):
                self.tree.insert("", "end", values=(acc['ma_nguoi_dung'], acc['username'], acc['password'], acc['vai_tro']))
                

    def add_user(self):
        self.add_window = tk.Toplevel(self)
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

        # Tính toán vị trí giữa cửa sổ chính
        x_pos = main_x + (main_width // 2) - (win_width // 2)
        y_pos = main_y + (main_height // 2) - (win_height // 2)
        self.add_window.geometry(f"{win_width}x{win_height}+{x_pos}+{y_pos}")

        self.add_window.transient(self)  # Gắn cửa sổ con vào cửa sổ chính
        self.add_window.grab_set()  # Ngăn không cho thao tác trên cửa sổ chính khi cửa sổ con mở
        self.add_window.focus_set()  # Đặt tiêu điểm vào cửa sổ con

        # Tạo nhãn và ô nhập dữ liệu
        tk.Label(self.add_window, text="Mã người dùng:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ma_nguoi_dung_entry = tk.Entry(self.add_window)
        ma_nguoi_dung_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.add_window, text="Username:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        username_entry = tk.Entry(self.add_window)
        username_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.add_window, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        password_entry = tk.Entry(self.add_window, show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.add_window, text="Vai trò:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        vai_tro_entry = tk.Entry(self.add_window)
        vai_tro_entry.grid(row=3, column=1, padx=10, pady=5)

        # Hàm thêm tài khoản
        def submit():
            ma_nguoi_dung = ma_nguoi_dung_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            vai_tro = vai_tro_entry.get().strip()

            if not (ma_nguoi_dung and username and password and vai_tro):
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!", parent=self.add_window)
                return

            try:
                self.controller.add_account(ma_nguoi_dung, username, password, vai_tro)
                messagebox.showinfo("Thành công", "Người dùng đã được thêm thành công!", parent=self.add_window)
                self.add_window.destroy()  # Đóng form sau khi thêm xong
                self.load_data()  # Load lại dữ liệu
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm người dùng: {e}", parent=self.add_window)

        # Nút Thêm
        tk.Button(self.add_window, text="Thêm", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

 
    def edit_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một người dùng để sửa", parent=self)
            return

        values = self.tree.item(selected_item)['values']
        if not values:
            messagebox.showwarning("Cảnh báo", "Dữ liệu không hợp lệ!", parent=self)
            return

        ma_nguoi_dung_value = values[0]
        username_value = values[1]
        password_value = values[2]
        vai_tro_value = values[3]

        self.edit_window = tk.Toplevel(self)
        self.edit_window.title("Chỉnh sửa người dùng")
        self.edit_window.geometry("350x250")
        self.edit_window.resizable(False, False)

        # Căn giữa cửa sổ chỉnh sửa
        self.update_idletasks()
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        main_width = self.winfo_width()
        main_height = self.winfo_height()

        win_width = 350
        win_height = 250

        x_pos = main_x + (main_width // 2) - (win_width // 2)
        y_pos = main_y + (main_height // 2) - (win_height // 2)

        self.edit_window.geometry(f"{win_width}x{win_height}+{x_pos}+{y_pos}")

        self.edit_window.transient(self)
        self.edit_window.grab_set()
        self.edit_window.focus_set()

        # Tạo nhãn và ô nhập với giá trị ban đầu
        tk.Label(self.edit_window, text="Mã người dùng:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ma_nguoi_dung_Entry = tk.Entry(self.edit_window)
        ma_nguoi_dung_Entry.insert(0, ma_nguoi_dung_value)
        ma_nguoi_dung_Entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.edit_window, text="Username:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        username_entry = tk.Entry(self.edit_window)
        username_entry.insert(0, username_value)
        username_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.edit_window, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        password_entry = tk.Entry(self.edit_window, show="*")
        password_entry.insert(0, password_value)
        password_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.edit_window, text="Vai trò:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        vai_tro_entry = tk.Entry(self.edit_window)
        vai_tro_entry.insert(0, vai_tro_value)
        vai_tro_entry.grid(row=3, column=1, padx=10, pady=5)

        def submit_edit():
            new_ma_nguoi_dung = ma_nguoi_dung_Entry.get().strip()
            new_username = username_entry.get().strip()
            new_password = password_entry.get().strip()
            new_vai_tro = vai_tro_entry.get().strip()

            if not (new_ma_nguoi_dung and new_username and new_password and new_vai_tro):
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!", parent=self.edit_window)
                return

            try:
                self.controller.update_account(new_ma_nguoi_dung, new_username, new_password, new_vai_tro)
                messagebox.showinfo("Thành công", "Thông tin người dùng đã được cập nhật!", parent=self.edit_window)
                self.edit_window.destroy()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật: {e}", parent=self.edit_window)

        tk.Button(self.edit_window, text="Lưu", command=submit_edit).grid(row=4, column=0, columnspan=2, pady=10)

        self.edit_window.lift()
        self.edit_window.attributes('-topmost', True)


    def delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một người dùng để xóa",parent=self)
            return

        user_id = self.tree.item(selected_item)['values'][0]
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa người dùng ID {user_id}?",parent=self)

        if confirm:
            try:
                self.controller.delete_account(user_id)
                self.load_data()
                messagebox.showinfo("Thành công", "Người dùng đã bị xóa!",parent=self)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa người dùng: {e}",parent=self)


if __name__ == "__main__":
    root = ctk.CTk()  
    root.withdraw()  
    app = AccountManager(root)  
    app.mainloop()
