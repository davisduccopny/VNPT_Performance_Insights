import streamlit as st 
import time
from PROJECTS.module_login import login
from PROJECTS.module_insert import load_data_service as load_data_service_for_all
from PROJECTS.module_view import load_data as load_data_for_all
from st_pages import add_page_title, get_nav_from_toml, hide_pages
if "is_logged_in" not in st.session_state or not st.session_state.is_logged_in:
    page_title = "VNPT-PERFORMANCE-INSIGHTS"
else:
    page_title = None
st.set_page_config(layout="wide",page_title=page_title, page_icon='src/vnpt.ico', initial_sidebar_state='auto')
st.logo("src/VNPT PERFORMANCE INSIGHTS (2).png", icon_image="src/vnpt.ico")

if "is_logged_in" not in st.session_state or not st.session_state.is_logged_in:
    st.session_state.is_logged_in = False
    st.session_state.role_access_admin = False
    st.session_state.line_access = None
    st.session_state.type_process = None
    login()

if st.session_state.is_logged_in:
    load_data_for_all()
    load_data_service_for_all()
    # Home
    home_page = st.Page("pages_view/home.py", title="Trang chủ", icon=":material/home:", default=True)
    users_page = st.Page("pages_view/users.py", title="Người dùng", icon=":material/manage_accounts:")
    if st.session_state.type_process != 'LDPVNPT':
        nav = get_nav_from_toml(".streamlit/pages.toml")
        
        if st.session_state.role_access_admin == 'admin':
            pg = st.navigation(nav)
        else:
            hide_pages(["Thêm dữ liệu", "Xóa dữ liệu","Giải trình"])
            pg = st.navigation(nav)
    else:
        nav = get_nav_from_toml(".streamlit/pages_ldp.toml")
        pg = st.navigation(nav)
    pg.run()
