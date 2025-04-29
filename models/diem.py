import os
import logging
from tensorflow.keras.models import load_model
from resources.models_ai.preprocess import preprocess_image
from resources.models_ai.predict import predict_score_from_image
from .database import Database
from config import MODEL_PATH, THRESHOLDS

class DiemModel:
    def __init__(self):
        self.db = Database()
        if not os.path.exists(MODEL_PATH):
            msg = f"Không tìm thấy mô hình AI tại {MODEL_PATH}"
            logging.error(msg)
            raise FileNotFoundError(msg)
        try:
            self.ai_model = load_model(MODEL_PATH)
        except Exception as e:
            logging.error(f"Tải mô hình AI thất bại: {e}")
            raise RuntimeError("Tải mô hình AI thất bại.")

    def trich_xuat(self, path: str) -> tuple:
        if not os.path.isfile(path):
            raise FileNotFoundError("Ảnh đầu vào không tồn tại.")
        img = preprocess_image(path)
        res = predict_score_from_image(self.ai_model, img)
        if not res or 'mssv' not in res or 'diem' not in res:
            raise ValueError("Dữ liệu AI không hợp lệ.")
        return res['mssv'], float(res['diem'])

    def lay_diem_kiem_tra(self, mssv, ma_mon):
        rows = self.db.execute_query(
            "SELECT diem_kiem_tra FROM diem WHERE mssv=%s AND ma_mon=%s", (mssv, ma_mon)
        )
        return float(rows[0]['diem_kiem_tra']) if rows else 0.0

    def cap_nhat_diem(self, mssv, ma_mon, kt, ck, tk, xl):
        exists = self.db.execute_query(
            "SELECT 1 FROM diem WHERE mssv=%s AND ma_mon=%s", (mssv, ma_mon)
        )
        if exists:
            sql = ("UPDATE diem SET diem_kiem_tra=%s, diem_cuoi_ky=%s, diem_tong_ket=%s, xep_loai=%s "
                   "WHERE mssv=%s AND ma_mon=%s")
            params = (kt, ck, tk, xl, mssv, ma_mon)
        else:
            sql = ("INSERT INTO diem (mssv, ma_mon, diem_kiem_tra, diem_cuoi_ky, diem_tong_ket, xep_loai) "
                   "VALUES (%s, %s, %s, %s, %s, %s)")
            params = (mssv, ma_mon, kt, ck, tk, xl)
        return self.db.execute_commit(sql, params) > 0

    def lay_ds_mon_hoc(self):
        return self.db.execute_query("SELECT ma_mon, ten_mon FROM mon_hoc")

    def lay_diem_theo_mon(self, ma_mon):
        return self.db.execute_query(
            "SELECT mssv, diem_kiem_tra, diem_cuoi_ky, diem_tong_ket, xep_loai "
            "FROM diem WHERE ma_mon=%s", (ma_mon,)
        )

    def lay_si_so(self, ma_mon):
        rows = self.db.execute_query(
            "SELECT COUNT(*) AS si_so FROM dang_ky dk "
            "JOIN lop l ON dk.ma_lop=l.ma_lop WHERE l.ma_mon=%s", (ma_mon,)
        )
        return int(rows[0]['si_so']) if rows else 0