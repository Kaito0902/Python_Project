import mysql.connector

class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        """Kết nối đến database và trả về đối tượng connection."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="quan_ly_diem"
            )
            print("✅ Kết nối Database thành công!")
            return conn
        except mysql.connector.Error as err:
            print(f"❌ Lỗi kết nối Database: {err}")
            return None

    def execute_query(self, query, values=None):
        """Thực thi câu lệnh INSERT, UPDATE, DELETE"""
        conn = self.connect()
        if not conn:
            print("❌ Chưa kết nối đến database!")
            return False
        try:
            cursor = conn.cursor()
            cursor.execute(query, values) if values else cursor.execute(query)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"❌ Lỗi thực thi query: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def fetch_all(self, query, values=None):
        """Thực thi SELECT và trả về danh sách kết quả"""
        conn = self.connect()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)  # Đảm bảo con trỏ có dictionary=True
            cursor.execute(query, values) if values else cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"❌ Lỗi lấy dữ liệu: {err}")
            return []
        finally:
            cursor.close()
            conn.close()
