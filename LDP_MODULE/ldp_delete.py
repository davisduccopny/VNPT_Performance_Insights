import streamlit as st
import mysql.connector
from mysql.connector import pooling, Error
import PROJECTS.config as module_config

def delete_plan(radio_process_plan,deleted_data):
    try:
        conn = module_config.connect_to_mysql()
        cursor = conn.cursor()
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
    finally:
        if conn.is_connected():
            cursor.close()

def delete_thuchien_from_data(radio_process_make,deleted_data):
    try:
        conn = module_config.connect_to_mysql()
        cursor = conn.cursor()
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
    finally:
        if conn.is_connected():
            cursor.close()