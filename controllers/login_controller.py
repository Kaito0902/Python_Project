import mysql.connector
from models.database import Database

class LoginController:
    def __init__(self):
        self.db = Database()

    def dang_nhap(self, username, password):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM tai_khoan WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if user:
            return user  # Trả về thông tin tài khoản nếu đăng nhập thành công
        return None  # Sai tài khoản hoặc mật khẩu
