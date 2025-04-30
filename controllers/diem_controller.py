import logging
from models.diem import DiemModel
from utils.config import THRESHOLDS

class DiemController:
    """Logic quét ảnh, tính và lưu điểm theo môn học"""
    def __init__(self):
        self.model = DiemModel()

    def quet_va_lưu(self, path: str, ma_mon: str) -> dict:
        try:
            mssv, ck = self.model.trich_xuat(path)
            kt = self.model.lay_diem_kiem_tra(mssv, ma_mon)
            tk = round((kt + ck) / 2, 2)
            if tk >= THRESHOLDS['Gioi']:
                xl = 'Gioi'
            elif tk >= THRESHOLDS['Kha']:
                xl = 'Kha'
            elif tk >= THRESHOLDS['Trung binh']:
                xl = 'Trung binh'
            else:
                xl = 'Yeu'
            success = self.model.cap_nhat_diem(mssv, ma_mon, kt, ck, tk, xl)
            if not success:
                return None
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

        return self.model.lay_ds_mon_hoc()

    def lay_danh_sach_diem(self, ma_mon: str) -> list:

        return self.model.lay_diem_theo_mon(ma_mon)