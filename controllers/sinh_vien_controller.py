from models.database import execute_query
from models.sinh_vien import SinhVien

class SinhVienController:
    
    def __init__(self):
        pass  

    def get_students_data(self):
        query = "SELECT mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email FROM sinh_vien"
        students = execute_query(query, fetch=True)
        return students if students else []

    def add_student_db(self, mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email):
        query = """
        INSERT INTO sinh_vien (mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        return execute_query(query, (mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email), commit=True)

    def delete_student_db(self, mssv):
        query = "DELETE FROM sinh_vien WHERE mssv = %s"
        return execute_query(query, (mssv,), commit=True)

    def update_student_db(self, mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email):
        query = """
        UPDATE sinh_vien 
        SET ho_ten = %s, lop = %s, khoa = %s, ngay_sinh = %s, gioi_tinh = %s, que = %s, email = %s 
        WHERE mssv = %s
        """
        return execute_query(query, (ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email, mssv), commit=True)

    def search_student_db(self, query_text):
        query = """
        SELECT mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email 
        FROM sinh_vien 
        WHERE mssv LIKE %s OR ho_ten LIKE %s OR lop LIKE %s OR khoa LIKE %s OR email LIKE %s
        """
        like_query = f"%{query_text}%"
        return execute_query(query, (like_query, like_query, like_query, like_query, like_query), fetch=True)
