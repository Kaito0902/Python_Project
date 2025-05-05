from models.cau_hinh_diem_models import CauHinhDiemModels

class CauHinhDiemController:
    def __init__(self):
        self.model = CauHinhDiemModels()

    def insert(self, ma_lop, ten_cot_diem, trong_so):
        try:
            self.model.insert(ma_lop, ten_cot_diem, trong_so)
            return True
        except Exception as e:
            print(f"Lỗi khi thêm cấu hình điểm: {e}")
            return False

    def update(self, id, ma_lop, ten_cot_diem, trong_so):
        try:
            self.model.update(id, ma_lop, ten_cot_diem, trong_so)
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật cấu hình điểm: {e}")
            return False

    def delete(self, id):
        try:
            self.model.delete(id)
            return True
        except Exception as e:
            print(f"Lỗi khi xóa cấu hình điểm: {e}")
            return False

    def select_all(self, ma_lop):
        try:
            return self.model.select_all(ma_lop)
        except Exception as e:
            print(f"Lỗi khi lấy danh sách cấu hình điểm: {e}")
            return []

    def get_total_trong_so(self, ma_lop):
        return self.model.get_total_trong_so(ma_lop)

    def get_trong_so_by_id(self, id):
        try:
            return self.model.get_trong_so_by_id(id)
        except Exception as e:
            print(f"Lỗi khi lấy trọng số theo id: {e}")
            return 0

    def is_ten_cot_diem_exists(self, ma_lop, ten_cot_diem):
        return self.model.is_ten_cot_diem_exists(ma_lop, ten_cot_diem)