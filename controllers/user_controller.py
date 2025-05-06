from models.permission_models import PermissionModel  # 🔥 Import model


class UserController:
    def __init__(self):
        self.model = PermissionModel()  # 🔥 Khởi tạo model
        print("✅ UserController đã khởi tạo & kết nối database!")

    def get_module_permissions(self, username, module):
        """Lấy quyền của user trên một module cụ thể."""

        # 🔥 Kiểm tra kết nối database trước khi truy vấn
        if not self.model.db:
            print("❌ Lỗi: Database chưa được khởi tạo!")
            return {"xem": 0, "them": 0, "sua": 0, "xoa": 0}

        query = """
            SELECT q.xem, q.them, q.sua, q.xoa
            FROM quyen_han q
            INNER JOIN tai_khoan u ON q.vai_tro = u.vai_tro
            WHERE u.username = %s AND q.module = %s
        """

        try:
            result = self.model.db.fetch_one(query, (username, module))

            if result is None:  # 🔥 Nếu không có dữ liệu, trả về quyền mặc định
                print(f"❌ Không tìm thấy quyền cho user {username} trên module {module}")
                return {"xem": 0, "them": 0, "sua": 0, "xoa": 0}

            # 🔥 Đảm bảo kết quả luôn trả về dạng dict
            if isinstance(result, tuple):
                return {"xem": result[0], "them": result[1], "sua": result[2], "xoa": result[3]}

            if isinstance(result, dict):
                return result  # 🔥 Nếu dữ liệu đã là dict, trả về luôn

            print(f"❌ Lỗi: Kết quả không đúng kiểu dữ liệu! {result}")
            return {"xem": 0, "them": 0, "sua": 0, "xoa": 0}  # 🔥 Tránh lỗi nếu kiểu dữ liệu không đúng

        except Exception as e:
            print(f"❌ Lỗi khi truy vấn SQL: {e}")
            return {"xem": 0, "them": 0, "sua": 0, "xoa": 0}  # 🔥 Tránh lỗi khi truy vấn SQL


# 🚀 Test nhanh
if __name__ == "__main__":
    controller = UserController()
    permissions = controller.get_module_permissions("admin", "Quản lý môn học")
    print("🚀 Quyền của admin:", permissions)