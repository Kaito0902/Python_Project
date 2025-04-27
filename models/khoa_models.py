from models.database import Database

class KhoaModels:
    def __init__(self):
        self.db = Database()

    def select_all(self):
        query = "SELECT * FROM khoa WHERE trang_thai = 1"
        return self.db.execute_query(query)

    def select_by(self, keyword):
        query = "SELECT * FROM khoa WHERE (ma_khoa = %s OR ten_khoa LIKE %s) AND trang_thai = 1"
        return self.db.execute_query(query, (keyword, f"%{keyword}%"))

    def insert(self, ma_khoa, ten_khoa, so_dien_thoai, email):
        query = "INSERT INTO khoa (ma_khoa, ten_khoa, so_dien_thoai, email, trang_thai) VALUES (%s, %s, %s, %s, 1)"
        return self.db.execute_commit(query, (ma_khoa, ten_khoa, so_dien_thoai, email))

    def update(self, ma_khoa, ten_khoa, so_dien_thoai, email):
        query = "UPDATE khoa SET ten_khoa = %s, so_dien_thoai = %s, email = %s WHERE ma_khoa = %s"
        return self.db.execute_commit(query, (ten_khoa, so_dien_thoai, email, ma_khoa))

    def delete(self, ma_khoa):
        query = "UPDATE khoa SET trang_thai = 0 WHERE ma_khoa = %s"
        return self.db.execute_commit(query, (ma_khoa,))

    def select_by_id(self, ma_khoa):
        query = "SELECT * FROM khoa WHERE ma_khoa = %s AND trang_thai = 1"
        result = self.db.execute_query(query, (ma_khoa,))
        if result and len(result) > 0:
            return result[0]

    def check_exists(self, ma_khoa):
        query = "SELECT COUNT(*) FROM khoa WHERE ma_khoa = %s"
        result = self.db.execute_query(query, (ma_khoa,))
        count = result[0]['COUNT(*)'] if result else 0
        return count > 0
