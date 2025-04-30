from models.chi_tiet_diem_models import ChiTietDiemModels

class ChiTietDiemController:
    def __init__(self):
        self.model = ChiTietDiemModels()

    def insert(self, id, mssv, id_cot_diem, diem):
        try:
            self.model.insert(id, mssv, id_cot_diem, diem)
            return True
        except Exception as e:
            print(f"Lỗi khi thêm chi tiết điểm: {e}")
            return False

    def update(self, id, mssv, id_cot_diem, diem):
        try:
            self.model.update(id, mssv, id_cot_diem, diem)
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật chi tiết điểm: {e}")
            return False

    def select_all(self, ma_lop):
        try:
            return self.model.select_all(ma_lop)
        except Exception as e:
            print(f"Lỗi khi lấy danh sách chi tiết điểm: {e}")
            return []
