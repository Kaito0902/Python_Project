from models.database import Database


class AccountModels:
    def __init__(self):
        self.db = Database()

    def get_all_accounts(self):
        return self.db.fetch_all("SELECT ma_nguoi_dung, username, password, vai_tro FROM tai_khoan")

    def add_account(self, ma_nguoi_dung, username, password, vai_tro):
        query = "INSERT INTO tai_khoan (ma_nguoi_dung, username, password, vai_tro) VALUES (%s, %s, %s, %s)"
        values = (ma_nguoi_dung, username, password, vai_tro)
        self.db.execute_query(query, values)

    def update_account(self, ma_nguoi_dung, username, password, vai_tro):
        query = "UPDATE tai_khoan SET username = %s, password = %s, vai_tro = %s WHERE ma_nguoi_dung = %s"
        values = (username, password, vai_tro, ma_nguoi_dung)
        self.db.execute_query(query, values)

    def delete_account(self, ma_nguoi_dung):
        query = "DELETE FROM tai_khoan WHERE ma_nguoi_dung = %s"
        self.db.execute_query(query, (ma_nguoi_dung,))

    def check_permission(self, user_role, permission):
        query = """
            SELECT 1 FROM phan_quyen
            JOIN vai_tro ON phan_quyen.vai_tro_id = vai_tro.id
            JOIN quyen ON phan_quyen.quyen_id = quyen.id
            WHERE vai_tro.ten_vai_tro = %s AND quyen.ten_quyen = %s
        """
        return self.db.execute_query(query, (user_role, permission))


    def log_action(self, nguoi_dung, hanh_dong):
        query = "INSERT INTO nhat_ky (nguoi_dung, hanh_dong) VALUES (%s, %s)"
        return self.db.execute_query(query, (nguoi_dung, hanh_dong))


    def get_logs(self):
        return self.db.execute_query("SELECT * FROM logs ORDER BY timestamp DESC")


