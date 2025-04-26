
import mysql.connector
import logging
class Database:
    def __init__(self):
        self.conn = None
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="qldsv"
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("✅ Kết nối database thành công!")
        except mysql.connector.Error as e:
            logging.error("❌ Lỗi kết nối MySQL!", exc_info=True)

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            logging.error("❌ Lỗi truy vấn SQL!", exc_info=True)

    def execute_commit(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()
            return self.cursor.rowcount
        except mysql.connector.Error as e:
            logging.error("❌ Lỗi thực thi SQL!", exc_info=True)

    def close(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("✅ Đã đóng kết nối database!")