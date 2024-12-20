import bcrypt
import streamlit as st
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
import PROJECTS.config as config_project
import time


### PATH THAO TAC VOI DATABASE
def check_user_access(username, input_password, conn, cursor):
    '''Ham kiem tra xem nguoi dung co quyen truy cap hay khong'''
    
    cursor.execute("SELECT password, role, line,ma_nv FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    # Nếu tìm thấy user trong cơ sở dữ liệu
    if user:
        stored_password = user[0]  # Lấy mật khẩu đã mã hóa từ CSDL
        stored_role = user[1]
        line = user[2]# Lấy vai trò từ CSDL
        ma_nv = user[3]

        # Kiểm tra mật khẩu nhập vào có khớp với mật khẩu đã mã hóa không
        if bcrypt.checkpw(input_password.encode('utf-8'), stored_password.encode('utf-8')):
            return stored_role,line,ma_nv  # Trả về vai trò của người dùng
        else:
            return None,None,None  # Mật khẩu không đúng
    else:
        return None,None,None  # Tài khoản không tồn tại
def select_info_user(username,cursor):
    cursor.execute("SELECT username,password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    return user
def update_user_by_users(username_state, username,display_name, password, conn, cursor):
    '''Ham cap nhat thong tin nguoi dung boi chinh nguoi dung'''
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute(
        "UPDATE users SET username = %s,display_name = %s, password = %s WHERE username = %s",
        (username,display_name, hashed_password, username_state)
    )
    conn.commit()

    if cursor.rowcount == 0:
        return False  
    return True
def update_user_by_admin(username_state, username,display_name, password, line,role, conn, cursor):
    '''Ham cap nhat thong tin nguoi dung boi admin'''
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute(
        "UPDATE users SET username = %s,display_name = %s, password = %s, line= %s,role=%s WHERE username = %s",
        (username,display_name, hashed_password, line,role , username_state)
    )
    conn.commit()

    if cursor.rowcount == 0:
        return False  
    return True

### PATH THIET KE VA XU LY LOGIN
def login():
    container_login = st.container(key="container_login")
    with container_login:
        st.markdown("<h2 style='text-align: center;'> <i class='vnpt-icon'></i> VINAPHONE PERFORMANCE INSIGHTS</h2>", unsafe_allow_html=True)
        config_project.social_media_show()
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False
        st.session_state.role_access_admin = False
        st.session_state.line_access = None
        st.session_state.type_process = None
    background_image_login = config_project.get_relative_file_path("../src/for_style/302938672_434661178647430_3619299105774288951_n.jpg")
    icon_login_path = config_project.get_relative_file_path("../src/vnpt.png")
    st.markdown(f"""
            <style>
                [data-testid="stMainBlockContainer"]{{
                width: 100%;
                padding: 6rem 1rem 10rem;
                max-width: 46rem;

                }}
                [data-testid="stSidebar"] {{
                    display: none;
                }}
                .st-key-container_login {{
                    width: 100%;
                    box-shadow: -10px 5px 10px rgba(255, 255, 255, 0.1), 
                    10px 5px 10px rgba(255, 255, 255, 0.1), 
                    0px 10px 10px rgba(255, 255, 255, 0.1);
                    padding: 25px;
                    border-radius: 15px;
                    background: rgba(255, 255, 255, 0.8);
                }}
                .vnpt-icon {{
                    display: inline-block;
                    width: 1.65rem;
                    height: 1.65rem;
                    background-image: url('data:image/png;base64,{icon_login_path}');
                    background-size: contain;
                    background-repeat: no-repeat;
                }}
                [data-testid="stHeader"] {{
                    background: rgba(0,0,0,0);
                }}
                [data-testid="stAppViewContainer"] > .stMain {{
                    background-image: url("data:image/jpg;base64,{background_image_login}");
                    background-size: cover;
                    background-position: right;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
            </style>
            """, unsafe_allow_html=True)

    
    if not st.session_state.is_logged_in:
        with container_login.form(key="login_form",enter_to_submit=True, border=False):
            title_placeholder = st.empty()
            title_placeholder.subheader("Đăng nhập")
            username_placeholder = st.empty()
            password_placeholder = st.empty()
            success_placeholder = st.empty()
            username = username_placeholder.text_input("Tên người dùng", placeholder="Enter user name", key="username_login")
            password = password_placeholder.text_input("Mật khẩu", type="password", placeholder="Enter password", key="password_login")
            cols_login_type_process = st.columns([3,1])
            config_project.create_db_pool()
            toggle_login_type_process = cols_login_type_process[1].toggle("Login cấp phòng", value=False, key="toggle_login_type_process")
            with cols_login_type_process[0]:
                if cols_login_type_process[0].form_submit_button("🔓Đăng nhập",type="primary", help="Nhấn vào để đăng nhập!"):
                    with st.spinner('🔒 Đang kiểm tra thông tin đăng nhập...'):
                            time.sleep(2)  
                    if (username is not None and password is not None) and (username != '' and password != ''):
                        conn = config_project.connect_to_mysql()
                        cursor = conn.cursor()
                        user_role_mvnpt,line_access,ma_nv_access = check_user_access(username,password,conn,cursor)
                        if user_role_mvnpt and (user_role_mvnpt is not None):
                            if  toggle_login_type_process is True:
                                if user_role_mvnpt == 'admin':
                                    st.session_state.is_logged_in = True
                                    st.session_state.line_access = line_access
                                    st.session_state.role_access_admin = user_role_mvnpt
                                    st.session_state.usernamevnpt = username
                                    st.session_state.employee_id = ma_nv_access
                                    st.session_state.type_process = 'LDPVNPT'
                                    success_placeholder.success("✅ Đăng nhập thành công!")
                                    time.sleep(2)  
                                    title_placeholder.empty()
                                    username_placeholder.empty()
                                    password_placeholder.empty()
                                    success_placeholder.empty()
                                    st.rerun()
                                else:
                                    st.warning("❌ Bạn không có quyền truy cập vào hệ thống!")
                            else:
                                if line_access != 'LDPVNPT':
                                    st.session_state.is_logged_in = True
                                    st.session_state.line_access = line_access
                                    st.session_state.role_access_admin = user_role_mvnpt
                                    st.session_state.usernamevnpt = username
                                    st.session_state.employee_id = ma_nv_access
                                    st.session_state.type_process = 'LINE'
                                    success_placeholder.success("✅ Đăng nhập thành công!")
                                    time.sleep(2)  
                                    title_placeholder.empty()
                                    username_placeholder.empty()
                                    password_placeholder.empty()
                                    success_placeholder.empty()
                                    st.rerun()
                                else:
                                    st.warning("❌ Bạn không có quyền truy cập vào hệ thống!")
                                
                        else:
                            st.error("❌ Tên đăng nhập hoặc mật khẩu không đúng!")
                    else:
                        st.warning("❌ Vui lòng nhập tên đăng nhập và mật khẩu!")
        # with container_login:
        #     with st.spinner("🔍Đang khởi động..."):
        #         time.sleep(2)
        #     stream_text = st.empty()
        #     stream_text.write_stream(stream_data)
        #     time.sleep(1)
        #     stream_text.empty()
                    
_LOREM_IPSUM = "🎉Chào mừng bạn đến với ứng dụng VINAPHONE PERFORMANCE INSIGHTS của chúng tôi ! Đăng nhập để khám phá thêm!"

# Hàm stream dữ liệu
def stream_data():
    # Phần chào mừng ban đầu
    for word in _LOREM_IPSUM.split(" "):
        yield word
        time.sleep(0.1)
        yield " "
    
