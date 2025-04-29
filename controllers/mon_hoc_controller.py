from models.mon_hoc import fetch_mon_hoc
"""
Controller cho danh sách môn học.
"""
class MonHocController:
    @staticmethod
    def list_mon_hoc() -> list:
        return fetch_mon_hoc()