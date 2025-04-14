from models.sinh_vien import SinhVienModels

class SinhVienController:
    def __init__(self):
        self.model = SinhVienModels()

    def get_students_data(self):
        try:
            return self.model.select_all()
        except Exception as e:
            print(f"Lỗi khi lấy danh sách sinh viên: {e}")
            return []

    def add_student_db(self, mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email):
        try:
            return self.model.insert(mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email)
        except Exception as e:
            print(f"Lỗi khi thêm sinh viên: {e}")
            return False

    def update_student_db(self, mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email):
        try:
            return self.model.update(mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email)
        except Exception as e:
            print(f"Lỗi khi cập nhật sinh viên: {e}")
            return False

    def delete_student_db(self, mssv):
        try:
            return self.model.delete(mssv)
        except Exception as e:
            print(f"Lỗi khi xóa sinh viên: {e}")
            return False

    def search_student_db(self, keyword):
        try:
            return self.model.select_by(keyword)
        except Exception as e:
            print(f"Lỗi khi tìm kiếm sinh viên: {e}")
            return []
