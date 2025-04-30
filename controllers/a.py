import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # 🔥 Thêm thư mục cha vào sys.path

from controllers.user_controller import UserController  # 🔥 Đảm bảo chữ thường đúng tên file

controller = UserController()
permissions = controller.get_module_permissions("admin", "mon_hoc")
print(permissions)
