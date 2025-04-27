from models.database import Database

class PermissionModels:
    def __init__(self):
        self.db = Database()

    def get_permissions_for_role(self, vai_tro_id):
        """
        Lấy danh sách quyền (quyen_id) dành cho vai trò có id = vai_tro_id.
        :param vai_tro_id: id của vai trò trong bảng vai_tro.
        :return: Danh sách các giá trị quyen_id.
        """
        query = "SELECT quyen_id FROM phan_quyen WHERE vai_tro_id = %s"
        rows = self.db.execute_query(query, (vai_tro_id,))

        # Nếu có dữ liệu thì map ra list quyền, không thì trả về list rỗng
        permissions = [row['quyen_id'] for row in rows] if rows else []
        return permissions
