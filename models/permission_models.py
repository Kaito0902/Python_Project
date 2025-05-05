from models.database import Database

class PermissionModel:
    def __init__(self):
        self.db = Database()

    def get_permissions(self):
        """Lấy danh sách quyền từ bảng `quyen_han`."""
        query = "SELECT q.vai_tro, q.module, q.xem, q.them, q.sua, q.xoa FROM quyen_han q"
        data = self.db.fetch_all(query)
        if not data:
            print("❌ Không có dữ liệu quyền hạn!")
            return []
        if isinstance(data[0], tuple):
            return [
                {"vai_tro": row[0], "module": row[1], "xem": row[2],
                 "them": row[3], "sua": row[4], "xoa": row[5]} for row in data
            ]
        return [
            {"vai_tro": row["vai_tro"], "module": row["module"], "xem": row["xem"],
             "them": row["them"], "sua": row["sua"], "xoa": row["xoa"]} for row in data
        ]

    def add_role(self, ten_vai_tro):
        """
        Thêm vai trò mới vào bảng `vai_tro` và trả về ID của vai trò vừa thêm.
        """
        query_insert_role = "INSERT INTO vai_tro (ten_vai_tro) VALUES (%s)"
        self.db.execute_commit(query_insert_role, (ten_vai_tro,))
        return self.db.fetch_one("SELECT id FROM vai_tro WHERE ten_vai_tro = %s", (ten_vai_tro,))

    def add_permissions(self, ten_vai_tro, checkboxes):
        """Thêm phân quyền cho vai trò từ dữ liệu trên form."""
        query_insert_permissions = (
            "INSERT INTO quyen_han (vai_tro, module, xem, them, sua, xoa) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        for module in checkboxes:
            values = (
                ten_vai_tro,
                module,
                checkboxes[module]["xem"].get(),
                checkboxes[module]["them"].get(),
                checkboxes[module]["sua"].get(),
                checkboxes[module]["xoa"].get()
            )
            self.db.execute_commit(query_insert_permissions, values)