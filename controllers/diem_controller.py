# controllers/diem_controller.py
import logging
from models.diem import DiemModel
from utils.config import THRESHOLDS

class DiemController:
    """Logic quét ảnh, tính và lưu điểm theo môn học"""
    def __init__(self):
        self.model = DiemModel()

    def quet_va_luu(self, path: str, ma_mon: str) -> dict:
        try:
            # inference AI
            mssv, ck = self.model.trich_xuat(path)
            # điểm kiểm tra lấy từ CSDL
            kt = self.model.lay_diem_kiem_tra(mssv, ma_mon)
            tk = round((kt + ck) / 2, 2)
            # phân loại dựa trên thresholds
            if   tk >= THRESHOLDS['Gioi']:        xl = 'Gioi'
            elif tk >= THRESHOLDS['Kha']:         xl = 'Kha'
            elif tk >= THRESHOLDS['Trung binh']:  xl = 'Trung binh'
            else:                                 xl = 'Yeu'

            success = self.model.cap_nhat_diem(mssv, ma_mon, kt, ck, tk, xl)
            if not success:
                raise RuntimeError(f"Cập nhật điểm thất bại cho MSSV={mssv}, môn={ma_mon}")

            return {
                'mssv': mssv,
                'diem_kiem_tra': kt,
                'diem_cuoi_ky': ck,
                'diem_tong_ket': tk,
                'xep_loai': xl
            }
        except Exception as e:
            logging.error(f"Lỗi quét và lưu: {e}")
            raise

    def lay_danh_sach_mon(self) -> list:
        return self.model.db.execute_query("SELECT ma_mon FROM mon_hoc")
