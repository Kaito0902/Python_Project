from models.database import Database


class AccountModels:
    def __init__(self):
        self.db = Database()  # Kết nối database

    def get_all_accounts(self):
        """Lấy danh sách tất cả tài khoản"""
        query = "SELECT ma_nguoi_dung, username, password, vai_tro FROM tai_khoan"
        return self.db.fetch_all(query)
    
    def lay_danh_sach_vai_tro(self):
        query = "SELECT ten_vai_tro FROM vai_tro"
        rows = self.db.fetch_all(query)
        if not rows:  # Kiểm tra nếu danh sách rỗng
            print("⚠ Không tìm thấy vai trò nào trong database!")

        return [row["ten_vai_tro"] for row in rows]  # Trả về danh sách vai trò

    def get_by_ma_nguoi_dung(self, ma_nguoi_dung):
        """Lấy thông tin tài khoản theo mã người dùng"""
        query = "SELECT * FROM tai_khoan WHERE ma_nguoi_dung = %s"
        result = self.db.execute_query(query, (ma_nguoi_dung,))
        return result[0] if result else None

    def add_account(self, ma_nguoi_dung, username, password, vai_tro):
        """Thêm tài khoản vào database"""
        query = "INSERT INTO tai_khoan (ma_nguoi_dung, username, password, vai_tro) VALUES (%s, %s, %s, %s)"
        values = (ma_nguoi_dung, username, password, vai_tro)
        self.db.execute_query(query, values, commit=True)

    def update_account(self, ma_nguoi_dung, username, password, vai_tro):
        """Cập nhật thông tin tài khoản"""
        query = "UPDATE tai_khoan SET username = %s, password = %s, vai_tro = %s WHERE ma_nguoi_dung = %s"
        values = (username, password, vai_tro, ma_nguoi_dung)
        self.db.execute_query(query, values, commit=True)

    def delete_account(self, ma_nguoi_dung):
        """Xóa tài khoản"""
        query = "DELETE FROM tai_khoan WHERE ma_nguoi_dung = %s"
        self.db.execute_query(query, (ma_nguoi_dung,), commit=True)

    

    def log_action(self, ma_nguoi_dung, hanh_dong):
        """Ghi lại hành động của người dùng vào nhật ký"""
        conn = self.db.connect()
        cursor = conn.cursor()
        query = "INSERT INTO nhat_ky (ma_nguoi_dung, hanh_dong) VALUES (%s, %s)"
        cursor.execute(query, (ma_nguoi_dung, hanh_dong))
        conn.commit()
        cursor.close()
        conn.close()

    def get_logs(self):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC")
        logs = cursor.fetchall()
        cursor.close()
        conn.close()
        return logs

