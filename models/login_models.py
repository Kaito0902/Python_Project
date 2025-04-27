from models.database import Database

class LoginModels:
    def __init__(self):
        self.db = Database()

    def dang_nhap(self, username, password):
        """
        Thực hiện đăng nhập.
        Trả về thông tin tài khoản nếu thành công, None nếu thất bại.
        """
        query = "SELECT * FROM tai_khoan WHERE username = %s AND password = %s"
        result = self.db.execute_query(query, (username, password))

        if result:
            return result[0]  # Lấy dòng đầu tiên (vì username là duy nhất)
        return None
