from models.database import Database
from datetime import datetime
class DiemModels:
    def __init__(self):
        self.db = Database()

    def select_all(self):
        query = "SELECT * FROM diem"
        return self.db.execute_query(query)

    def select_by_mssv(self, mssv):
        query = "SELECT * FROM diem WHERE mssv = %s"
        return self.db.execute_query(query, (mssv,))

    def update_diem_cuoi_ky(self, mssv, ma_lop, diem_cuoi_ky):
        query = """
            UPDATE diem
            SET diem_cuoi_ky = %s
            WHERE mssv = %s AND ma_lop = %s
        """
        return self.db.execute_commit(query, (diem_cuoi_ky, mssv, ma_lop))

    def get_danh_sach_lop_va_so_luong_sv(self, ma_mon):
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Xác định học kỳ từ tháng hiện tại
        if 1 <= current_month <= 5:
            hoc_ky = 2
        elif 6 <= current_month <= 7:
            hoc_ky = 3
        else:
            hoc_ky = 1

        query = """
            SELECT l.ma_lop, COUNT(DISTINCT dk.mssv) AS so_luong_sinh_vien
            FROM lop l
            JOIN dang_ky dk ON l.ma_lop = dk.ma_lop
            WHERE l.ma_mon = %s AND l.hoc_ky = %s AND l.nam = %s
            GROUP BY l.ma_lop
        """
        return self.db.execute_query(query, (ma_mon, hoc_ky, current_year))

    def get_danh_sach_sv_theo_ma_lop(self, ma_lop):
        query = """
            SELECT sv.mssv, sv.ho_ten
            FROM diem d
            JOIN sinh_vien sv ON d.mssv = sv.mssv
            WHERE d.ma_lop = %s
        """
        return self.db.execute_query(query, (ma_lop,))

    def get_danh_sach_mon_va_so_luong_sv_trong_ky(self):
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Xác định học kỳ theo tháng hiện tại
        if 1 <= current_month <= 5:
            hoc_ky = 2
        elif 6 <= current_month <= 7:
            hoc_ky = 3
        else:
            hoc_ky = 1

        query = """
            SELECT l.ma_mon, m.ten_mon, COUNT(DISTINCT dk.mssv) AS so_luong_sinh_vien
            FROM dang_ky dk
            JOIN lop l ON dk.ma_lop = l.ma_lop
            JOIN mon_hoc m ON l.ma_mon = m.ma_mon
            WHERE l.hoc_ky = %s AND l.nam = %s
            GROUP BY l.ma_mon, m.ten_mon
        """
        return self.db.execute_query(query, (hoc_ky, current_year))
