from models.lop import LopModels

class LopController:
    def __init__(self):
        self.lop_models = LopModels()
        
    def add_class(self, ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv):
        try:
            if not self.lop_models.is_valid_mon(ma_mon):
                return False, "Môn học không tồn tại hoặc đã bị xóa."

            existing_class = self.lop_models.get_by_ma_lop(ma_lop)
            if existing_class:
                if int(existing_class['trang_thai']) == 0:
                    restored = self.lop_models.restore(ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv)
                    return (restored, "Lớp học đã được cập nhập thành công.") if restored else (False, "Không thể thêm lớp học.")
                else:
                    return False, "Lớp học đã tồn tại và đang hoạt động."
            else:
                inserted = self.lop_models.insert(ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv)
                return (inserted, "Thêm lớp học thành công.") if inserted else (False, "Không thể thêm lớp học.")
        except Exception as e:
            return False, f"Lỗi khi thêm lớp học: {str(e)}"
    
    def update_class(self, ma_lop, ma_mon, so_luong, hoc_ky, nam):
        try:
            if not self.lop_models.is_valid_mon(ma_mon):
                return False, "Môn học không tồn tại hoặc đã bị xóa."
            
            updated = self.lop_models.update(ma_lop, ma_mon, so_luong, hoc_ky, nam)
            return (updated, "Cập nhật lớp học thành công.") if updated else (False, "Không thể cập nhật lớp học.")
        except Exception as e:
            return False, f"Lỗi khi cập nhật lớp học: {str(e)}"

    def select_all(self):
        try:
            return self.lop_models.select_all()
        except Exception as e:
            print(f"Lỗi khi lấy danh sách lớp: {e}")
            return []
        
    def get_students_in_class(self, ma_lop):
        try:
            return self.lop_models.get_students_in_class(ma_lop)
        except Exception as e:
            print(f"Lỗi khi lấy danh sách sinh viên trong lớp: {e}")
            return []

    def get_by_ma_lop(self, ma_lop):
        try:
            return self.lop_models.get_by_ma_lop(ma_lop)
        except Exception as e:
            print(f"Lỗi khi lấy thông tin lớp có mã : {e}")
            return []
        
    def delete(self, ma_lop):
        try:
            self.lop_models.delete(ma_lop)
            return True
        except Exception as e:
            print(f"Lỗi khi xóa lớp: {e}")
            return False

    def search_class(self, keyword):
        try:
            return self.lop_models.select_by(keyword)
        except Exception as e:
            print(f"Lỗi khi tìm lớp: {e}")
            return []
        
    def is_class_available(self, ma_lop):
        try:
            result = self.lop_models.is_class_available(ma_lop)
            if result:
                so_luong = result[0]['so_luong']
                da_dang_ky = result[0]['da_dang_ky']
                return da_dang_ky < so_luong
            return True
        except Exception as e:
            print(f"Lỗi kiểm tra số lượng lớp {ma_lop} thất bại: {e}")
            return False

    def is_student_registered(self, mssv, ma_lop):
        try:
            return self.lop_models.is_student_registered(mssv, ma_lop)
        except Exception as e:
            print(f"Lỗi kiểm tra sinh viên {mssv} đã đăng ký lớp {ma_lop} thất bại: {e}")
            return False

    def register_student_to_class(self, mssv, ma_lop):
        try:
            return self.lop_models.register_student_to_class(mssv, ma_lop)
        except Exception as e:
            print(f"[Lỗi] Khi đăng ký sinh viên {mssv} vào lớp {ma_lop}: {e}")
            return False
            
    def huy_dang_ky(self, mssv, ma_lop):
        try:
            return self.lop_models.huy_dang_ky(mssv, ma_lop)
        except Exception as e:
            print(f"Lỗi khi hủy đăng ký sinh viên khỏi lớp: {e}")
            return False

    def danh_sach_gv(self, ma_lop):
            try:
                return self.lop_models.danh_sach_gv_theo_khoa(ma_lop)
            except Exception as e:
                print(f"Lỗi khi lấy danh sách giảng viên: {e}")
                return False
        
    def phan_cong_gv(self, ma_lop, ma_gv):
        try:
            return self.lop_models.phan_cong_giang_vien(ma_lop, ma_gv)
        except Exception as e:
            print(f"Lỗi khi phân công giảng viên: {e}")
            return False

    def them(self):
        try:
            return self.lop_models.them()
        except Exception as e:
            print(f"Lỗi khi thêm: {e}")
            return False

