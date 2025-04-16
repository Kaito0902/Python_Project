from models.database import Database

class LopModels:
    def __init__(self):
        self.db = Database()

    def select_all(self):
        query = "SELECT * FROM lop WHERE trang_thai = 1"
        return self.db.execute_query(query)

    def select_by(self, keyword):
        query = "SELECT * FROM lop WHERE (ma_lop = %s OR ma_mon LIKE %s) AND trang_thai = 1"
        return self.db.execute_query(query, (keyword, f"%{keyword}%"))

    def insert(self, ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv):
        query = """
        INSERT INTO lop (ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv, trang_thai)
        VALUES (%s, %s, %s, %s, %s, %s, 1)
        """
        return self.db.execute_commit(query, (ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv))

    def update(self, ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv):
        query = """
        UPDATE lop
        SET ma_mon = %s, so_luong = %s, hoc_ky = %s, nam = %s, ma_gv = %s
        WHERE ma_lop = %s
        """
        return self.db.execute_commit(query, (ma_mon, so_luong, hoc_ky, nam, ma_gv, ma_lop))

    def delete(self, ma_lop):
        query = "UPDATE lop SET trang_thai = 0 WHERE ma_lop = %s"
        return self.db.execute_commit(query, (ma_lop,))
