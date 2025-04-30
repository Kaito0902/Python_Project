from models.database import Database
from session import current_user

class LogModels:
    def __init__(self):
        self.db = Database()

    def ghi_nhat_ky(self, ma_nguoi_dung, hanh_dong):
        """
        Ghi nhật ký hoạt động cho người dùng.
        :param ma_nguoi_dung: Mã người dùng thực hiện hành động.
        :param hanh_dong: Mô tả hành động (ví dụ: 'Thêm tài khoản', 'Sửa người dùng', v.v.)
        """
        query = "INSERT INTO nhat_ky (ma_nguoi_dung, hanh_dong) VALUES (%s, %s)"
        self.db.execute_commit(query, (ma_nguoi_dung, hanh_dong))

    def get_logs(self):
        """
        Lấy danh sách nhật ký từ bảng nhat_ky, sắp xếp theo thời gian giảm dần.
        Trả về danh sách các dict với các khóa: id, ma_nguoi_dung, hanh_dong, thoi_gian.
        """
        query = "SELECT id, ma_nguoi_dung, hanh_dong, thoi_gian FROM nhat_ky ORDER BY thoi_gian DESC"
        return self.db.fetch_all(query)

    def authenticate(self, username, password):
        """
        Xác thực người dùng với username và password.
        Nếu đúng, lưu thông tin vào current_user.
        """
        query = "SELECT * FROM tai_khoan WHERE username = %s AND password = %s"
        result = self.db.execute_query(query, (username, password))

        if result:
            user = result[0]  # lấy dòng đầu tiên
            current_user.clear()
            current_user.update({
                "ma_nguoi_dung": user["ma_nguoi_dung"],
                "username": user["username"],
                "vai_tro_id": user["vai_tro"]
            })
            return user
        else:
            return None
