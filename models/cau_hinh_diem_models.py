from models.database import Database

class CauHinhDiemModels:
    def __init__(self):
        self.db = Database()

    def select_all(self):
        query = "SELECT * from cau_hinh_diem"
        return self.db.execute_query(query)

    def insert(self, id, ma_lop, ten_cot_diem, trong_so):
        query = "INSERT INTO from cau_hinh_diem (id, ma_lop, ten_cot_diem, trong_so) VALUES (%d, %s, %s, %f)"
        return self.db.execute_commit(query, (id, ma_lop, ten_cot_diem, trong_so))

