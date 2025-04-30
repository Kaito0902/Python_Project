from models.database import Database

db = Database()  # 🔥 Khởi tạo đối tượng Database

def lay_quyen(vai_tro):
    query = "SELECT module, xem, them, sua, xoa, xem_nhat_ky, xem_chi_tiet_lop FROM quyen_han WHERE vai_tro = %s"
    rows = db.fetch_all(query, (vai_tro,))

    permissions = {}  # Chuyển đổi dữ liệu thành dạng từ điển
    for row in rows:
        permissions[row["module"]] = {
            "xem": row["xem"],
            "them": row["them"],
            "sua": row["sua"],
            "xoa": row["xoa"],
            "xem_nhat_ky": row["xem_nhat_ky"],
            "xem_chi_tiet_lop": row["xem_chi_tiet_lop"]
        }
    return permissions  # Trả về dictionary thay vì list