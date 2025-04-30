from models.giang_vien_models import GiangVienModels
import re


class GiangVienController:
    def __init__(self):
        self.giang_vien_models = GiangVienModels()

    def insert(self, ma_gv, ten_gv, khoa, email, sdt):
        try:
            if not self.is_valid_phone(sdt):
                print("Số điện thoại không hợp lệ.")
                return False
            if not self.is_valid_email(email):
                print("Email không hợp lệ.")
                return False

            self.giang_vien_models.insert(ma_gv, ten_gv, khoa, email, sdt)
            return True
        except Exception as e:
            print(f"Lỗi khi thêm giảng viên: {e}")
            return False

    def update(self, ma_gv, ten_gv, khoa, email, sdt):
        try:
            if not self.is_valid_phone(sdt):
                print("Số điện thoại không hợp lệ.")
                return False
            if not self.is_valid_email(email):
                print("Email không hợp lệ.")
                return False

            self.giang_vien_models.update(ma_gv, ten_gv, khoa, email, sdt)
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật giảng viên: {e}")
            return False

    def select_all(self):
        try:
            return self.giang_vien_models.select_all()
        except Exception as e:
            print(f"Lỗi khi lấy danh sách giảng viên: {e}")
            return []

    def check_exists(self, ma_gv):
        try:
            return self.giang_vien_models.check_exists(ma_gv)
        except Exception as e:
            print(f"Lỗi khi kiểm tra tồn tại giảng viên: {e}")
            return False

    def check_exists_for_update(self, ma_gv_moi, ma_gv_cu):
        try:
            if ma_gv_moi == ma_gv_cu:
                return False
            return self.giang_vien_models.check_exists(ma_gv_moi)
        except Exception as e:
            print(f"Lỗi khi kiểm tra tồn tại giảng viên khi cập nhật: {e}")
            return False

    def delete(self, ma_gv):
        try:
            self.giang_vien_models.delete(ma_gv)
            return True
        except Exception as e:
            print(f"Lỗi khi xóa giảng viên: {e}")
            return False

    def select_by(self, keyword):
        try:
            return self.giang_vien_models.select_by(keyword)
        except Exception as e:
            print(f"Lỗi khi tìm kiếm giảng viên: {e}")
            return []

    def is_valid_phone(self, phone):
        pattern = r"^0\d{9}$"
        return bool(re.match(pattern, phone))

    def is_valid_email(self, email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        return bool(re.match(pattern, email))

