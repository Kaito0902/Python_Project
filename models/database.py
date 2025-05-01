
import mysql.connector
import logging
class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None  # Khởi tạo con trỏ nhưng chưa gán giá trị

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="qldsv"
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("✅ Kết nối database thành công!")
            return self.conn  # Đảm bảo trả về kết nối đã khởi tạo
        except mysql.connector.Error as e:
            logging.error("❌ Lỗi kết nối MySQL!", exc_info=True)
            self.conn = None  # Đảm bảo gán `None` nếu có lỗi
            self.cursor = None  # Đảm bảo `cursor` cũng được reset nếu có lỗi

            return None

    def execute_query(self, query, values=None, commit=False):
        """Thực thi SELECT hoặc INSERT, UPDATE, DELETE"""
        conn = self.conn or self.connect()  # Dùng kết nối hiện có hoặc tạo mới
        if not conn:
            print("❌ Chưa kết nối đến database!")
            return False

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, values or ())

            if commit:
                conn.commit()
                return True
            else:
                return cursor.fetchall()
        except mysql.connector.Error as e:
            logging.error(f"❌ Lỗi SQL: {e}", exc_info=True)
            return False if commit else []
        finally:
            if cursor:
                cursor.close()


    def execute_commit(self, query, params=None):
        conn = self.conn or self.connect()  # Dùng kết nối hiện có hoặc tạo mới
        if not conn:
            print("❌ Chưa kết nối đến database!")
            return False

        try:
            cursor = conn.cursor(dictionary=True)  # Lấy con trỏ mới
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.rowcount
        except mysql.connector.Error as e:
            logging.error("❌ Lỗi thực thi SQL!", exc_info=True)
            return False
        finally:
            if cursor:
                cursor.close()  # Đảm bảo đóng con trỏ sau khi dùng

    def fetch_all(self, query, params=None):
        """Thực thi SELECT và trả về danh sách kết quả"""
        conn = self.conn or self.connect()  # Dùng kết nối hiện có hoặc tạo mới
        if not conn:
            print("❌ Chưa kết nối đến database!")
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)  # Đảm bảo dữ liệu trả về dạng dictionary
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            return result  # Trả về danh sách kết quả

        except mysql.connector.Error as err:
            print(f"❌ Lỗi lấy dữ liệu: {err}")
            return []

        finally:
            if cursor:
                cursor.close()  # Đóng con trỏ, nhưng giữ kết nối để tránh mất phiên làm việc

    def fetch_one(self, query, params=None):
        """Thực thi truy vấn & lấy một kết quả."""
        conn = self.conn or self.connect()  # 🔥 Đảm bảo có kết nối
        if not conn or not self.cursor:  # 🔥 Kiểm tra nếu cursor chưa khởi tạo
            print("❌ Không thể thực thi query: Cursor hoặc kết nối bị None!")
            return None

        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"❌ Lỗi SQL: {err}")
            return None
        finally:
            if self.cursor:
                self.cursor.close() 
        
    def close(self):
        if self.conn:
            self.conn.close()
            print("✅ Đã đóng kết nối database!")

