"""
Tiện ích khởi tạo và thao tác cơ sở dữ liệu từ file SQL.
"""
import os
import mysql.connector
from utils.config import DB_CONFIG

def init_database(schema_file: str):

    cfg = DB_CONFIG
    conn = mysql.connector.connect(
        host=cfg['host'], port=int(cfg['port']),
        user=cfg['user'], password=cfg['password'],
        database=cfg['database'], charset='utf8mb4'
    )
    cursor = conn.cursor()
    with open(schema_file, 'r', encoding='utf-8') as f:
        sql_commands = f.read().split(';')
    for cmd in sql_commands:
        cmd = cmd.strip()
        if cmd:
            cursor.execute(cmd)
    conn.commit()
    cursor.close()
    conn.close()