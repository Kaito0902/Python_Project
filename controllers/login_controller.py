from models.login_models import LoginModels
from session import current_user

class LoginController:
    def __init__(self):
        self.login_model = LoginModels()

    def dang_nhap(self, username, password):
        """
        Thực hiện đăng nhập.
        Nếu thành công, lưu thông tin vào current_user.
        Trả về True nếu thành công, False nếu thất bại.
        """
        user = self.login_model.dang_nhap(username, password)
        if user:
            current_user.clear()
            current_user.update({
                "ma_nguoi_dung": user["ma_nguoi_dung"],
                "username": user["username"],
                "vai_tro_id": user["vai_tro"]
            })
            return True
        return False

    def dang_xuat(self):
        """
        Đăng xuất người dùng hiện tại (xóa current_user).
        """
        current_user.clear()

    def lay_ma_nguoi_dung(self, username, password):

        return self.login_model.dang_nhap(username, password)

