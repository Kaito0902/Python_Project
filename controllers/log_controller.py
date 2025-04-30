from session import current_user
from models.log_models import LogModels

class LogController:
    def __init__(self):
        self.log_model = LogModels()

    def ghi_nhat_ky(self, ma_nguoi_dung, hanh_dong):
        """
        Ghi nhật ký hành động của người dùng.
        :param ma_nguoi_dung: Mã người dùng.
        :param hanh_dong: Mô tả hành động.
        """
        if not ma_nguoi_dung and "ma_nguoi_dung" in current_user:
            ma_nguoi_dung = current_user["ma_nguoi_dung"]

        if not ma_nguoi_dung:
            print("❌ Không có người dùng hợp lệ để ghi nhật ký!")
            return False

        self.log_model.ghi_nhat_ky(ma_nguoi_dung, hanh_dong)

    def lay_nhat_ky(self):
        """
        Lấy toàn bộ nhật ký.
        """
        return self.log_model.get_logs()

    def dang_nhap(self, username, password):
        """
        Đăng nhập và tự động ghi lại nhật ký đăng nhập thành công.
        :param username: Tên đăng nhập
        :param password: Mật khẩu
        """
        user = self.log_model.authenticate(username, password)
        if user:
            self.ghi_nhat_ky("Đăng nhập hệ thống")
            return True
        return False
