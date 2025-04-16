from models.database import Database

class GiangVienModels:
    def __init__(self):
        self.db = Database()

    def select_all(self):
        query = "SELECT * from giang_vien WHERE trang_thai = 1"
        return self.db.execute_query(query)

    def select_by(self, keyword):
        query = "SELECT * from giang_vien WHERE (ma_gv = %s OR ho_ten LIKE %s) AND trang_thai = 1"
        return self.db.execute_query(query, (keyword, f"%{keyword}%"))

    def insert(self, ma_gv, ho_ten, khoa, email, sdt):
        query = "INSERT INTO giang_vien (ma_gv, ho_ten, khoa, email, sdt, trang_thai) VALUES (%s, %s, %s, %s, %s, 1)"
        return self.db.execute_commit(query, (ma_gv, ho_ten, khoa, email, sdt))

    def update(self, ma_gv, ho_ten, khoa, email, sdt):
        query = "UPDATE giang_vien SET ho_ten = %s, khoa = %s, email = %s, sdt = %s WHERE ma_gv = %s"
        return self.db.execute_commit(query, (ho_ten, khoa, email, sdt, ma_gv))

    def delete(self, ma_gv):
        query = "UPDATE giang_vien SET trang_thai = 0 WHERE ma_gv = %s"
        return self.db.execute_commit(query, (ma_gv,))
