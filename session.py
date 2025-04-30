from controllers.AuthManager import lay_quyen

current_user = {"ma_nguoi_dung": None, "username": None, "vai_tro_id": None}  # 🔥 Khởi tạo mặc định
if current_user["vai_tro_id"] is not None:
    current_user_permissions = lay_quyen(current_user["vai_tro_id"])
else:
    current_user_permissions = {}


# session.py
current_user = {
    "ma_nguoi_dung": None,
    "username": None,
    "vai_tro": None
}

def set_current_user(ma_nguoi_dung, username, vai_tro):
    global current_user
    current_user["ma_nguoi_dung"] = ma_nguoi_dung
    current_user["username"] = username
    current_user["vai_tro"] = vai_tro

def clear_session():
    global current_user
    current_user = {
        "ma_nguoi_dung": None,
        "username": None,
        "vai_tro": None
    }
