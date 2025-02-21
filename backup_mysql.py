import os
import mysql.connector
from mysql.connector import Error


# Lấy thông tin kết nối từ biến môi trường
AIVEN_CONFIG = {
    "host": os.environ.get("AIVEN_DB_HOST"),
    "user": os.environ.get("AIVEN_DB_USER"),
    "password": os.environ.get("AIVEN_DB_PASSWORD"),
    "database": os.environ.get("AIVEN_DB_NAME"),
    "port": os.environ.get("AIVEN_DB_PORT", 3306),
}

CPANEL_CONFIG = {
    "host": os.environ.get("CPANEL_DB_HOST"),
    "user": os.environ.get("CPANEL_DB_USER"),
    "password": os.environ.get("CPANEL_DB_PASSWORD"),
    "database": os.environ.get("CPANEL_DB_NAME"),
    "port":  3306,
}


def get_table_list():
    """Lấy danh sách tất cả các bảng từ MySQL Aiven"""
    try:
        conn = mysql.connector.connect(**AIVEN_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        conn.close()
        return tables
    except Error as e:
        print(f"Lỗi khi lấy danh sách bảng: {e}")
        return []


def get_data_from_table(table_name):
    """Lấy dữ liệu từ một bảng trong MySQL Aiven"""
    try:
        conn = mysql.connector.connect(**AIVEN_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error as e:
        print(f"Lỗi khi lấy dữ liệu từ bảng {table_name}: {e}")
        return None


def get_table_columns(table_name):
    """Lấy danh sách các cột của bảng từ MySQL Aiven"""
    try:
        conn = mysql.connector.connect(**AIVEN_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [col[0] for col in cursor.fetchall()]
        cursor.close()
        conn.close()
        return columns
    except Error as e:
        print(f"Lỗi khi lấy danh sách cột của bảng {table_name}: {e}")
        return []


def insert_data_to_cpanel(table_name, data, batch_size=500):
    """Chèn dữ liệu vào MySQL trên cPanel nhanh hơn bằng batch insert"""
    if not data:
        print(f"Không có dữ liệu để đồng bộ cho bảng {table_name}.")
        return

    columns = get_table_columns(table_name)
    if not columns:
        print(f"Bỏ qua bảng {table_name} vì không lấy được danh sách cột.")
        return

    try:
        conn = mysql.connector.connect(**CPANEL_CONFIG)
        cursor = conn.cursor()

        # Tắt trigger trước khi chèn dữ liệu (nếu cần)
        if table_name == 'users':
            cursor.execute("SET SESSION sql_mode='NO_ENGINE_SUBSTITUTION,NO_AUTO_CREATE_USER'")

        # Tạo câu lệnh INSERT/REPLACE động
        placeholders = ", ".join(["%s"] * len(columns))
        insert_query = f"REPLACE INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        # Chuyển dữ liệu thành danh sách tuple
        values = [tuple(row[col] for col in columns) for row in data]

        # Chia nhỏ dữ liệu thành từng batch để tránh quá tải
        total_records = len(values)
        for i in range(0, total_records, batch_size):
            batch = values[i:i + batch_size]
            cursor.executemany(insert_query, batch)
            conn.commit()  # Commit từng batch
            print(f"Đã chèn {len(batch)} bản ghi vào bảng {table_name} ({i + len(batch)}/{total_records})")

        # Bật lại trigger sau khi chèn xong
        if table_name == 'users':
            cursor.execute("SET SESSION sql_mode=DEFAULT")

        cursor.close()
        conn.close()
        print(f"✅ Hoàn tất đồng bộ {total_records} bản ghi vào bảng {table_name}.")
    except Error as e:
        print(f"❌ Lỗi khi chèn dữ liệu vào bảng {table_name}: {e}")




def main():
    tables = get_table_list()
    if not tables:
        print("Không tìm thấy bảng nào để đồng bộ.")
        return

    for table in tables:
        print(f"Đồng bộ bảng: {table}")
        data = get_data_from_table(table)
        insert_data_to_cpanel(table, data)


if __name__ == "__main__":
    main()
