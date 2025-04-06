import mysql.connector

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="khanh",
            database="quan_ly_sinh_vien"
        )
        if connection.is_connected():
            print("✅ Kết nối MySQL thành công!")
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Lỗi kết nối MySQL: {err}")
        return None

def execute_query(query, params=None, fetch=False, commit=False):
    conn = connect_db()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute(query, params or ())

        if fetch:
            result = cursor.fetchall()  
        elif commit:
            conn.commit()
            result = cursor.rowcount 
        else:
            result = None

        return result
    except mysql.connector.Error as err:
        print(f"❌ Lỗi SQL: {err}")
        return None
    finally:
        cursor.close()
        conn.close()
