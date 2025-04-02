import streamlit as st
import mysql.connector
from mysql.connector import pooling, Error
import EM_MODULE.config as module_config

def delete_plan(radio_process_plan,deleted_data):
    conn = module_config.connect_to_mysql()
    cursor = conn.cursor()
    try:
        for year_insert, line, loaidoanhthu in deleted_data:
            delete_query = """
            DELETE FROM kehoach_linelv
            WHERE year_insert = %s AND line = %s AND loaidoanhthu = %s AND type_process =%s
            """
            cursor.execute(delete_query, (year_insert, line, loaidoanhthu,radio_process_plan))
        conn.commit()
        return True
    except Error as e:
        st.error(f"Lỗi khi xóa dữ liệu: {e}")

def delete_thuchien_from_data(radio_process_make,deleted_data):
    conn = module_config.connect_to_mysql()
    cursor = conn.cursor()
    try:
        for thang, year_insert, loaidoanhthu in deleted_data:
            delete_query = """
            DELETE FROM thuchien
            WHERE thang = %s AND year_insert = %s AND loaidoanhthu = %s AND type_process =%s
            """
            cursor.execute(delete_query, (thang, year_insert, loaidoanhthu, radio_process_make))
        conn.commit()
        return True
    except Error as e:
        st.error(f"Lỗi khi xóa dữ liệu: {e}")