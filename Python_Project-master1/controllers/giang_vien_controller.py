from models.giang_vien_models import GiangVienModels

class GiangVienController:
    def __init__(self):
        self.giang_vien_models = GiangVienModels()

    def insert(self, ma_gv, ten_gv, email, sdt, dia_chi):
        try:
            self.giang_vien_models.insert(ma_gv, ten_gv, email, sdt, dia_chi)
            return True
        except Exception as e:
            print(f"Lỗi khi thêm giảng viên: {e}")
            return False

    def update(self, ma_gv, ten_gv, email, sdt, dia_chi):
        try:
            self.giang_vien_models.update(ma_gv, ten_gv, email, sdt, dia_chi)
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

