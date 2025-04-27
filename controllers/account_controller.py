from models.account_models import AccountModels

class AccountController:
    def __init__(self):
        self.account_models = AccountModels()

    def get_all_accounts(self):
        """Lấy danh sách tất cả tài khoản"""
        return self.account_models.get_all_accounts()

    def add_account(self, ma_nguoi_dung, username, password, vai_tro):
        """Thêm tài khoản mới"""
        self.account_models.add_account(ma_nguoi_dung, username, password, vai_tro)
        self.account_models.log_action(username, "Thêm tài khoản")

    def update_account(self, ma_nguoi_dung, username, password, vai_tro):
        """Cập nhật thông tin tài khoản"""
        self.account_models.update_account(ma_nguoi_dung, username, password, vai_tro)
        self.account_models.log_action(username, "Cập nhật tài khoản")

    def delete_account(self, ma_nguoi_dung, username):
        """Xóa tài khoản"""
        self.account_models.delete_account(ma_nguoi_dung)
        self.account_models.log_action(username, "Xóa tài khoản")

    def check_permission(self, user_role, permission):
        """Kiểm tra quyền của người dùng"""
        return self.account_models.check_permission(user_role, permission)

    def get_logs(self):
        """Lấy danh sách nhật ký hoạt động"""
        return self.account_models.get_logs()
