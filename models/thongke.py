from models.database import Database

class ThongKeModel:
    """Lấy dữ liệu thô từ bảng diem và bảng lop"""
    def __init__(self):
        self.db = Database()

    def lay_all_diem(self):
        sql = """
          SELECT d.ma_lop, l.nam,
                 COUNT(*)              AS si_so,
                 SUM(d.diem_tong_ket>=5) AS dau,
                 SUM(d.diem_tong_ket<5)  AS rot,
                 ROUND(AVG(d.diem_tong_ket),2) AS diem_tb
          FROM diem d
          JOIN lop l ON d.ma_lop = l.ma_lop
          GROUP BY d.ma_lop, l.nam
          ORDER BY l.nam;
        """
        return self.db.execute_query(sql)
