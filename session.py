# session.py
from controllers.AuthManager import lay_quyen

# Khởi tạo thông tin phiên mặc định, sử dụng key "vai_tro_id"
current_user = {
    "ma_nguoi_dung": None,
    "username": None,
    "vai_tro_id": None
}

# Biến toàn cục để lưu thông tin quyền của người dùng
current_user_permissions = {}

def set_current_user(ma_nguoi_dung, username, vai_tro):
    global current_user, current_user_permissions
    current_user["ma_nguoi_dung"] = ma_nguoi_dung
    current_user["username"] = username
    current_user["vai_tro_id"] = vai_tro
    # Lấy quyền dựa trên vai trò (vai_tro) và cập nhật current_user_permissions in-place.
    current_user_permissions.clear()
    current_user_permissions.update(lay_quyen(vai_tro))

def clear_session():
    global current_user, current_user_permissions
    current_user["ma_nguoi_dung"] = None
    current_user["username"] = None
    current_user["vai_tro_id"] = None
    current_user_permissions.clear()

def get_current_user():
    return current_user