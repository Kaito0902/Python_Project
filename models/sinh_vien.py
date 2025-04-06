class SinhVien:
    def __init__(self, mssv, ho_ten, lop, khoa, ngay_sinh, gioi_tinh, que, email):
        self.mssv = mssv
        self.ho_ten = ho_ten
        self.lop = lop
        self.khoa = khoa
        self.ngay_sinh = ngay_sinh  
        self.gioi_tinh = gioi_tinh
        self.que = que
        self.email = email

    def to_dict(self):
        return {
            "mssv": self.mssv,
            "ho_ten": self.ho_ten,
            "lop": self.lop,
            "khoa": self.khoa,
            "ngay_sinh": self.ngay_sinh,
            "gioi_tinh": self.gioi_tinh,
            "que": self.que,
            "email": self.email,
        }
