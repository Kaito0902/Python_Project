from models.database import execute_query
from models.lop import Lop

class LopController:
    
    def __init__(self):
        pass  

    def get_all_class(self):
        query = "SELECT ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv FROM lop;"
        classes = execute_query(query, fetch=True)
        return [Lop(**row) for row in classes]

    def search_class(self, ma_lop):
        query = "SELECT * FROM lop WHERE ma_lop = %s"
        result = execute_query(query, (ma_lop,), fetch=True)
        return [Lop(**row) for row in result] if result else None

    def add_class(self, ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv):
        query = """
        INSERT INTO lop (ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return execute_query(query, (ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv))

    def update_class(self, ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv):
        query = """
        UPDATE lop
        SET ma_mon = %s, so_luong = %s, hoc_ky = %s, nam = %s, ma_gv = %s
        WHERE ma_lop = %s
        """
        return execute_query(query, (ma_mon, so_luong, hoc_ky, nam, ma_gv, ma_lop))

    def delete_class(self, ma_lop):
        query = "DELETE FROM lop WHERE ma_lop = %s"
        return execute_query(query, (ma_lop,))

    def is_student_exist(mssv):
        query = "SELECT * FROM sinh_vien WHERE mssv = %s"
        result = execute_query(query, (mssv,), fetch=True)
        return bool(result)

    def is_class_exist(ma_lop):
        query = "SELECT * FROM lop WHERE ma_lop = %s"
        result = execute_query(query, (ma_lop,), fetch=True)
        return bool(result)

    def is_class_full(ma_lop):
        query = "SELECT so_luong FROM lop WHERE ma_lop = %s"
        result = execute_query(query, (ma_lop,), fetch=True)
        if not result:
            return True
        max_students = result[0]['so_luong']

        count_query = "SELECT COUNT(*) AS count FROM dang_ky WHERE ma_lop = %s"
        current = execute_query(count_query, (ma_lop,), fetch=True)[0]['count']
        return current >= max_students

    def is_student_registered(mssv, ma_lop):
        query = "SELECT * FROM dang_ky WHERE mssv = %s AND ma_lop = %s"
        result = execute_query(query, (mssv, ma_lop), fetch=True)
        return bool(result)

    def register_class(mssv, ma_lop):
        query = "INSERT INTO dang_ky (mssv, ma_lop) VALUES (%s, %s)"
        return execute_query(query, (mssv, ma_lop), commit=True)

    def get_all_registrations():
        query = """
        SELECT dk.mssv, sv.ho_ten, dk.ma_lop
        FROM dang_ky dk
        JOIN sinh_vien sv ON dk.mssv = sv.mssv
        """
        return execute_query(query, fetch=True)
