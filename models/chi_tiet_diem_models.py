from models.database import Database

class ChiTietDiemModels:
    def __init__(self):
        self.db = Database()

    def select_all(self, ma_lop):
        query = """
        SELECT ctd.*, chd.ten_cot_diem, chd.trong_so
        FROM chi_tiet_diem ctd
        JOIN sinh_vien sv ON ctd.mssv = sv.mssv
        JOIN dang_ky dk ON sv.mssv = dk.mssv
        JOIN cau_hinh_diem chd ON dk.ma_lop = chd.ma_lop AND ctd.id_cot_diem = chd.id
        WHERE dk.ma_lop = %s
        """
        return self.db.execute_query(query, (ma_lop,))

    def insert(self, id, mssv, id_cot_diem, diem):
        query = "INSERT INTO chi_tiet_diem (id, mssv, id_cot_diem, diem) VALUES (%s, %s, %s, %f)"
        return self.db.execute_commit(query, (id, mssv, id_cot_diem, diem))

    def update(self, id, mssv, id_cot_diem, diem):
        query = """
            UPDATE chi_tiet_diem 
            SET mssv = %s, id_cot_diem = %s, diem = %s 
            WHERE id = %s
        """
        return self.db.execute_commit(query, (mssv, id_cot_diem, diem, id))