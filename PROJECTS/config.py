import mysql.connector
from mysql.connector import pooling, Error
from mysql.connector import OperationalError, InternalError
import mysql.connector.pooling
import streamlit as st
from st_pages import Page, Section, hide_pages, add_page_title, get_nav_from_toml
import os
import base64
import time
from mysql.connector.errors import PoolError
from st_social_media_links import SocialMediaIcons

# PATH FOR DATABASE

def create_db_pool():
    if "db_pool" not in st.session_state or st.session_state.db_pool:
        st.session_state.db_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="my_pool_vnpt",
            pool_size=10,
            pool_reset_session=True,
            host='103.200.23.68',
            user='samryvnc_anhemtamke',
            password='Tamke@123',
            database='samryvnc_vnpt_performance_insights'
        )

# Hàm lấy kết nối từ pool


def connect_to_mysql():
    retries = 5
    delay = 2
    for _ in range(retries):
        try:
            return st.session_state.db_pool.get_connection()
        except PoolError:
            print("Connection pool exhausted. Retrying...")
            time.sleep(delay)
    raise Exception("Failed to get connection from pool after several retries.")


    
def check_connection(conn):
    try:
        if conn.unread_result:
            conn.cursor().fetchall() 
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchall() 
        cursor.close()
        return True
            
    except IndexError as e:
        print(f"Lỗi IndexError khi truy vấn: {e}")
        return False
    except (OperationalError, InternalError) as e:
        print(f"Lỗi kết nối hoặc lỗi đọc kết quả: {e}")
        return False
    except Exception as e:
        print(f"Lỗi không xác định: {e}")
        return False
def reconnect_if_needed():
    if not is_connection_alive(st.session_state.db_pool):
        del st.session_state.db_pool
        create_db_pool()
        conn = connect_to_mysql()


def is_connection_alive(conn):
    try:
        conn.ping(reconnect=True)
        return True
    except:
        return False
  
# PATH FOR UI DESIGN
@st.dialog("Lựa chọn")
def show_confirmation_dialog(item):
    if "dialog_open" not in st.session_state:
        st.session_state.dialog_open = False
    if "confirmation" not in st.session_state:
        st.session_state.confirmation = None
    if st.session_state.dialog_open:
            st.write(f"🤔 Bạn có chắc chắn muốn {item} không❓")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Đồng ý", key="yes_confirm", use_container_width=True):
                    st.session_state.confirmation = "Yes"
                    st.session_state.dialog_open = False
                    st.rerun()
            with col2:
                if st.button("Từ chối", key="no_confirm", use_container_width=True):
                    st.session_state.confirmation = "No"
                    st.session_state.dialog_open = False
                    st.rerun()

def get_relative_file_path(path_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_file_path = os.path.join(current_dir, path_name)
    with open(full_file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_image
def social_media_show():
    social_media_links = [
        "https://www.facebook.com/",
        "https://www.linkedin.com/",
        "https://discord.com/",
        "https://www.github.com/"
    ]

    social_media_icons = SocialMediaIcons(social_media_links)
    social_media_icons.render()

def add_sidebar_footer():
    container_sidebar_button_setting = st.sidebar.container(key="container_sidebar_button_setting")
    with container_sidebar_button_setting:
        cols_button_setting_sidebar = st.columns([1,8,8,1])
        with cols_button_setting_sidebar[1]:
            if st.button("Log out", icon=":material/logout:", key="logout_from_app",type="secondary",):
                st.session_state.is_logged_in = False
                st.session_state.role_access_admin = False
                st.session_state.line_access = None
                st.session_state.usernamevnpt = None
                st.rerun()
        with cols_button_setting_sidebar[2]:
            if st.button("Connect", icon=":material/settings_backup_restore:", key="reconnect_db", type="secondary",):
                st.session_state.db_pool = None
                reconnect_if_needed()
                st.rerun()
    container_side_bar_footer = st.sidebar.container(key="container_side_bar_footer")
    image_footer_logo = get_relative_file_path("../src/vnpt.png")
    
    with container_side_bar_footer:
        st.markdown(f"""
                    <image src="data:image/png;base64,{image_footer_logo}" style="width: 30%;border-radius:50px;"/>
                    <h3 style='font-size: 18px;text-align:center;'>LIÊN HỆ</h3>
                    <p style='font-size:14px;text-align:center;'><svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="rgb(0, 50, 73)"><path d="M215.74-144Q186-144 165-165.15 144-186.3 144-216v-384q0-29.7 21.12-50.85Q186.23-672 215.88-672h71.89v-72q0-29.7 21.11-50.85Q330-816 359.73-816h216.2q29.73 0 50.9 21.15Q648-773.7 648-744v216h96q29.7 0 50.85 21.15Q816-485.7 816-456v240q0 29.7-21.15 50.85Q773.7-144 744-144H528v-144h-96v144H215.74Zm.26-72h72v-72h-72v72Zm0-156h72v-72h-72v72Zm0-156h72v-72h-72v72Zm144 156h72v-72h-72v72Zm0-156h72v-72h-72v72Zm0-144h72v-72h-72v72Zm144 300h72v-72h-72v72Zm0-156h72v-72h-72v72Zm0-144h72v-72h-72v72Zm168 456h72v-72h-72v72Zm0-156h72v-72h-72v72Z"/></svg> Trung tâm VNPT Hồ Chí Minh</p>
                    <p style='font-size:14px;text-align:center;'><svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="rgb(0, 50, 73)"><path d="M480-191q119-107 179.5-197T720-549q0-105-68.5-174T480-792q-103 0-171.5 69T240-549q0 71 60.5 161T480-191Zm0 72q-13 0-24.5-4.5T433-137q-40-35-86.5-82T260-320q-40-54-66-112.5T168-549q0-134 89-224.5T480-864q133 0 222.5 90.5T792-549q0 58-26.5 117t-66 113q-39.5 54-86 100.5T527-137q-11 9-22.5 13.5T480-119Zm0-433Zm0 72q30 0 51-21t21-51q0-30-21-51t-51-21q-30 0-51 21t-21 51q0 30 21 51t51 21Z"/></svg> 142 Điện Biên Phủ - Đa Kao - Q1</p>
                    <p style='font-size:14px;text-align:center;'><svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="rgb(0, 50, 73)"><path d="M480.28-96Q401-96 331-126t-122.5-82.5Q156-261 126-330.96t-30-149.5Q96-560 126-629.5q30-69.5 82.5-122T330.96-834q69.96-30 149.5-30t149.04 30q69.5 30 122 82.5T834-629.28q30 69.73 30 149Q864-401 834-331t-82.5 122.5Q699-156 629.28-126q-69.73 30-149 30Zm-.28-72q130 0 221-91t91-221q0-130-91-221t-221-91q-130 0-221 91t-91 221q0 130 91 221t221 91Zm0-312Zm-72 168h144q20.4 0 34.2-13.8Q600-339.6 600-360v-36q0-15.3-10.29-25.65Q579.42-432 564.21-432t-25.71 10.35Q528-411.3 528-396v12h-96v-192h96v12q0 15.3 10.29 25.65Q548.58-528 563.79-528t25.71-10.35Q600-548.7 600-564v-36q0-20.4-13.8-34.2Q572.4-648 552-648H408q-20.4 0-34.2 13.8Q360-620.4 360-600v240q0 20.4 13.8 34.2Q387.6-312 408-312Z"/></svg> VNPT VinaPhone ©2024</p>
                    
                    """, unsafe_allow_html=True)
        st.markdown("---")
        social_media_show()
        st.markdown("""
                    <style>
                    .st-key-container_sidebar_button_setting{
                        margin-top: 20px;
                    }
                    .st-key-container_sidebar_button_setting p{
                        font-weight: bold;
                        font-size: 0.8rem;
                    }
                    .st-key-container_side_bar_footer{
                        background-color: rgb(120, 189, 243);
                        border-radius: 15px;  
                        padding: 10px 0px; 
                        text-align:center;
                    }
                    
                    </style>
                    """, unsafe_allow_html=True)

