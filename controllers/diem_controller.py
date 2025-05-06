from models.diem_models import DiemModels

class DiemController:
    def __init__(self):
        self.diem_models = DiemModels()

    def select_all(self):
        try:
            return self.diem_models.select_all()
        except Exception as e:
            print(f"Lỗi khi lấy danh sách điểm: {e}")
            return []

    def select_by_mssv(self, mssv):
        try:
            return self.diem_models.select_by_mssv(mssv)
        except Exception as e:
            print(f"Lỗi khi lấy điểm theo MSSV: {e}")
            return []

    def update(self, mssv, ma_lop, diem_cuoi_ky):
        try:
            return self.diem_models.update_diem_cuoi_ky(mssv, ma_lop, diem_cuoi_ky)
        except Exception as e:
            print(f"Lỗi khi cập nhật điểm cuối kỳ: {e}")
            return False

    def get_danh_sach_mon_va_so_luong_sv(self):
        try:
            return self.diem_models.get_danh_sach_mon_va_so_luong_sv_trong_ky()
        except Exception as e:
            print(f"Lỗi khi lấy danh sách môn và số lượng sinh viên: {e}")
            return []

    def get_diem_cuoi_ky_by_ma_mon(self, ma_lop):
        try:
            return self.diem_models.get_danh_sach_sv_theo_ma_lop(ma_lop)
        except Exception as e:
            print(f"Lỗi khi lấy điểm cuối kỳ theo mã môn: {e}")
            return []

    def get_danh_sach_lop_va_so_luong_sv(self, ma_mon):
        try:
            return self.diem_models.get_danh_sach_lop_va_so_luong_sv(ma_mon)
        except Exception as e:
            print(f"Lỗi khi lấy danh sách lớp và số lượng sinh viên: {e}")
            return []

    def insert_diem_kiem_tra(self, mssv, ma_lop, diem_kiem_tra):
        try:
            return self.insert_diem_kiem_tra(mssv, ma_lop, diem_kiem_tra)
        except Exception as e:
            print(f"Lỗi khi cập nhật điểm kiểm tra: {e}")
            return False
