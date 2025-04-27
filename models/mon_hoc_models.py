from models.database import Database

class MonHocModels:
    def __init__(self):
        self.db = Database()

    def select_all(self):
        query = "SELECT * from mon_hoc WHERE trang_thai = 1"
        return self.db.execute_query(query)

    def select_by(self, keyword):
        query = "SELECT * from mon_hoc WHERE (ma_mon = %s OR ten_mon LIKE %s) AND trang_thai = 1"
        return self.db.execute_query(query, (keyword, f"%{keyword}%"))

    def insert(self, ma_mon, ten_mon, so_tin_chi, khoa):
        query = "INSERT INTO mon_hoc (ma_mon, ten_mon, so_tin_chi, khoa, trang_thai) VALUES (%s, %s, %s, %s, 1)"
        return self.db.execute_commit(query, (ma_mon, ten_mon, so_tin_chi, khoa))

    def update(self, ma_mon, ten_mon, so_tin_chi, khoa):
        query = "UPDATE mon_hoc SET ten_mon = %s, so_tin_chi = %s, khoa = %s WHERE ma_mon = %s"
        return self.db.execute_commit(query, (ten_mon, so_tin_chi, khoa, ma_mon))

    def delete(self, ma_mon):
        query = "UPDATE mon_hoc SET trang_thai = 0 WHERE ma_mon = %s"
        return self.db.execute_commit(query, (ma_mon,))

    def check_exists(self, ma_mon):
        query = "SELECT COUNT(*) FROM mon_hoc WHERE ma_mon = %s"
        result = self.db.execute_query(query, (ma_mon,))
        count = result[0]['COUNT(*)'] if result else 0
        return count > 0



