import streamlit as st 
import time
from EM_MODULE.config import measure_test_time_load_api
if "is_logged_in" not in st.session_state or not st.session_state.is_logged_in:
    page_title = "VNPT-PERFORMANCE-INSIGHTS"
else:
    page_title = None
st.set_page_config(layout="wide",page_title=page_title, page_icon=measure_test_time_load_api('src/vnpt.ico'), initial_sidebar_state='auto')
st.logo(measure_test_time_load_api("src/VNPT_PERFORMANCE_INSIGHTS__2_-removebg-preview.png"), icon_image=measure_test_time_load_api('src/vnpt.ico'))

with st.spinner('Đang tải giao diện...'):
    from EM_MODULE.module_login import login
    from EM_MODULE.module_insert import load_data_service as load_data_service_for_all
    from EM_MODULE.module_view import load_data as load_data_for_all
    from LDP_MODULE.ldp_view import load_data_ldp 
    from st_pages import add_page_title, get_nav_from_toml, hide_pages


    if "is_logged_in" not in st.session_state or not st.session_state.is_logged_in:
        st.session_state.is_logged_in = False
        st.session_state.role_access_admin = False
        st.session_state.line_access = None
        st.session_state.type_process = None
        st.cache_data.clear()
        login()

if st.session_state.is_logged_in:
    
    # Home
    home_page = st.Page("pages_view/home.py", title="Trang chủ", icon=":material/home:", default=True)
    users_page = st.Page("pages_view/users.py", title="Người dùng", icon=":material/manage_accounts:")
    if st.session_state.type_process != 'LDPVNPT':
        load_data_for_all()
        load_data_service_for_all()
        nav = get_nav_from_toml(".streamlit/pages.toml")
        
        if st.session_state.role_access_admin == 'admin':
            pg = st.navigation(nav)
        else:
            hide_pages(["Quản lý dữ liệu", "Xóa dữ liệu","Giải trình"])
            pg = st.navigation(nav)
    else:
        load_data_ldp()
        load_data_service_for_all()
        nav = get_nav_from_toml(".streamlit/pages_ldp.toml")
        pg = st.navigation(nav)
    pg.run()
