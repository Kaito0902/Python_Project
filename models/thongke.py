from models.database import Database

class ThongKeModel:
    """Lấy dữ liệu thô từ bảng diem và bảng lop"""
    def __init__(self):
        self.db = Database()

    def lay_all_diem(self):

        sql = (
            "SELECT d.mssv, d.diem_tong_ket, l.nam AS nam "
            "FROM diem d "
            "JOIN lop l ON d.ma_mon = l.ma_mon"
        )
        return self.db.execute_query(sql)
