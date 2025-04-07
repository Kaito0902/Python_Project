class Lop:
    def __init__(self, ma_lop, ma_mon, so_luong, hoc_ky, nam, ma_gv):
        self.ma_lop = ma_lop
        self.ma_mon = ma_mon
        self.so_luong = so_luong
        self.hoc_ky = hoc_ky
        self.nam = nam
        self.ma_gv = ma_gv

    def to_dict(self):
        return {
            "ma_lop": self.ma_lop,
            "ma_mon": self.ma_mon,
            "so_luong": self.so_luong,
            "hoc_ky": self.hoc_ky,
            "nam": self.nam,
            "ma_gv": self.ma_gv,
        }
