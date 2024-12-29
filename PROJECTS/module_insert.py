import streamlit as st
import numpy as np
import pandas as pd
import mysql.connector
from mysql.connector import pooling, Error
import webbrowser
import PROJECTS.config as module_config


@st.cache_data
def load_data_service():
    conn = module_config.connect_to_mysql()
    query = "SELECT ma_dv_id66, ten_dv, danh_muc_tt FROM dichvu"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Tạo DataFrame từ kết quả
    df = pd.DataFrame(rows, columns=["ma_dv_id66", "ten_dv", "danh_muc_tt"])
    return df
def fetch_all_services(conn):
    query = "SELECT ma_dv_id66, ten_dv, danh_muc_tt FROM dichvu"
    try:
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except Error as e:
        print(f"Error: {e}")
        return []

def add_service_manage(ma_dv_id66,ten_dv,danh_muc_tt,conn):
    query = """
        INSERT INTO dichvu (ma_dv_id66, ten_dv, danh_muc_tt)
        VALUES (%s, %s, %s)
    """
    data = [(ma_dv_id66, ten_dv, danh_muc_tt)]
    try:
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.executemany(query, data)
            conn.commit()
            return True
    except Error as e:
        print(f"Error: {e}")
        return False
def update_service_manage(data,conn):
    query = """
        UPDATE dichvu
        SET ten_dv = %s, danh_muc_tt = %s
        WHERE ma_dv_id66 = %s
    """
    try:
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.executemany(query, data)
            conn.commit()
            return True
    except Error as e:
        print(f"Error: {e}")
        return False
def delete_service_manage(data,conn):
    query = """
        DELETE FROM dichvu
        WHERE ma_dv_id66 = %s
    """
    try:
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.executemany(query, data)
            conn.commit()
            return True
    except Error as e:
        print(f"Error: {e}")
        return False

# PART 2: INSERT DATA
    # PART 2.1: INSERT INTO KEHOACH
def query_dichvu_from_database(conn):
    cursor = conn.cursor()
    # đoạn code select
    query = "SELECT ma_dv_id66, ten_dv, danh_muc_tt FROM dichvu"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def select_rows_kehoach_for_insert(data, result_service):
    """
    Lọc các dòng từ DataFrame `data` với điều kiện giá trị trong cột `id_dv_606` nằm trong `nhom_dv_id`.
    """
    nhom_dv_id = pd.DataFrame(result_service, columns=["ma_dv_id66", "ten_dv", "danh_muc_tt"])
    nhom_dv_id = nhom_dv_id[nhom_dv_id["danh_muc_tt"].notna()]
    nhom_dv_id = nhom_dv_id[~nhom_dv_id["danh_muc_tt"].isin(["1", "1.1.01", "1.1.02", "1.1.03", "1.1.05", "1.1.06", "1.1.07"])]
    if 'id_dv_606' not in data.columns:
        raise ValueError("Cột 'id_dv_606' không tồn tại trong DataFrame.")

    
    if isinstance(nhom_dv_id, pd.DataFrame):
        nhom_dv_id = nhom_dv_id['ma_dv_id66'].tolist()  
    
   
    nhom_dv_id_clean = list(set(nhom_dv_id))
    
    
    subset = data[data['id_dv_606'].isin(nhom_dv_id_clean)]

    return subset

def insertData_kehoach_to_database(line, year,loaidoanhthu, data,conn):
    # Tạo một con trỏ để thực thi các câu lệnh SQL
    cursor = conn.cursor()
# Lặp qua từng hàng trong DataFrame
    for index, row in data.iterrows():
        # Câu lệnh SQL để insert dữ liệu
        sql = """INSERT INTO kehoach
                (ma_nv,id_dv_606,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,line,year_insert,loaidoanhthu, type_process)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        # Dữ liệu để insert, kết hợp với line và year
        data_to_insert = tuple(list(row[:14]) + [line, year,loaidoanhthu, st.session_state.type_process])
        
        # Thực thi câu lệnh SQL
        cursor.execute(sql, data_to_insert)
    
    # Commit các thay đổi vào cơ sở dữ liệu
    conn.commit()
    
    if cursor.rowcount > 0:
        return True
    else:
        return False

def update_table_kehoach(data_show_updated):
    conn = module_config.connect_to_mysql()
    cursor = conn.cursor()
    try:
        update_query = """
            UPDATE kehoach
            SET t1 = %s, t2 = %s, t3 = %s, t4 = %s, t5 = %s, t6 = %s, t7 = %s, t8 = %s, t9 = %s, t10 = %s, t11 = %s, t12 = %s
            WHERE id = %s
        """
        for index, row in data_show_updated.iterrows():
            cursor.execute(update_query, (
                row['t1'], row['t2'], row['t3'], row['t4'], row['t5'], row['t6'], 
                row['t7'], row['t8'], row['t9'], row['t10'], row['t11'], row['t12'], 
                row['id']
            ))
        conn.commit()
        return True
    except Error as e:
        return e
    finally:
        cursor.close()
        conn.close()

    
   
def query_kehoach_by_line_year(line_test, year_test,loaidoanhthu,conn):
    cursor = conn.cursor()

    # Thực hiện truy vấn SQL
    cursor.execute("SELECT * FROM kehoach WHERE line=%s AND year_insert=%s AND loaidoanhthu=%s AND type_process =%s;", (line_test, year_test,loaidoanhthu, st.session_state.type_process))
    rows = cursor.fetchall()

    # Tạo DataFrame từ các hàng
    kq_kehoach = pd.DataFrame(rows, columns=[col[0] for col in cursor.description])

    return kq_kehoach
def validate_columns(data):
    required_columns = ["ma_nv", "id_dv_606", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "t11", "t12"]
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        return missing_columns
    else:
        return False
# PART 2: THUCHIEN
def get_data_thuchien(thang, nam, line,loaidoanhthu,conn):
    cursor = conn.cursor()
    query = "SELECT nhom_dv, doanhthu, thang, year_insert, loaidoanhthu,line FROM thuchien WHERE thang=%s AND year_insert=%s AND line=%s AND loaidoanhthu=%s AND type_process=%s;"
    cursor.execute(query, (thang, nam, line, loaidoanhthu, st.session_state.type_process))
    
    # Lấy tất cả kết quả từ truy vấn
    rows_thuchien = cursor.fetchall()
    
    # Tạo DataFrame từ kết quả
    kq_thuchien = pd.DataFrame(rows_thuchien, columns=["nhom_dv", "doanh_thu", "thang", "year_insert", "loaidoanhthu","line"])
    kq_thuchien['nhom_dv'] = kq_thuchien['nhom_dv'].str.strip()
    
    # Trả về DataFrame
    return kq_thuchien
def group_data_for_insert_thuchien(data):
    grouped_data = data.groupby(['MA_NV', 'NHOM DV']).agg({'DOANH THU': 'sum'}).reset_index()
    return grouped_data
def validate_thuchien_columns(data):
    required_columns = ["MA_NV", "NHOM DV","DOANH THU"]
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        return missing_columns
    else:
        return False
def insert_data_to_thuchien(thang, nam,loaidoanhthu,line, group_data,conn):
    # Tạo một con trỏ để thực thi các câu lệnh SQL
    cursor = conn.cursor()
    
    # Lặp qua từng hàng trong DataFrame
    for index, row in group_data.iterrows():
        # Câu lệnh SQL để insert dữ liệu
        sql = """INSERT INTO thuchien
                (IDnhanvien, nhom_dv, doanhthu,line, thang, year_insert,loaidoanhthu, type_process)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        # Dữ liệu để insert, kết hợp với thang và nam
        data_to_insert = (row.iloc[0], row.iloc[1], row.iloc[2],line, thang, nam,loaidoanhthu, st.session_state.type_process)
        
        # Thực thi câu lệnh SQL
        cursor.execute(sql, data_to_insert)

    conn.commit()
    if cursor.rowcount > 0:
        cursor.close()
        return True
    else:
        cursor.close()
        return False
def get_data_preview_for_insert_database(line,year,loaidoanhthu,conn):
    cursor = conn.cursor()
    query = "SELECT DISTINCT(thang),line,year_insert,loaidoanhthu FROM thuchien WHERE year_insert =%s AND line=%s AND loaidoanhthu=%s AND type_process=%s;"
    cursor.execute(query, (year,line,loaidoanhthu, st.session_state.type_process))
    
    # Lấy tất cả kết quả từ truy vấn
    rows_thuchien = cursor.fetchall()
    
    # Tạo DataFrame từ kết quả
    kq_thuchien = pd.DataFrame(rows_thuchien, columns=["thang", "line", "year_insert", "loaidoanhthu"])
    kq_thuchien = kq_thuchien.rename(columns={"thang": "Tháng", "line": "Line", "year_insert": "Năm", "loaidoanhthu": "Loại doanh thu"})
    
    # Trả về DataFrame
    return kq_thuchien

def open_link(url):
    try:
        webbrowser.open(url, new=2)  # new=2 opens in a new tab, if possible
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
def load_local_file(file_path):
    """Đọc file từ hệ thống tệp."""
    try:
        with open(file_path, "rb") as file:
            return file.read()  # Đọc nội dung file dạng binary
    except FileNotFoundError:
        st.error(f"Không tìm thấy file: {file_path}")
        return None