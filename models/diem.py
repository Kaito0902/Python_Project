
import os
from tensorflow.keras.models import load_model
from resources.models_ai.preprocess import preprocess_image
from resources.models_ai.predict import predict_score_from_image
from models.database import Database
from utils.config import MODEL_PATH

class DiemModel:
    """Xử lý AI và CRUD bảng diem"""
    def __init__(self):
        self.db = Database()
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Không tìm thấy model tại {MODEL_PATH}")
        self.ai_model = load_model(MODEL_PATH)

    def trich_xuat(self, path: str):
        """Nhận diện MSSV và điểm CK từ ảnh."""
        if not os.path.isfile(path):
            raise FileNotFoundError("Ảnh không tồn tại")
        img = preprocess_image(path)
        res = predict_score_from_image(self.ai_model, img)
        # giả sử predict_score_from_image trả về dict {'mssv':..., 'diem': ...}
        return res['mssv'], float(res['diem'])

    def lay_diem_kiem_tra(self, mssv, ma_mon):
        rows = self.db.execute_query(
            "SELECT diem_kiem_tra FROM diem WHERE mssv=%s AND ma_mon=%s",
            (mssv, ma_mon)
        )
        return float(rows[0]['diem_kiem_tra']) if rows else 0.0

    def cap_nhat_diem(self, mssv, ma_mon, kt, ck, tk, xl):
        exists = self.db.execute_query(
            "SELECT 1 FROM diem WHERE mssv=%s AND ma_mon=%s",
            (mssv, ma_mon)
        )
        if exists:
            sql = (
                "UPDATE diem SET diem_kiem_tra=%s, diem_cuoi_ky=%s, "
                "diem_tong_ket=%s, xep_loai=%s WHERE mssv=%s AND ma_mon=%s"
            )
            params = (kt, ck, tk, xl, mssv, ma_mon)
        else:
            sql = (
                "INSERT INTO diem "
                "(mssv, ma_mon, diem_kiem_tra, diem_cuoi_ky, diem_tong_ket, xep_loai) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            params = (mssv, ma_mon, kt, ck, tk, xl)
        return self.db.execute_commit(sql, params) > 0
