from models.database import Database

class CauHinhDiemModels:
    def __init__(self):
        self.db = Database()

    def select_all(self, ma_lop):
        query = "SELECT * from cau_hinh_diem WHERE ma_lop = %s"
        return self.db.execute_query(query, (ma_lop,))

    def insert(self, ma_lop, ten_cot_diem, trong_so):
        query = "INSERT INTO cau_hinh_diem (ma_lop, ten_cot_diem, trong_so) VALUES (%s, %s, %s)"
        return self.db.execute_commit(query, (ma_lop, ten_cot_diem, trong_so))

    def delete(self, id):
        query = "DELETE FROM cau_hinh_diem WHERE id = %s"
        return self.db.execute_commit(query, (id,))

    def update(self, id, ma_lop, ten_cot_diem, trong_so):
        query = """
            UPDATE cau_hinh_diem 
            SET ma_lop = %s, ten_cot_diem = %s, trong_so = %s 
            WHERE id = %s
        """
        return self.db.execute_commit(query, (ma_lop, ten_cot_diem, trong_so, id))

