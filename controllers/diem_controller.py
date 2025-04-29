from models.diem import get_diem_kiemtra, save_final_score
from resources.models_ai.predict import predict_image
from utils.helpers import classify_score
"""
Controller xử lý luồng quét ảnh và lưu điểm.
"""
def process_scan(file_path: str, ma_mon: str) -> dict:
    mssv, diem_ck = predict_image(file_path)
    diem_kt = get_diem_kiemtra(mssv, ma_mon)
    if diem_kt is None:
        raise ValueError(f"Không tìm thấy điểm KT cho {mssv}, môn {ma_mon}")
    diem_tk = (diem_kt + diem_ck) * 0.5
    xep_loai = classify_score(diem_tk)
    save_final_score(mssv, ma_mon, diem_kt, diem_ck, diem_tk, xep_loai)
    return {
        'mssv': mssv,
        'diem_kt': diem_kt,
        'diem_ck': diem_ck,
        'diem_tk': diem_tk,
        'xep_loai': xep_loai
    }