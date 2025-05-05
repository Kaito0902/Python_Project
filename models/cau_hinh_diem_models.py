from models.database import Database

class CauHinhDiemModels:
    def __init__(self):
        self.db = Database()

    def select_all(self, ma_lop):
        query = "SELECT * from cau_hinh_diem WHERE ma_lop = %s"
        return self.db.execute_query(query, (ma_lop,))

    def insert(self, ma_lop, ten_cot_diem, trong_so):
        try:

            # Lấy id bằng SELECT
            query_insert = "INSERT INTO cau_hinh_diem (ma_lop, ten_cot_diem, trong_so) VALUES (%s, %s, %s)"
            self.db.execute_commit(query_insert, (ma_lop, ten_cot_diem, trong_so))

            # Lấy id dựa trên ma_lop và ten_cot_diem (đã đảm bảo tính duy nhất)
            query_select_id = "SELECT id FROM cau_hinh_diem WHERE ma_lop = %s AND ten_cot_diem = %s"
            result = self.db.execute_query(query_select_id, (ma_lop, ten_cot_diem))

            if result:
                id_cot_diem = result[0]['id']

                query_sv = """
                                SELECT mssv FROM dang_ky WHERE ma_lop = %s
                            """
                ds_sinh_vien = self.db.execute_query(query_sv, (ma_lop,))

                for sinh_vien in ds_sinh_vien:
                    mssv = sinh_vien['mssv']
                    query_insert_diem = """
                                    INSERT INTO chi_tiet_diem (mssv, id_cot_diem, diem) 
                                    VALUES (%s, %s, 0)
                                """
                    self.db.execute_commit(query_insert_diem, (mssv, id_cot_diem))
                return True
            else:
                return False  # Không tìm thấy id (trường hợp rất hiếm khi đã insert thành công)

        except Exception as e:
            print(f"Lỗi khi thêm cấu hình điểm: {str(e)}")
            return False

    def delete(self, id):
        try:
            # Xóa các dòng liên quan trong chi_tiet_diem trước
            query_delete_diem = "DELETE FROM chi_tiet_diem WHERE id_cot_diem = %s"
            self.db.execute_commit(query_delete_diem, (id,))

            query = "DELETE FROM cau_hinh_diem WHERE id = %s"
            self.db.execute_commit(query, (id,))
            return True

        except Exception as e:
            print(f"Lỗi khi xóa cấu hình điểm: {e}")
            return False

    def update(self, id, ma_lop, ten_cot_diem, trong_so):
        query = """
            UPDATE cau_hinh_diem 
            SET ma_lop = %s, ten_cot_diem = %s, trong_so = %s 
            WHERE id = %s
        """
        return self.db.execute_commit(query, (ma_lop, ten_cot_diem, trong_so, id))

    def get_total_trong_so(self, ma_lop):
        query = "SELECT SUM(trong_so) FROM cau_hinh_diem WHERE ma_lop = %s"
        result = self.db.execute_query(query, (ma_lop,))
        print("Result from database:", result)

        if result and result[0] and result[0]['SUM(trong_so)'] is not None:
            return result[0]['SUM(trong_so)']  # Dùng key 'SUM(trong_so)'
        else:
            return 0

    def get_trong_so_by_id(self, id):
        query = "SELECT trong_so FROM cau_hinh_diem WHERE id = %s"
        result = self.db.execute_query(query, (id,))
        if result and result[0] and result[0]['trong_so'] is not None:  # Kiểm tra cẩn thận
            return result[0]['trong_so']
        else:
            return 0

    def is_ten_cot_diem_exists(self, ma_lop, ten_cot_diem):
        query = "SELECT * FROM cau_hinh_diem WHERE ma_lop = %s AND ten_cot_diem = %s"
        result = self.db.execute_query(query, (ma_lop, ten_cot_diem))
        return bool(result)

