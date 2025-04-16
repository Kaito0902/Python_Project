from models.mon_hoc_models import MonHocModels

class MonHocController:
    def __init__(self):
        self.mon_hoc_models = MonHocModels()

    def insert(self, ma_mon, ten_mon, so_tin_chi, khoa):
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


