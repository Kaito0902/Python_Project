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
