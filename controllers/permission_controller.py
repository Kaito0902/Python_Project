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
        query_insert_permissions = (
            "INSERT INTO quyen_han (vai_tro, module, xem, them, sua, xoa) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
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
        """Thêm vai trò mới vào bảng `vai_tro`."""
        query = "INSERT INTO vai_tro (ten_vai_tro) VALUES (%s)"
        self.model.db.execute_commit(query, (ten_vai_tro,))

    def get_role_details(self, ten_vai_tro):
        """
        Lấy chi tiết vai trò từ bảng `quyen_han` dựa trên tên vai trò.
        Trả về dict với key là tên module và value là dict chứa các quyền.
        """
        query = "SELECT module, xem, them, sua, xoa FROM quyen_han WHERE vai_tro = %s"
        self.model.db.cursor.execute(query, (ten_vai_tro,))
        rows = self.model.db.cursor.fetchall()
        if not rows:
            return None
        role_details = {}
        for row in rows:
            if isinstance(row, tuple):
                module = row[0]
                role_details[module] = {
                    "xem": row[1],
                    "them": row[2],
                    "sua": row[3],
                    "xoa": row[4]
                }
            else:
                module = row["module"]
                role_details[module] = {
                    "xem": row["xem"],
                    "them": row["them"],
                    "sua": row["sua"],
                    "xoa": row["xoa"]
                }
        return role_details

    def update_role(self, old_role, new_role, updated_permissions):
        """
        Cập nhật tên vai trò và các quyền của vai trò.
        Nếu tên vai trò thay đổi, cập nhật bảng `vai_tro` và tiến hành update bảng `quyen_han`.
        """
        if old_role != new_role:
            query_update_role = "UPDATE vai_tro SET ten_vai_tro = %s WHERE ten_vai_tro = %s"
            self.model.db.execute_commit(query_update_role, (new_role, old_role))
        query_update_permissions = (
            "UPDATE quyen_han SET xem = %s, them = %s, sua = %s, xoa = %s "
            "WHERE vai_tro = %s AND module = %s"
        )
        for module, perms in updated_permissions.items():
            values = (
                perms.get("xem", 0),
                perms.get("them", 0),
                perms.get("sua", 0),
                perms.get("xoa", 0),
                new_role,  # sử dụng tên vai trò mới sau update
                module
            )
            self.model.db.execute_commit(query_update_permissions, values)

    def is_role_used(self, ten_vai_tro):
        """
        Kiểm tra xem vai trò có đang được sử dụng bởi tài khoản nào không.
        Sử dụng bảng `tai_khoan` với cột `vai_tro`.
        """
        query = "SELECT * FROM tai_khoan WHERE vai_tro = %s"
        self.model.db.cursor.execute(query, (ten_vai_tro,))
        result = self.model.db.cursor.fetchall()
        return len(result) > 0

    def delete_role(self, ten_vai_tro):
        """
        Xóa vai trò và các quyền liên quan từ bảng `quyen_han` và `vai_tro`.
        Phương thức này chỉ được gọi sau khi đã kiểm tra ràng buộc.
        """
        query_delete_permissions = "DELETE FROM quyen_han WHERE vai_tro = %s"
        self.model.db.execute_commit(query_delete_permissions, (ten_vai_tro,))
        query_delete_role = "DELETE FROM vai_tro WHERE ten_vai_tro = %s"
        self.model.db.execute_commit(query_delete_role, (ten_vai_tro,))

    def get_account_count_by_role(self, ten_vai_tro):
        """
        Lấy số lượng tài khoản có vai trò là ten_vai_tro từ bảng `tai_khoan`.
        """
        query = "SELECT COUNT(*) as count FROM tai_khoan WHERE vai_tro = %s"
        self.model.db.cursor.execute(query, (ten_vai_tro,))
        result = self.model.db.cursor.fetchone()
        if result:
            if isinstance(result, tuple):
                return result[0]
            else:
                return result.get("count", 0)
        return 0