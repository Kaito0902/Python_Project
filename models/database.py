from utils.helpers import get_db_connection
"""
Module quản lý kết nối DB chung cho models.
"""
def get_connection():
    return get_db_connection()