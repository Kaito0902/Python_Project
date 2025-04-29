import logging
import pandas as pd
from models.diem import DiemModel
from config import THRESHOLDS

class DiemController:
    def __init__(self):
        self.model = DiemModel()

    def quet_va_lưu(self, path, ma_mon):
        try:
            mssv, ck = self.model.trich_xuat(path)
            kt = self.model.lay_diem_kiem_tra(mssv, ma_mon)
            tk = round((kt + ck) / 2, 2)
            if tk >= THRESHOLDS['Gioi']: xl = 'Gioi'
            elif tk >= THRESHOLDS['Kha']: xl = 'Kha'
            elif tk >= THRESHOLDS['Trung binh']: xl = 'Trung binh'
            else: xl = 'Yeu'
            ok = self.model.cap_nhat_diem(mssv, ma_mon, kt, ck, tk, xl)
            return None if not ok else {'mssv': mssv, 'diem_kiem_tra': kt, 'diem_cuoi_ky': ck, 'diem_tong_ket': tk, 'xep_loai': xl}
        except Exception as e:
            logging.error(f"Lỗi quét và lưu: {e}")
            raise

    def lay_danh_sach_mon(self):
        return self.model.lay_ds_mon_hoc()

    def lay_danh_sach_diem(self, ma_mon):
        return self.model.lay_diem_theo_mon(ma_mon)

    def tinh_thong_ke(self, ma_mon):
        ds = self.model.lay_diem_theo_mon(ma_mon)
        si_so = self.model.lay_si_so(ma_mon)
        if not ds:
            return {'si_so': si_so, 'so_dau': 0, 'so_rot': 0, 'diem_tb': 0.0}
        so_dau = sum(1 for r in ds if r['diem_tong_ket'] >= 5)
        return {'si_so': si_so, 'so_dau': so_dau, 'so_rot': len(ds)-so_dau, 'diem_tb': round(sum(r['diem_tong_ket'] for r in ds)/len(ds),2)}

    def export_excel(self, ma_mon, file_path):
        pd.DataFrame(self.lay_danh_sach_diem(ma_mon)).to_excel(file_path, index=False)
        return file_path