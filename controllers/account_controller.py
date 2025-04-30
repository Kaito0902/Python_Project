from models.account_models import AccountModels
from uuid import uuid4  # Dùng UUID để tạo mã người dùng duy nhất

class AccountController:
    def __init__(self):
        self.account_models = AccountModels()

    def get_all_accounts(self):
        """Lấy danh sách tất cả tài khoản"""
        return self.account_models.get_all_accounts()
    
    def lay_danh_sach_vai_tro(self):
        return self.account_models.lay_danh_sach_vai_tro()


    def add_account(self, ma_nguoi_dung, username, password, vai_tro):
        """Thêm tài khoản mới"""
        
        # Kiểm tra nếu mã người dùng không hợp lệ
        print(f"🔍 Giá trị đầu vào: {ma_nguoi_dung}")
        if not ma_nguoi_dung or ma_nguoi_dung == "0":
            print("❌ Mã người dùng không hợp lệ! Tạo mã mới...")
            ma_nguoi_dung = str(uuid4())[:10]  # Tạo ID duy nhất

        # Kiểm tra nếu tài khoản đã tồn tại
        existing_account = self.account_models.get_by_ma_nguoi_dung(ma_nguoi_dung)
        if existing_account:
            print("❌ Mã người dùng đã tồn tại! Vui lòng nhập mã khác.")
            return False

        # Gửi thông tin đến model để lưu vào database
        self.account_models.add_account(ma_nguoi_dung, username, password, vai_tro)


    def update_account(self, ma_nguoi_dung, username, password, vai_tro):
        """Cập nhật thông tin tài khoản"""
        self.account_models.update_account(ma_nguoi_dung, username, password, vai_tro)

    def delete_account(self, ma_nguoi_dung):
        """Xóa tài khoản"""
        self.account_models.delete_account(ma_nguoi_dung)

    

    def get_logs(self):
        """Lấy danh sách nhật ký hoạt động"""
        return self.account_models.get_logs()
