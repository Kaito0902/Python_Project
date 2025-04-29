import tkinter as tk
from tkinter import ttk, messagebox
from utils.helpers import get_db_connection
"""
Giao diện hiển thị danh sách điểm và thống kê theo môn.
"""
def show_diem_list(ma_mon: str):
    win = tk.Toplevel()
    win.title(f'Danh sách điểm - {ma_mon}')
    win.geometry('600x400')
    try:
        conn = get_db_connection()
    except Exception as e:
        messagebox.showerror('DB Error', str(e))
        return
    cur = conn.cursor()
    cur.execute(
        'SELECT mssv, diem_kiem_tra, diem_cuoi_ky, diem_tong_ket, xep_loai '
        'FROM diem WHERE ma_mon=%s ORDER BY mssv', (ma_mon,)
    )
    rows = cur.fetchall()
    cur.close(); conn.close()
    # Thống kê
    scores = [r[3] for r in rows]
    total = len(scores)
    pass_count = sum(1 for s in scores if s >= 5.0)
    fail_count = total - pass_count
    avg_score = sum(scores)/total if total else 0.0
    stats = f"Đậu: {pass_count}    Rớt: {fail_count}    TB: {avg_score:.2f}"
    tk.Label(win, text=stats, font=('Arial',12,'bold')).pack(pady=5)
    # Bảng chi tiết
    cols = ('mssv','diem_kt','diem_ck','diem_tk','xep_loai')
    tv = ttk.Treeview(win, columns=cols, show='headings')
    for c,h in zip(cols,['MSSV','Điểm KT','Điểm CK','Điểm TK','Xếp loại']):
        tv.heading(c,text=h)
        tv.column(c,width=100,anchor='center')
    tv.pack(fill='both',expand=True)
    for r in rows:
        tv.insert('', 'end', values=r)