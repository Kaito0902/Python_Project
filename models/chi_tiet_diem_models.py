from models.database import Database

class ChiTietDiemModels:
    def __init__(self):
        self.db = Database()

    def select_all(self):
        query = "SELECT * from chi_tiet_diem"
        return self.db.execute_query(query)

    def insert(self, id, mssv, id_cot_diem, diem):
        query = "INSERT INTO chi_tiet_diem (id, mssv, id_cot_diem, diem) VALUES (%d, %s, %d, %f)"
        return self.db.execute_commit(query, (id, mssv, id_cot_diem, diem))
