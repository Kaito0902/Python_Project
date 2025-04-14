from models.database import Database

class SinhVienModels:
    def __init__(self):
        self.db = Database()

    def select_all(self):
        query = """
        SELECT mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email
        FROM sinh_vien
        WHERE trang_thai = 1
        """
        return self.db.execute_query(query)

    def select_by(self, keyword):
        query = """
        SELECT mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email
        FROM sinh_vien
        WHERE trang_thai = 1 AND (
            mssv LIKE %s OR ho_ten LIKE %s OR lop LIKE %s OR khoa LIKE %s OR email LIKE %s
        )
        """
        like_kw = f"%{keyword}%"
        return self.db.execute_query(query, (like_kw, like_kw, like_kw, like_kw, like_kw))

    def insert(self, mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email):
        query = """
        INSERT INTO sinh_vien (mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email, trang_thai)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)
        """
        return self.db.execute_commit(query, (mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email))

    def update(self, mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email):
        query = """
        UPDATE sinh_vien
        SET ho_ten = %s, lop = %s, khoa = %s, ngay_sinh = %s, gioi_tinh = %s, que = %s, email = %s
        WHERE mssv = %s
        """
        return self.db.execute_commit(query, (ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email, mssv))

    def delete(self, mssv):
        query = "UPDATE sinh_vien SET trang_thai = 0 WHERE mssv = %s"
        return self.db.execute_commit(query, (mssv,))
