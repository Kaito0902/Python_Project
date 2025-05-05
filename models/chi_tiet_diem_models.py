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

    def get_by_mssv_and_column(self, ma_lop, mssv, ten_cot_diem):
        query = """
        SELECT ctd.*
        FROM chi_tiet_diem ctd
        JOIN cau_hinh_diem chd ON ctd.id_cot_diem = chd.id
        WHERE ctd.ma_lop = %s AND ctd.mssv = %s AND chd.ten_cot_diem = %s
        """
        return self.db.execute_query(query, (ma_lop, mssv, ten_cot_diem), fetch_one=True)

    def update(self, mssv, id_cot_diem, diem):
        query = """
        UPDATE chi_tiet_diem ctd
        SET ctd.diem = %s
        WHERE ctd.mssv = %s AND ctd.id_cot_diem = %s
        """
        self.db.execute_commit(query, (diem, mssv, id_cot_diem))

    def insert(self, ma_lop, mssv, ten_cot_diem, diem):
        # Lấy id_cot_diem từ tên cột điểm
        query = "SELECT id FROM cau_hinh_diem WHERE ma_lop = %s AND ten_cot_diem = %s"
        id_cot_diem = self.db.execute_query(query, (ma_lop, ten_cot_diem), fetch_one=True)

        if not id_cot_diem:
            raise Exception(f"Cột điểm '{ten_cot_diem}' không tồn tại trong cấu hình điểm")

        query = """
        INSERT INTO chi_tiet_diem (ma_lop, mssv, id_cot_diem, diem)
        VALUES (%s, %s, %s, %s)
        """
        self.db.execute_query(query, (ma_lop, mssv, id_cot_diem["id"], diem))