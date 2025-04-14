
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

# import mysql.connector
#
# def connect_db():
#     try:
#         connection = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="khanh",
#             database="quan_ly_sinh_vien"
#         )
#         if connection.is_connected():
#             print("✅ Kết nối MySQL thành công!")
#         return connection
#     except mysql.connector.Error as err:
#         print(f"❌ Lỗi kết nối MySQL: {err}")
#         return None
#
    # def execute_query(query, params=None, fetch=False, commit=False):
    #     conn = connect_db()
    #     if not conn:
    #         return None
    #
    #     cursor = conn.cursor(dictionary=True, buffered=True)
    #     try:
    #         cursor.execute(query, params or ())
    #
    #         if fetch:
    #             result = cursor.fetchall()
    #         elif commit:
    #             conn.commit()
    #             result = cursor.rowcount
    #         else:
    #             result = None
    #
    #         return result
    #     except mysql.connector.Error as err:
    #         print(f"❌ Lỗi SQL: {err}")
    #         return None
    #     finally:
    #         cursor.close()
    #         conn.close()

