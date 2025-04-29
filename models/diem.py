from .database import get_connection
"""
Model tương tác bảng diem.
"""
def get_diem_kiemtra(mssv: str, ma_mon: str) -> float:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'SELECT diem_kiem_tra FROM diem WHERE mssv=%s AND ma_mon=%s',
        (mssv, ma_mon)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return float(row[0]) if row else None
def save_final_score(mssv: str, ma_mon: str,
                     diem_kt: float, diem_ck: float,
                     diem_tk: float, xep_loai: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS diem (
            mssv VARCHAR(20),
            ma_mon VARCHAR(20),
            diem_kiem_tra FLOAT,
            diem_cuoi_ky FLOAT,
            diem_tong_ket FLOAT,
            xep_loai VARCHAR(20),
            PRIMARY KEY (mssv, ma_mon)
        )
    """)
    cur.execute(
        """
        INSERT INTO diem(mssv, ma_mon, diem_kiem_tra, diem_cuoi_ky,
                         diem_tong_ket, xep_loai)
        VALUES(%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
          diem_kiem_tra=VALUES(diem_kiem_tra),
          diem_cuoi_ky=VALUES(diem_cuoi_ky),
          diem_tong_ket=VALUES(diem_tong_ket),
          xep_loai=VALUES(xep_loai)
        """,
        (mssv, ma_mon, diem_kt, diem_ck, diem_tk, xep_loai)
    )
    conn.commit()
    cur.close()
    conn.close()