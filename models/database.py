import mysql.connector
from mysql.connector import pooling
import logging
from config import DB_CONFIG
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
class Database:
    """
    Kết nối MySQL với connection pool.
    """
    def __init__(self):
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name=DB_CONFIG.get('pool_name'),
                pool_size=int(DB_CONFIG.get('pool_size')),
                host=DB_CONFIG.get('host'),
                port=int(DB_CONFIG.get('port')),
                user=DB_CONFIG.get('user'),
                password=DB_CONFIG.get('password'),
                database=DB_CONFIG.get('database'),
                charset='utf8mb4'
            )
        except Exception as e:
            logging.error(f"DB pool init error: {e}")
            raise
    def execute_query(self, sql, params=None):
        conn = self.pool.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params or ())
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Query error: {e} -- SQL: {sql} % {params}")
            raise
        finally:
            cursor.close()
            conn.close()
    def execute_commit(self, sql, params=None):
        conn = self.pool.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            logging.error(f"Commit error: {e} -- SQL: {sql} % {params}")
            raise
        finally:
            cursor.close()
            conn.close()