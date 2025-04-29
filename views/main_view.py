import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from controllers.mon_hoc_controller import MonHocController
from controllers.diem_controller import process_scan
from views.diem_view import show_diem_list
"""
Giao diện chính: chọn môn, quét ảnh, hiển thị kết quả.
"""
def main():
    root = tk.Tk()
    root.title('Quét Điểm Sinh Viên')
    root.geometry('600x700')
    # Danh sách môn học
    frame = tk.LabelFrame(root, text='Danh sách Môn học')
    frame.pack(fill='x', padx=10, pady=5)
    canvas = tk.Canvas(frame, height=180)
    scrollbar = tk.Scrollbar(frame, orient='vertical', command=canvas.yview)
    scrollable = tk.Frame(canvas)
    scrollable.bind(
        '<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
    )
    canvas.create_window((0,0), window=scrollable, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    for ma, ten in MonHocController.list_mon_hoc():
        row = tk.Frame(scrollable)
        tk.Label(row, text=ma, width=10, anchor='w').pack(side='left')
        tk.Label(row, text=ten, width=30, anchor='w').pack(side='left')
        tk.Button(row, text='Xem', command=lambda m=ma: show_diem_list(m)).pack(side='right')
        row.pack(fill='x', pady=2)
    # Panel ảnh và kết quả
    panel = tk.Label(root)
    panel.pack(pady=10)
    result = tk.Label(root, text='', font=('Arial',12), justify='left')
    result.pack(pady=5)
    def on_scan():
        file_path = filedialog.askopenfilename(filetypes=[('Image files','*.jpg;*.png;*.jpeg')])
        if not file_path: return
        img = tk.PhotoImage(file=file_path)
        panel.config(image=img); panel.image=img
        ma_mon = simpledialog.askstring('Mã môn','Nhập mã môn:')
        if not ma_mon: return
        try:
            r = process_scan(file_path, ma_mon)
            result.config(text=(
                f"MSSV: {r['mssv']}\n"
                f"Điểm KT: {r['diem_kt']:.2f}\n"
                f"Điểm CK: {r['diem_ck']:.2f}\n"
                f"Điểm TK: {r['diem_tk']:.2f}\n"
                f"Xếp loại: {r['xep_loai']}"
            ))
        except Exception as e:
            messagebox.showerror('Error', str(e))
    tk.Button(root, text='Chọn Ảnh', command=on_scan).pack(pady=5)
    root.mainloop()
if __name__ == '__main__':
    main()