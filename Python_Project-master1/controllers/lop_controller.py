from models.lop import LopModels

class LopController:
    def __init__(self):
        self.lop_models = LopModels()

    def insert(self, ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv):
        try:
            self.lop_models.insert(ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv)
            return True
        except Exception as e:
            print(f"Lỗi khi thêm lớp: {e}")
            return False

    def update(self, ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv):
        try:
            self.lop_models.update(ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv)
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật lớp: {e}")
            return False

    def select_all(self):
        try:
            return self.lop_models.select_all()
        except Exception as e:
            print(f"Lỗi khi lấy danh sách lớp: {e}")
            return []

    def delete(self, ma_lop):
        try:
            self.lop_models.delete(ma_lop)
            return True
        except Exception as e:
            print(f"Lỗi khi xóa lớp: {e}")
            return False

    def select_by(self, ma_lop):
        try:
            return self.lop_models.select_by(ma_lop)
        except Exception as e:
            print(f"Lỗi khi tìm lớp: {e}")
            return []
