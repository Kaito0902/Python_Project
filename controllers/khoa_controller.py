from models.khoa_models import KhoaModels


class KhoaController:
    def __init__(self):
        self.khoa_models = KhoaModels()

    def insert(self, ma_khoa, ten_khoa, so_dien_thoai, email):
        try:
            self.khoa_models.insert(ma_khoa, ten_khoa, so_dien_thoai, email)
            return True
        except Exception as e:
            print(f"Lỗi khi thêm khoa: {e}")
            return False

    def update(self, ma_khoa, ten_khoa, so_dien_thoai, email):
        try:
            self.khoa_models.update(ma_khoa, ten_khoa, so_dien_thoai, email)
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật khoa: {e}")
            return False

    def select_all(self):
        try:
            return self.khoa_models.select_all()
        except Exception as e:
            print(f"Lỗi khi lấy danh sách khoa: {e}")
            return []

    def delete(self, ma_khoa):
        try:
            self.khoa_models.delete(ma_khoa)
            return True
        except Exception as e:
            print(f"Lỗi khi xóa khoa: {e}")
            return False

    def select_by(self, keyword):
        try:
            return self.khoa_models.select_by(keyword)
        except Exception as e:
            print(f"Lỗi khi tìm kiếm khoa: {e}")
            return []

    def select_by_id(self, ma):
        try:
            return self.khoa_models.select_by_id(ma)
        except Exception as e:
            print(f"Lỗi khi tìm kiếm khoa: {e}")
            return None

    def select_by_name(self):
        try:
            return self.khoa_models.select_by_name()
        except Exception as e:
            print(f"Lỗi khi lấy danh sách khoa: {e}")
            return None

    def check_exists(self, ma_khoa):
        try:
            return self.khoa_models.check_exists(ma_khoa)
        except Exception as e:
            print(f"Lỗi khi kiểm tra tồn tại môn học: {e}")
            return False

    def check_exists_for_update(self, ma_khoa_moi, ma_khoa_cu):
        try:
            if ma_khoa_moi == ma_khoa_cu:
                return False
            return self.khoa_models.check_exists(ma_khoa_moi)
        except Exception as e:
            print(f"Lỗi khi kiểm tra tồn tại giảng viên khi cập nhật: {e}")
            return False