from models.database import Database


class LopModels:
    def __init__(self):
        self.db = Database()

    def select_all(self):
        query = """
            SELECT lop.*, mon_hoc.ten_mon
            FROM lop
            JOIN mon_hoc ON lop.ma_mon = mon_hoc.ma_mon
            WHERE lop.trang_thai = 1
        """
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
        query = """
        SELECT l.*, mh.ten_mon, 
            COALESCE(gv.ho_ten, 'Chưa phân công') AS ho_ten,
            gv.trang_thai AS gv_trang_thai
        FROM lop l
        JOIN mon_hoc mh ON l.ma_mon = mh.ma_mon
        LEFT JOIN giang_vien gv ON l.ma_gv = gv.ma_gv
        WHERE l.ma_lop = %s
        """
        result = self.db.execute_query(query, (ma_lop,))
        return result[0] if result else None

    def is_valid_mon(self, ma_mon):
        query = "SELECT * FROM mon_hoc WHERE ma_mon = %s AND trang_thai = 1"
        result = self.db.execute_query(query, (ma_mon,))
        return bool(result)

    def insert(self, ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv):
        query = """
        INSERT INTO lop (ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv, trang_thai)
        VALUES (%s, %s, %s, %s, %s, %s, 1)
        """
        return self.db.execute_commit(query, (ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv))

    def update(self, ma_lop, ma_mon, so_luong, hoc_ky, nam):
        query = """
        UPDATE lop
        SET ma_mon = %s, so_luong = %s, hoc_ky = %s, nam = %s
        WHERE ma_lop = %s
        """
        return self.db.execute_commit(query, (ma_mon, so_luong, hoc_ky, nam, ma_lop))

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

    def them(self):
        query_them = """
                    INSERT INTO chi_tiet_diem (mssv, id_cot_diem, diem)
                    SELECT dk.mssv, chd.id, 0
                    FROM dang_ky dk
                    JOIN cau_hinh_diem chd ON dk.ma_lop = chd.ma_lop
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM chi_tiet_diem ctd
                        WHERE ctd.mssv = dk.mssv AND ctd.id_cot_diem = chd.id
                    );
                    """
        return self.db.execute_commit(query_them)

    def huy_dang_ky(self, mssv, ma_lop):
        query = "DELETE FROM dang_ky WHERE mssv = %s AND ma_lop = %s"
        query_delete_diem = "DELETE FROM chi_tiet_diem WHERE mssv = %s"
        self.db.execute_commit(query_delete_diem, (mssv,))
        return self.db.execute_commit(query, (mssv, ma_lop))

    def danh_sach_gv_theo_khoa(self, ma_lop):
        query = """
        SELECT gv.*
        FROM giang_vien gv
        JOIN khoa k ON gv.khoa = k.ma_khoa
        WHERE gv.trang_thai = 1
        AND gv.khoa = (
            SELECT mh.khoa
            FROM lop l
            JOIN mon_hoc mh ON l.ma_mon = mh.ma_mon
            WHERE l.ma_lop = %s
        )
        """
        return self.db.execute_query(query, (ma_lop,))

    def phan_cong_giang_vien(self, ma_lop, ma_gv):
        query = "UPDATE lop SET ma_gv = %s WHERE ma_lop = %s"
        return self.db.execute_commit(query, (ma_gv, ma_lop))
