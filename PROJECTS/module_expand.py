import streamlit as st
import numpy as np
import pandas as pd
import mysql.connector
from mysql.connector import pooling, Error
import PROJECTS.config as module_config
import PROJECTS.module_view as module_view
import bcrypt

@st.cache_data
def load_data():
    conn = module_config.connect_to_mysql()
    try:
        users = module_view.query_to_dataframe(f"SELECT id,username,line,role,display_name,ma_nv FROM users WHERE role!= 'admin';", conn)
        users = list(users.to_records(index=False))
        return users
    finally:
        conn.close()


def delete_user_by_id(user_id):
    try:
        conn = module_config.connect_to_mysql()
        cursor = conn.cursor()
        delete_query = "DELETE FROM users WHERE id = %s"
        cursor.execute(delete_query, (user_id,))
        conn.commit()
        return True
    except Error as e:
        st.error(f"Lỗi khi xóa người dùng: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
def update_user_by_id(user_id, line, username, display_name, role, ma_nv):
    try:
        conn = module_config.connect_to_mysql()
        cursor = conn.cursor()
        update_query = """
            UPDATE users
            SET line = %s, username = %s, display_name = %s, role = %s, ma_nv = %s
            WHERE id = %s
        """
        cursor.execute(update_query, (line, username, display_name, role,ma_nv, user_id))
        conn.commit()
        return True
    except Error as e:
        st.error(f"Lỗi khi cập nhật người dùng: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
def add_user(username, display_name, role, line, password, ma_nv):
    try:
        conn = module_config.connect_to_mysql()
        cursor = conn.cursor()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        insert_query = """
            INSERT INTO users (username, display_name, role, line, password,ma_nv)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (username, display_name, role, line, hashed_password, ma_nv))
        conn.commit()
        return True
    except Error as e:
        st.error(f"Lỗi khi thêm người dùng: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()