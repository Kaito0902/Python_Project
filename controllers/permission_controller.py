from models.database import Database

class PermissionController:
    def __init__(self):
        self.db = Database()

    def get_permissions_for_role(self, vai_tro_id):
        """
        Lấy danh sách quyền (quyen_id) dành cho vai trò có id = vai_tro_id.
        :param vai_tro_id: id của vai trò trong bảng vai_tro.
        :return: Danh sách các giá trị quyen_id.
        """
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT quyen_id FROM phan_quyen WHERE vai_tro_id = %s"
        cursor.execute(query, (vai_tro_id,))
        rows = cursor.fetchall()
        permissions = [row['quyen_id'] for row in rows]
        cursor.close()
        conn.close()
        return permissions
