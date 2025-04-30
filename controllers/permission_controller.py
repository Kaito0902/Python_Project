from models.permission_models import PermissionModel
import tkinter as tk
from tkinter import messagebox

class PermissionController:
    def __init__(self):
        self.model = PermissionModel()
    
    def get_permissions(self):
        """Lấy danh sách quyền từ model."""
        return self.model.get_permissions()
    
    def add_permissions(self, ten_vai_tro, checkboxes):
        """
        Thêm các quyền cho vai trò vào bảng `quyen_han`.
        Chú ý: Sử dụng key lowercase ("xem", "them", "sua", "xoa").
        """
        query_insert_permissions = "INSERT INTO quyen_han (vai_tro, module, xem, them, sua, xoa) VALUES (%s, %s, %s, %s, %s, %s)"
        for module in checkboxes:
            if "xem" not in checkboxes[module]:
                print(f"❌ Lỗi: Không tìm thấy module {module} hoặc key 'xem'!")
                return False
            values = (
                ten_vai_tro,
                module,
                checkboxes[module]["xem"].get(),
                checkboxes[module]["them"].get(),
                checkboxes[module]["sua"].get(),
                checkboxes[module]["xoa"].get()
            )
            self.model.db.execute_commit(query_insert_permissions, values)
    
    def is_role_exists(self, ten_vai_tro):
        """Kiểm tra xem vai trò đã tồn tại trong bảng `vai_tro` hay chưa."""
        query = "SELECT * FROM vai_tro WHERE ten_vai_tro = %s"
        self.model.db.cursor.execute(query, (ten_vai_tro,))
        result = self.model.db.cursor.fetchall()
        return len(result) > 0
    
    def add_new_role(self, ten_vai_tro):
        """Thêm vai trò mới vào bảng `vai_tro` nếu nó chưa tồn tại."""
        query = "INSERT INTO vai_tro (ten_vai_tro) VALUES (%s)"
        self.model.db.execute_commit(query, (ten_vai_tro,))
    
    def delete_item(self, item_id, current_user, module):
        """Xóa dữ liệu từ module nếu user có quyền xóa."""
        module_permissions = self.get_module_permissions(current_user, module)
        if module_permissions["xoa"] == 1:
            query = f"DELETE FROM {module} WHERE id = %s"
            self.model.db.execute_commit(query, (item_id,))
            tk.messagebox.showinfo("Thành công", "Đã xóa dữ liệu thành công!")
        else:
            tk.messagebox.showwarning("Cảnh báo", "Bạn không có quyền xóa trong module này!")