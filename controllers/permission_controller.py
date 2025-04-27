from models.permission_models import PermissionModels

class PermissionController:
    def __init__(self):
        self.permission_model = PermissionModels()

    def lay_quyen_theo_vai_tro(self, vai_tro_id):
        """
        Lấy danh sách quyền theo vai trò.
        :param vai_tro_id: ID vai trò.
        :return: Danh sách quyen_id.
        """
        return self.permission_model.get_permissions_for_role(vai_tro_id)
