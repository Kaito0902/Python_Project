import mysql.connector
from mysql.connector import Error as MySQLError
"""
Module chứa các helper chung: kết nối DB, phân loại điểm.
"""
# Cấu hình DB chung
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234567',
    'database': 'doanpt'
}
def get_db_connection():
    """Kết nối MySQL và trả về connection."""
    try:
        return mysql.connector.connect(**db_config)
    except MySQLError as e:
        raise
def classify_score(score: float) -> str:
    """Phân loại điểm tổng kết theo thang điểm."""
    if score >= 8.5:
        return 'Giỏi'
    if score >= 7.0:
        return 'Khá'
    if score >= 5.0:
        return 'Trung bình'
    return 'Yếu'