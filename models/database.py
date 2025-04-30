import mysql.connector
from mysql.connector import pooling
import logging
from utils.config import DB_CONFIG

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

class Database:
    """
    Connection pool cho MySQL.
    """
    def __init__(self):
        self.pool = pooling.MySQLConnectionPool(
            pool_name=DB_CONFIG['pool_name'],
            pool_size=int(DB_CONFIG['pool_size']),
            host=DB_CONFIG['host'],
            port=int(DB_CONFIG['port']),
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            charset='utf8mb4'
        )

    def execute_query(self, sql, params=None):
        conn = self.pool.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params or ())
            return cursor.fetchall()
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
        finally:
            cursor.close()
            conn.close()