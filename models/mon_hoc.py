from .database import get_connection
"""
Model tương tác bảng mon_hoc.
"""
def fetch_mon_hoc() -> list:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT ma_mon, ten_mon FROM mon_hoc ORDER BY ma_mon')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
