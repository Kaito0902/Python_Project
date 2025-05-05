# main.py (entry‐point của ứng dụng)
import sys, os, customtkinter as ctk
from views.diem_view    import DiemView
from views.thongke_view import ThongKeView

# thêm project root để import modules
sys.path.insert(0, os.path.dirname(__file__))

def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Điểm Sinh Viên")
    app.geometry("900x650")

    tabs = ctk.CTkTabview(app)
    tabs.pack(fill="both", expand=True, padx=20, pady=20)

    tabs.add("Quét điểm")
    DiemView(tabs.tab("Quét điểm")).pack(fill="both", expand=True)

    tabs.add("Thống kê")
    ThongKeView(tabs.tab("Thống kê")).pack(fill="both", expand=True)

    app.mainloop()

if __name__ == "__main__":
    main()
