from models.database import Database

class LopModels:
    def __init__(self):
        self.db = Database()

    def select_all(self):
        query = "SELECT * FROM lop WHERE trang_thai = 1"
        return self.db.execute_query(query)

    def select_by(self, keyword):
        like_kw = f"%{keyword}%"
        query = """
            SELECT * FROM lop 
            WHERE (ma_lop LIKE %s OR ma_mon LIKE %s OR nam LIKE %s OR ma_gv LIKE %s) 
            AND trang_thai = 1
        """
        return self.db.execute_query(query, (like_kw, like_kw, like_kw, like_kw))
    
    def get_students_in_class(self, ma_lop):
        query = """
        SELECT sv.mssv, sv.ho_ten, sv.ngay_sinh, sv.khoa, sv.email
        FROM dang_ky dk
        JOIN sinh_vien sv ON dk.mssv = sv.mssv
        WHERE dk.ma_lop = %s AND sv.trang_thai = 1
        """
        return self.db.execute_query(query, (ma_lop,))
    
    def get_by_ma_lop(self, ma_lop):
        query = "SELECT * FROM lop WHERE ma_lop = %s"
        result = self.db.execute_query(query, (ma_lop,))
        return result[0] if result else None
    
    def is_valid_mon(self,ma_mon):
        query = "SELECT * FROM mon_hoc WHERE ma_mon = %s AND trang_thai = 1"
        result = self.db.execute_query(query, (ma_mon,))
        return bool(result)

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

    def restore(self, ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv):
        query = """
        UPDATE lop
        SET ma_mon = %s, so_luong = %s, hoc_ky = %s, nam = %s, ma_gv = %s, trang_thai = 1
        WHERE ma_lop = %s
        """
        return self.db.execute_commit(query, (ma_mon, so_luong, hoc_ky, nam, ma_gv, ma_lop))

    def is_class_available(self, ma_lop):
        query = """
        SELECT so_luong, 
               (SELECT COUNT(*) FROM dang_ky WHERE ma_lop = %s) AS da_dang_ky
        FROM lop 
        WHERE ma_lop = %s
        """
        return self.db.execute_query(query, (ma_lop, ma_lop))

    def is_student_registered(self, mssv, ma_lop):
        query = "SELECT * FROM dang_ky WHERE mssv = %s AND ma_lop = %s"
        result = self.db.execute_query(query, (mssv, ma_lop))
        return bool(result)

    def register_student_to_class(self, mssv, ma_lop):
        query = "INSERT INTO dang_ky (mssv, ma_lop) VALUES (%s, %s)"
        return self.db.execute_commit(query, (mssv, ma_lop))
    
    def huy_dang_ky(self, mssv, ma_lop):
        query = "DELETE FROM dang_ky WHERE mssv = %s AND ma_lop = %s"
        return self.db.execute_commit(query, (mssv, ma_lop))
    
    def phan_cong_giang_vien(self, ma_lop, ma_gv):
        query = "UPDATE lop SET ma_gv = %s WHERE ma_lop = %s"
        return self.db.execute_commit(query, (ma_gv, ma_lop))
