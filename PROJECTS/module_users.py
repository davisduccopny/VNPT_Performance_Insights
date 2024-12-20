import streamlit as st
import numpy as np
import pandas as pd
import mysql.connector
from mysql.connector import pooling, Error
from mysql.connector import OperationalError, InternalError
import PROJECTS.config as module_config
import bcrypt

@st.cache_data
def load_data_for_user(username):
    conn = module_config.connect_to_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, line, role, display_name, ma_nv FROM users WHERE username = %s;", (username,))
        users = cursor.fetchall()
        users = pd.DataFrame(users, columns=["id", "username", "line", "role", "display_name", "ma_nv"])
        if users.empty:
            return False
        return users
    finally:
        conn.close()
def change_password(username, old_pass, new_pass):
    conn = module_config.connect_to_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s;", (username,))
        result = cursor.fetchone()
        if result is None:
            return False
        
        stored_password = result[0]
        if not bcrypt.checkpw(old_pass.encode('utf-8'), stored_password.encode('utf-8')):
            return False
        
        hashed_new_pass = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("UPDATE users SET password = %s WHERE username = %s;", (hashed_new_pass, username))
        conn.commit()
        return True
    except (OperationalError, InternalError, Error) as e:
        st.error(f"Error: {e}")
        return False
    finally:
        conn.close()
def change_profile(username, display_name, line, ma_nv):
    conn = module_config.connect_to_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET display_name = %s, line = %s, ma_nv = %s WHERE username = %s;", (display_name, line, ma_nv, username))
        conn.commit()
        return True
    except (OperationalError, InternalError, Error) as e:
        st.error(f"Error: {e}")
        return False
    finally:
        conn.close()
def delete_user(username):
    conn = module_config.connect_to_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s;", (username,))
        conn.commit()
        return True
    except (OperationalError, InternalError, Error) as e:
        st.error(f"Error: {e}")
        return False
    finally:
        conn.close()
        
@st.cache_data
def load_action_check_user(line):
    conn = module_config.connect_to_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ch.username,li.ten_line, ch.action_content, ch.time_action FROM check_action_user as ch JOIN line_manage as li ON ch.line = li.ma_line WHERE ch.line = %s;", (line,))
        actions = cursor.fetchall()
        actions = pd.DataFrame(actions, columns=["username", "line", "action_content", "time_action"])
        return actions
    except (OperationalError, InternalError, Error) as e:
        st.error(f"Error: {e}")
        return False
    finally:
        conn.close()
def insert_action_check_user(username, line, action):
    conn = module_config.connect_to_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO check_action_user (username,line, action_content) VALUES (%s, %s, %s);", (username, line, action))
        conn.commit()
        return True
    except (OperationalError, InternalError, Error) as e:
        st.error(f"Error: {e}")
        return False
    finally:
        conn.close()