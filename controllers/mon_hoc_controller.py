from models.mon_hoc_models import MonHocModels
from session import current_user_permissions


class MonHocController:
    def __init__(self):
        self.mon_hoc_models = MonHocModels()

    def insert(self, ma_mon, ten_mon, so_tin_chi, khoa):
        if not current_user_permissions.get("mon_hoc", {}).get("them"):
            print("Bạn không có quyền thêm môn học!")
            return False

        try:
            self.mon_hoc_models.insert(ma_mon, ten_mon, so_tin_chi, khoa)
            return True
        except Exception as e:
            print(f"Lỗi khi thêm môn học: {e}")
            return False

    def update(self, ma_mon, ten_mon, so_tin_chi, khoa):
        try:
            self.mon_hoc_models.update(ma_mon, ten_mon, so_tin_chi, khoa)
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật môn học: {e}")
            return False

    def select_all(self):
        try:
            return self.mon_hoc_models.select_all()
        except Exception as e:
            print(f"Lỗi khi lấy danh sách môn học: {e}")
            return []

    def check_exists(self, ma_mh):
        try:
            return self.mon_hoc_models.check_exists(ma_mh)
        except Exception as e:
            print(f"Lỗi khi kiểm tra tồn tại môn học: {e}")
            return False

    def check_exists_for_update(self, ma_mh_moi, ma_mh_cu):
        try:
            if ma_mh_moi == ma_mh_cu:
                return False
            return self.mon_hoc_models.check_exists(ma_mh_moi)
        except Exception as e:
            print(f"Lỗi khi kiểm tra tồn tại giảng viên khi cập nhật: {e}")
            return False

    def delete(self, ma_mon):
        try:
            self.mon_hoc_models.delete(ma_mon)
            return True
        except Exception as e:
            print(f"Lỗi khi xóa môn học: {e}")
            return False

    def select_by(self, keyword):
        try:
            return self.mon_hoc_models.select_by(keyword)
        except Exception as e:
            print(f"Lỗi khi tìm kiếm môn học: {e}")
            return []

    def select_by_id(self, ma_mon):
        try:
            return self.mon_hoc_models.select_by_id(ma_mon)
        except Exception as e:
            print(f"Lỗi khi lấy môn học: {e}")
            return []




