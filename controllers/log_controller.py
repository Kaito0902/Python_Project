from models.database import Database
from session import current_user


class LogController:
    def __init__(self):
        self.db = Database()

    def ghi_nhat_ky(self, ma_nguoi_dung, hanh_dong):
        """
        Ghi nhật ký hoạt động cho người dùng.
        :param ma_nguoi_dung: Mã người dùng thực hiện hành động.
        :param hanh_dong: Mô tả hành động (ví dụ: 'Thêm tài khoản', 'Sửa người dùng', v.v.)
        """
        conn = self.db.connect()
        cursor = conn.cursor()
        query = "INSERT INTO nhat_ky (ma_nguoi_dung, hanh_dong) VALUES (%s, %s)"
        cursor.execute(query, (ma_nguoi_dung, hanh_dong))
        conn.commit()
        cursor.close()
        conn.close()


    def get_logs(self):
        """
        Lấy danh sách nhật ký từ bảng nhat_ky, sắp xếp theo thời gian giảm dần.
        Trả về danh sách các dict với các khóa: id, ma_nguoi_dung, hanh_dong, thoi_gian.
        """
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, ma_nguoi_dung, hanh_dong, thoi_gian FROM nhat_ky ORDER BY thoi_gian "
        cursor.execute(query)
        logs = cursor.fetchall()
        cursor.close()
        conn.close()
        return logs
    
    
    def authenticate(self, username, password):
        # Giả sử bạn đã thực hiện truy vấn và lấy được dữ liệu từ database thành công
        query = "SELECT * FROM tai_khoan WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        user = self.cursor.fetchone()
        
        if user:
            current_user.clear()
            current_user.update({
                "ma_nguoi_dung": user["ma_nguoi_dung"],
                "username": user["username"],
                "vai_tro_id": user["vai_tro"]   # Giả sử trường vai_tro lưu id của vai trò
            })
            return user
        else:
            return None

