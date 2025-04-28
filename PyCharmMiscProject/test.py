import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import numpy as np
import mysql.connector
from mysql.connector import Error
import onnxruntime as ort
# ==== 1. Cấu hình Database ====
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234567',         # đổi mật khẩu nếu có
    'database': 'doanpt'   # đổi tên database của bạn
}
def create_connection():
    try:
        return mysql.connector.connect(**db_config)
    except Error as e:
        messagebox.showerror("DB Error", f"Không thể kết nối MySQL:\n{e}")
        return None
conn = create_connection()
if conn is None:
    exit(1)
# ==== 2. Lấy danh sách môn học ====
def fetch_mon_hoc():
    try:
        cur = conn.cursor()
        cur.execute("SELECT ma_mon, ten_mon FROM mon_hoc ORDER BY ma_mon")
        rows = cur.fetchall()
        return rows
    except Error as e:
        messagebox.showwarning("DB Warning", f"Lỗi khi lấy môn học:\n{e}")
        return []
    finally:
        cur.close()
# ==== 3. Lấy điểm kiểm tra ====
def get_diem_kiemtra(mssv, ma_mon):
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT diem_kiem_tra FROM diem WHERE mssv=%s AND ma_mon=%s",
            (str(mssv), ma_mon)
        )
        r = cur.fetchone()
        return float(r[0]) if r else None
    except Error as e:
        messagebox.showwarning("DB Warning", f"Lỗi khi truy vấn điểm kiểm tra:\n{e}")
        return None
    finally:
        cur.close()
# ==== 4. Lưu kết quả ====
def save_final_score(mssv, ma_mon, diem_kt, diem_ck, diem_tk, xeploai):
    try:
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
        conn.commit()
        sql = """
            INSERT INTO diem (mssv, ma_mon, diem_kiem_tra, diem_cuoi_ky, diem_tong_ket, xep_loai)
            VALUES (%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
              diem_kiem_tra=VALUES(diem_kiem_tra),
              diem_cuoi_ky=VALUES(diem_cuoi_ky),
              diem_tong_ket=VALUES(diem_tong_ket),
              xep_loai=VALUES(xep_loai)
        """
        cur.execute(sql, (str(mssv), ma_mon, diem_kt, diem_ck, diem_tk, xeploai))
        conn.commit()
    except Error as e:
        messagebox.showwarning("DB Warning", f"Lỗi khi lưu kết quả:\n{e}")
    finally:
        cur.close()
# ==== 5. Xếp loại ====
def classify_score(score):
    if score >= 8.5:
        return "Giỏi"
    elif score >= 7.0:
        return "Khá"
    elif score >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"
# ==== 6. Load ONNX model hoặc thiết lập mặc định ====
model_path = 'path_to_your_model.onnx'
if os.path.exists(model_path):
    session = ort.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
else:
    session = None
# Hàm dự đoán
def predict_image(img_path):
    if session is None:
        # default khi không có model
        return 123456, 9.0
    img = Image.open(img_path).convert('RGB')
    img = img.resize((224, 224))
    arr = np.array(img).astype(np.float32) / 255.0
    arr = np.transpose(arr, (2, 0, 1))  # CHW
    arr = np.expand_dims(arr, axis=0)
    outputs = session.run([output_name], {input_name: arr})
    pred = outputs[0]
    mssv = int(pred[0][0])
    diem_ck = float(pred[0][1])
    return mssv, diem_ck
# ==== 7. Mở cửa sổ danh sách sinh viên ====
def view_list_for_mon(ma_mon):
    win = tk.Toplevel(root)
    win.title(f"Danh sách môn {ma_mon}")
    win.geometry("600x400")
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT mssv, diem_kiem_tra, diem_cuoi_ky, diem_tong_ket, xep_loai "
            "FROM diem WHERE ma_mon=%s ORDER BY mssv", (ma_mon,)
        )
        rows = cur.fetchall()
    except Error as e:
        messagebox.showwarning("DB Warning", f"Lỗi khi truy vấn danh sách điểm:\n{e}")
        cur.close()
        return
    finally:
        cur.close()
    scores = [r[3] for r in rows]
    total = len(scores)
    pass_count = sum(1 for s in scores if s >= 5.0)
    fail_count = total - pass_count
    avg_score = sum(scores) / total if total > 0 else 0.0
    stats_label = tk.Label(
        win,
        text=f"Đậu: {pass_count}    Rớt: {fail_count}    Điểm trung bình: {avg_score:.2f}",
        font=("Arial", 12, "bold"),
        pady=5
    )
    stats_label.pack()
    columns = ("mssv", "diem_kt", "diem_ck", "diem_tk", "xeploai")
    tv = ttk.Treeview(win, columns=columns, show="headings")
    for c, h in zip(columns, ["MSSV", "Điểm KT", "Điểm CK", "Điểm TK", "Xếp loại"]):
        tv.heading(c, text=h)
        tv.column(c, width=100, anchor="center")
    tv.pack(fill="both", expand=True)
    for row in rows:
        tv.insert("", "end", values=row)
# ==== 8. Giao diện chính ====
root = tk.Tk()
root.title("Quét MSSV & Quản lý Môn học")
root.geometry("600x800")
frame_courses = tk.LabelFrame(root, text="Danh sách Môn học")
frame_courses.pack(fill="both", padx=10, pady=5)
canvas = tk.Canvas(frame_courses)
scroll = tk.Scrollbar(frame_courses, orient="vertical", command=canvas.yview)
scrollable = tk.Frame(canvas)
scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable, anchor="nw")
canvas.configure(yscrollcommand=scroll.set, height=200)
canvas.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")
for ma, ten in fetch_mon_hoc():
    row = tk.Frame(scrollable)
    tk.Label(row, text=ma, width=12, anchor="w").pack(side="left", padx=5)
    tk.Label(row, text=ten, width=30, anchor="w").pack(side="left")
    tk.Button(row, text="Xem danh sách",
              command=lambda m=ma: view_list_for_mon(m)).pack(side="right", padx=5)
    row.pack(fill="x", pady=2)
panel = tk.Label(root)
panel.pack(padx=10, pady=10)
tk.Button(root, text="Chọn Ảnh", command=lambda: open_image()).pack(pady=5)
result_label = tk.Label(root, text="", font=("Arial", 14), justify="left")
result_label.pack(pady=10)
def open_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.png *.jpeg"), ("All files", "*.*")]    )
    if not file_path:
        return
    img = Image.open(file_path)
    img.thumbnail((300, 300))
    tkimg = ImageTk.PhotoImage(img)
    panel.config(image=tkimg)
    panel.image = tkimg
    try:
        mssv, diem_ck = predict_image(file_path)
        ma_mon = simpledialog.askstring("Mã môn", "Nhập Mã môn:")
        if not ma_mon:
            messagebox.showwarning("Thiếu thông tin", "Bạn phải nhập Mã môn.")
            return
        diem_kt = get_diem_kiemtra(mssv, ma_mon)
        if diem_kt is None:
            messagebox.showwarning(
                "Không tìm thấy",
                f"Không tìm thấy điểm kiểm tra của MSSV {mssv}, Môn {ma_mon}."
            )
            return
        diem_tk = (diem_kt + diem_ck) * 0.5
        xeploai = classify_score(diem_tk)
        save_final_score(mssv, ma_mon, diem_kt, diem_ck, diem_tk, xeploai)
        result_label.config(text=(
            f"MSSV: {mssv}\n"
            f"Môn: {ma_mon}\n"
            f"Điểm CK: {diem_ck:.2f}\n"
            f"Điểm TK: {diem_tk:.2f}\n"
            f"Xếp loại: {xeploai}\n\n"
            "✔ Đã lưu vào DB."
        ))
    except Exception as e:
        messagebox.showerror("Error", f"Có lỗi:\n{e}")
root.mainloop()
