import os
import mysql.connector
from mysql.connector import Error

# Lấy thông tin kết nối từ biến môi trường
AIVEN_CONFIG = {
    "host": os.environ.get("AIVEN_DB_HOST"),
    "user": os.environ.get("AIVEN_DB_USER"),
    "password": os.environ.get("AIVEN_DB_PASSWORD"),
    "database": os.environ.get("AIVEN_DB_NAME"),
    "port": int(os.environ.get("AIVEN_DB_PORT", 3306)),
}

CPANEL_CONFIG = {
    "host": os.environ.get("CPANEL_DB_HOST"),
    "user": os.environ.get("CPANEL_DB_USER"),
    "password": os.environ.get("CPANEL_DB_PASSWORD"),
    "database": os.environ.get("CPANEL_DB_NAME"),
    "port": 3306,
}

def connect_db(config):
    """Tạo kết nối CSDL duy nhất"""
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except Error as e:
        print(f"❌ Lỗi kết nối CSDL: {e}")
        return None

def get_all_tables(cursor):
    """Lấy danh sách tất cả các bảng (với dictionary=True)"""
    cursor.execute("SHOW TABLES")
    return [list(table.values())[0] for table in cursor.fetchall()]


def get_all_data(cursor, tables):
    """Lấy dữ liệu của tất cả các bảng một lần"""
    all_data = {}
    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        all_data[table] = cursor.fetchall()
    return all_data

def get_table_columns(cursor, table_name):
    """Lấy danh sách cột của bảng (cursor có dictionary=True)"""
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    return [col["Field"] for col in cursor.fetchall()]

def batch_insert(cursor, table_name, columns, data, batch_size=500):
    """Xóa dữ liệu cũ của bảng đích và chèn dữ liệu mới theo batch."""
    if not data:
        return

    # 1️⃣ Tắt khóa ngoại nếu cần
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")

    # 2️⃣ Xóa toàn bộ dữ liệu cũ (dùng TRUNCATE nếu không có khóa ngoại)
    cursor.execute(f"DELETE FROM {table_name}")

    # 3️⃣ Tạo truy vấn INSERT
    placeholders = ", ".join(["%s"] * len(columns))
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    # 4️⃣ Nếu là bảng `users`, tắt trigger trước khi chèn
    if table_name == 'users':
        cursor.execute("SET SESSION sql_mode='NO_ENGINE_SUBSTITUTION,NO_AUTO_CREATE_USER'")

    # 5️⃣ Chèn dữ liệu theo batch
    for i in range(0, len(data), batch_size):
        cursor.executemany(query, data[i:i + batch_size])

    # 6️⃣ Bật lại trigger nếu cần
    if table_name == 'users':
        cursor.execute("SET SESSION sql_mode=DEFAULT")

    # 7️⃣ Bật lại khóa ngoại
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")


def sync_data():
    """Hàm chính để đồng bộ dữ liệu"""
    aiven_conn = connect_db(AIVEN_CONFIG)
    cpanel_conn = connect_db(CPANEL_CONFIG)

    if not aiven_conn or not cpanel_conn:
        return

    aiven_cursor = aiven_conn.cursor(dictionary=True)
    cpanel_cursor = cpanel_conn.cursor()

    tables = get_all_tables(aiven_cursor)
    if not tables:
        print("❌ Không tìm thấy bảng nào!")
        return

    # Lấy toàn bộ dữ liệu từ Aiven trong một lượt
    all_data = get_all_data(aiven_cursor, tables)

    for table in tables:
        print(f"🚀 Đang đồng bộ bảng: {table}")

        columns = get_table_columns(aiven_cursor, table)
        if not columns:
            print(f"⚠️ Bỏ qua bảng {table} vì không lấy được cột.")
            continue

        data = [tuple(row[col] for col in columns) for row in all_data[table]]
        batch_insert(cpanel_cursor, table, columns, data)

        print(f"✅ Đã đồng bộ {len(data)} bản ghi vào bảng {table}.")

    cpanel_conn.commit()  # Chỉ commit một lần sau khi hoàn tất

    # Đóng kết nối
    aiven_cursor.close()
    cpanel_cursor.close()
    aiven_conn.close()
    cpanel_conn.close()
    print("🎉 Đồng bộ hoàn tất!")

if __name__ == "__main__":
    sync_data()
