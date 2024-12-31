import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import time
import PROJECTS.config as module_config
import PROJECTS.module_view as module_view
from LDP_MODULE.ldp_view import load_data_ldp,load_line_manage
import PROJECTS.module_expand as module_expand
import PROJECTS.module_users as module_users

if not st.session_state.get("is_logged_in", False):
    with st.spinner("🔐 Đang chuyển hướng đến trang đăng nhập..."):
        time.sleep(2)
    st.session_state.is_logged_in = False
    st.session_state.role_access_admin = False
    st.session_state.line_access = None
    st.switch_page("main.py")
    st.stop()
with open('src/style.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('src/style_general.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('src/style_users.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


class OTHER_USER():
    def __init__(self):
        pass
    def check_password(self, password):
        if len(password) < 6:
            return False
        has_digit = any(char.isdigit() for char in password)
        has_alpha = any(char.isalpha() for char in password)
        return has_digit and has_alpha
class FRONTEND_UI_DESIGN():
    def __init__(self):
        self.array_line =  line_after_load["ten_line"].tolist()

    def ui_info(self, text,loai_data):
        container_title_manage_expand = st.container(key="container_title_manage_expand")
        with container_title_manage_expand:
            col_title_dmanage_expand = st.columns([5,2])
            col_title_dmanage_expand[0].markdown(f"""<h3 style='text-align: left; padding:0; margin-bottom:5px;'>{text}</h3>
                                            <p style='text-align: left; padding:0'>Cài đặt người dùng <span style="color:#c4c411; font-weight:bolder;"> {loai_data} </span></p>""", unsafe_allow_html=True)
            with col_title_dmanage_expand[1]:
                with st.form(key="search_form", enter_to_submit=True,border=False):
                    cols_search = st.columns([6,1])
                    search_term = cols_search[0].text_input(label=" ",placeholder="Tìm kiếm thông tin", key="search_term",type="default")
                    if cols_search[1].form_submit_button("🔍"):
                        if search_term:
                            return search_term
                        else:
                            st.toast(f"##### Vui lòng nhập thông tin!", icon="⚠️")
                            return None
    def sidebar_ui(self):
        with st.sidebar:
            module_config.show_expander_sidebar()
        container_sidebar_user = st.sidebar.container(key="container_sidebar_user")
        container_sidebar_user.markdown("<h3 style='text-align: center; padding:0; margin-bottom:5px;'>👨‍💼 NGƯỜI DÙNG</h3>", unsafe_allow_html=True)
        # container_sidebar_user.divider()
        with container_sidebar_user:
            selected = option_menu(
                menu_title= None,  # required
                options=["Chung", "Mật khẩu","Hiển thị", "Khác"] if st.session_state.type_process != 'LDPVNPT' else ["Mật khẩu","Hiển thị", "Khác"],
                icons=[],  
                menu_icon= None,  
                default_index=0,  
                orientation="vertical",  
                key="menu_sidebar_delete",
                styles={
                "container": {
                    "padding": "0px 5px", 
                    "max-width": "100%",
                    "margin": "0px auto",  
                    "border": "None",
                    "border-radius": "20px",
                    "background-color": "rgb(120 ,189, 243)",
                },
                "icon": {
                    "color": "#fff",  
                    "font-size": "0.8rem",
                    "font-weight": "bold",
                },
                "nav-link": {
                    "font-size": "0.8rem", 
                    "text-align": "left",  
                    "--hover-color": "#54a7ef",
                    "font-weight": "bold",
                },
                "nav-link-selected": {
                    "border-radius": "15px",
                    "background-color": "#7FC8F8005E7C", 
                    "font-size": "0.8rem",
                    "font-family": "Tahoma, Geneva, sans-serif",
                    
                    
                }
            }
                )
        return selected
    def general_user_ui(self, username, display_name, role, line_access):
        filter_thuchien_after, filter_kehoach_after = MAIN_USER().load_data_metric_user()
        container_header_user_general = st.container(key="container_header_user_general")
        with container_header_user_general:
            cols_header_user_general = st.columns([2, 5])
            toggle_show_info_general = cols_header_user_general[0].toggle(
                "Hiển thị thông tin người dùng", key="show_info_user_general", value=True
            )
            
        
        container_main_user_general = st.container(key="container_main_user_general")
        
        with container_main_user_general:
            container_column_user_general = st.container(key="container_column_user_general")
            
            with container_column_user_general:
                cols_column_general = st.columns([45, 20])
                
                with cols_column_general[0]:
                    image_user_path = module_config.get_relative_file_path("../src/image_ex/image_user.avif")
                    st.markdown(f"""
                    <div style="text-align: center; padding:0; margin-bottom:5px;">
                    <image src="data:image/png;base64,{image_user_path}" style="width: 20%; margin-top: 0 auto; border-radius: 40%; text-align:center;"></image>
                    </div>
                    <h3 style='text-align: center; padding:0; margin-bottom:10%;'>
                        {display_name if toggle_show_info_general else "***"}
                    </h3>
                    """, unsafe_allow_html=True)
                    
                    container_first_info = st.container(key="container_first_info")
                    with container_first_info:
                        cols_second_column = st.columns([1, 1, 1])
                        
                        with cols_second_column[0]:
                            metric_thuchien_user = filter_thuchien_after["doanhthu"].sum()
                            st.metric(
                                label="Doanh thu",
                                value=module_view.format_number(metric_thuchien_user) if toggle_show_info_general else "***",
                                delta="₫"
                            )
                        
                        with cols_second_column[1]:
                            metric_kehoach_user = filter_kehoach_after["t1"].sum()
                            st.metric(
                                label="Kế hoạch",
                                value=module_view.format_number(metric_kehoach_user) if toggle_show_info_general else "***",
                                delta="₫"
                            )
                        
                        with cols_second_column[2]:
                            metric_dichvu_danglam = len(filter_thuchien_after["nhom_dv"].unique())
                            st.metric(
                                label="Dịch vụ đang làm",
                                value=metric_dichvu_danglam if toggle_show_info_general else "***"
                            )
                
                with cols_column_general[1]:
                    st.markdown(f"""
                        <h3 style='text-align: center; padding:0; margin-bottom:5px;'>Tỷ lệ hoàn thành</h3>
                    """, unsafe_allow_html=True)
                    
                    container_metric_user = st.container(key="container_metric_user")
                    with container_metric_user:
                        completion_rate = 0 if metric_kehoach_user == 0 else round((metric_thuchien_user / metric_kehoach_user) * 100, 2)
                        if toggle_show_info_general:
                            donut_percentage = module_view.make_donut(completion_rate, "Tỷ lệ hoàn thành")
                            st.altair_chart(donut_percentage)
                        else:
                            st.write("***")
                    
                    container_second_info = st.container(key="container_second_info")
                    with container_second_info:
                        st.markdown(f"""
                            <div style="display:flex;align-items: center;flex-direction: column; padding:0; margin-bottom:5px;text-align:left;">
                            <h4 style='text-align: left; padding:0; margin-bottom:5px;'>Thông tin người dùng</h4>
                            <p style='text-align: left; padding:0; margin-bottom:5px;'>Tên đăng nhập: 
                                <span style="color:#c4c411; font-weight:bolder;">{username if toggle_show_info_general else "***"}</span>
                            </p>
                            <p style='text-align: left; padding:0; margin-bottom:5px;'>Vai trò: 
                                <span style="color:#c4c411; font-weight:bolder;">{role if toggle_show_info_general else "***"}</span>
                            </p>
                            <p style='text-align: left; padding:0; margin-bottom:5px;'>Line: 
                                <span style="color:#c4c411; font-weight:bolder;">{line_after_load[line_after_load["ma_line"]==line_access]["ten_line"].values[0] if toggle_show_info_general else "***"}</span>
                            </p>
                            </div>
                        """, unsafe_allow_html=True)
    def change_password_user(self):
        container_change_pass = st.container(key="container_change_pass")
        with container_change_pass:
            cols_permission_pass = st.columns([3,1])
            permission_pass_toggle = cols_permission_pass[0].toggle(
                "Cho phép sửa mật khẩu", key="permission_pass_toggle", value=False
            )
            cols_permission_pass[1].write(f"##### 👋 {MAIN_USER().load_data_for_user()[1]}")
            if permission_pass_toggle:
                disable = False
            else:
                disable = True
            container_form_change_pass = st.container(key="container_form_change_pass")
            with container_form_change_pass:
                with st.form(key="change_pass_form", enter_to_submit=True, border=False, clear_on_submit=True):
                    cols_change_pass = st.columns([6,1])
                    old_pass = cols_change_pass[0].text_input(label="🔑Mật khẩu cũ",placeholder="Nhập mật khẩu cũ", key="old_pass",type="password", disabled=disable)
                    new_pass = cols_change_pass[0].text_input(label="🔑Mật khẩu mới",placeholder="Nhập mật khẩu mới", key="new_pass",type="password", disabled=disable)
                    confirm_pass = cols_change_pass[0].text_input(label="🔑Xác nhận mật khẩu mới",placeholder="Nhập lại mật khẩu mới", key="confirm_pass",type="password", disabled=disable)
                    if st.form_submit_button("Save", icon=":material/save:", type="primary", help="Nhấn vào để lưu thay đổi!", disabled=disable):
                        with st.spinner("🔐 Đang thực hiện thao tác..."):
                            time.sleep(2)
                        if old_pass and new_pass and confirm_pass:
                            if not OTHER_USER().check_password(new_pass):
                                st.toast(f"##### Mật khẩu phải có ít nhất 6 ký tự, bao gồm cả chữ và số!", icon="⚠️")
                                time.sleep(2)
                                return None
                            else:
                                if new_pass != confirm_pass:
                                    st.toast(f"##### Mật khẩu mới không khớp!", icon="⚠️")
                                    time.sleep(1)
    
                                else:
                                    if module_users.change_password(st.session_state.usernamevnpt, old_pass, new_pass):
                                        st.toast("##### Đổi mật khẩu thành công!", icon="✅")
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.toast("##### Mật khẩu cũ không đúng!", icon="❌")
                                        time.sleep(1)
                        else:
                            st.toast(f"##### Vui lòng nhập thông tin!", icon="⚠️")
                            time.sleep(1)

    def display_user_change(self):
        container_change_display = st.container(key="container_change_display")
        with container_change_display:
            cols_permission_display = st.columns([3,1])
            permission_display_toggle = cols_permission_display[0].toggle(
                "Cho phép sửa thông tin", key="permission_display_toggle", value=False
            )
            cols_permission_display[1].write(f"##### 👋 {MAIN_USER().load_data_for_user()[1]}")
            if permission_display_toggle:
                disable = False
            else:
                disable = True
            container_form_change_display = st.container(key="container_form_change_display")
            with container_form_change_display:
                with st.form(key="change_display_form", enter_to_submit=True, border=False, clear_on_submit=False):
                    cols_change_display = st.columns([6,1])
                    display_name = cols_change_display[0].text_input(label="Tên hiển thị", value=MAIN_USER().load_data_for_user()[1],placeholder="Nhập tên hiển thị", key="display_name_user", disabled=disable)
                    main_user_instance = MAIN_USER()
                    current_line = main_user_instance.load_data_for_user()[3]
                    current_line = line_after_load[line_after_load["ma_line"]==current_line]["ten_line"].values[0]
                    line_index = self.array_line.index(current_line) if current_line in self.array_line else 0
                    line = cols_change_display[0].selectbox("Line", self.array_line, index=line_index, key="line_user_change_private", disabled=disable)
                    ma_nv = cols_change_display[0].text_input(label="Mã nhân viên", value=MAIN_USER().load_data_for_user()[0],placeholder="Nhập mã nhân viên", key="code_employee_new_change", disabled=disable)
                    ma_line_new = line_after_load[line_after_load["ten_line"]==line]["ma_line"].values[0] 
                    if st.form_submit_button("Save", icon=":material/save:", type="primary", help="Nhấn vào để lưu thay đổi!", disabled=disable):
                        with st.spinner("🔐 Đang thực hiện thao tác..."):
                            time.sleep(2)
                        if display_name and line and ma_nv:
                            if module_users.change_profile(st.session_state.usernamevnpt, display_name, ma_line_new, ma_nv):
                                st.toast("##### Đổi thông tin thành công!", icon="✅")
                                time.sleep(1)
                                module_users.load_data_for_user.clear()
                                st.rerun()
                            else:
                                st.toast("##### Mã nhân viên đã tồn tại!", icon="❌")
                                time.sleep(1)
                        else:
                            st.toast(f"##### Vui lòng nhập thông tin!", icon="⚠️")
                            time.sleep(1)
    def account_delete(self, search_term=None):
        st.info("##### ⚠️ Lưu ý: Hành động này không thể hoàn tác!")
        container_delete_account = st.container(key="container_delete_account")
        with container_delete_account:
            tabs_account_info_action =  st.tabs(["⏲️ Hành động người dùng","🗑️ Xóa tài khoản"])
            with tabs_account_info_action[1]:
                cols_delete_account = st.columns([0.5,2,3])
                with cols_delete_account[1]:
                    st.write("#### ⚠️ Xóa tài khoản 🤔🤔🤔")
                    key_delete_button_delete = st.button("Xóa tài khoản", icon=":material/delete:", key="delete_button_delete", use_container_width=True, help="Nhấn vào để xóa tài khoản của bạn!")
                    if key_delete_button_delete:
                        st.session_state.dialog_open = True
                            
                    if st.session_state.get("dialog_open", False):
                        module_config.show_confirmation_dialog("xóa tài khoản")
                    if "confirmation" in st.session_state:
                        if st.session_state.confirmation == "Yes":
                            with st.spinner("🔐 Đang thực hiện thao tác..."):
                                st.session_state.confirmation = None
                                if module_users.delete_user(st.session_state.usernamevnpt):
                                    st.session_state.is_logged_in = False
                                    st.session_state.role_access_admin = False
                                    st.session_state.line_access = None
                                    st.switch_page("Home.py")
                                else:
                                    st.toast("##### Xóa tài khoản không thành công!", icon="❌")
            with tabs_account_info_action[0]:
                # st.write("#### ⏲️ Hành động người dùng 🤔🤔🤔")
                data_action_check = module_users.load_action_check_user(st.session_state.line_access)
                if search_term:
                    data_action_check = data_action_check[(data_action_check["username"].str.contains(search_term, case=False)) | (data_action_check["action_content"].str.contains(search_term, case=False))]
                data_action_check = data_action_check.reset_index(drop=True)
                data_action_check = data_action_check.rename(columns={"username":"Tên đăng nhập" , "action_content":"Hành động","time_action":"Thời gian"})
                st.dataframe(data_action_check, use_container_width=True, hide_index=   True)
                
class MAIN_USER():
    def __init__(self):
        self.frontend = FRONTEND_UI_DESIGN()
    def user(self):
        
        selected = self.frontend.sidebar_ui()
        if selected == "Chung" and (st.session_state.type_process != 'LDPVNPT'):
            self.frontend.ui_info("👨‍💼 NGƯỜI DÙNG","Xem thông tin")
            ma_nv,diplay_name,role,line_access = self.load_data_for_user()
            self.frontend.general_user_ui(st.session_state.usernamevnpt,diplay_name,role,line_access)

        elif selected == "Mật khẩu":
            self.frontend.ui_info("👨‍💼 MẬT KHẨU","thay đổi mật khẩu")
            self.frontend.change_password_user()
        elif selected == "Hiển thị":
            self.frontend.ui_info("👨‍💼 HIỂN THỊ","thay đổi hiển thị")
            self.frontend.display_user_change()
        elif selected == "Khác":
            search_tearm = self.frontend.ui_info("👨‍💼 KHÁC","- hành động - xóa")
            self.frontend.account_delete(search_tearm)
    def load_data_for_user(self):
        ma_nv = data_user[data_user["username"] == st.session_state.usernamevnpt]["ma_nv"].values[0]
        diplay_name = data_user[data_user["username"] == st.session_state.usernamevnpt]["display_name"].values[0]
        role = data_user[data_user["username"] == st.session_state.usernamevnpt]["role"].values[0]
        line_access = data_user[data_user["username"] == st.session_state.usernamevnpt]["line"].values[0]
        return ma_nv,diplay_name,role,line_access
    def load_data_metric_user(self):
        ma_nv,diplay_name,role,line_access = self.load_data_for_user()
        filter_thuchien = thuchien_after_load[thuchien_after_load["IDnhanvien"] == ma_nv]
        filter_kehoach = kehoach_after_load[kehoach_after_load["ma_nv"] == ma_nv]
        return filter_thuchien, filter_kehoach

data_user = module_users.load_data_for_user(st.session_state.usernamevnpt)
if st.session_state.type_process != 'LDPVNPT':
    thuchien_after_load, kehoach_after_load, nhanvien_after_load, dichvu_after_load, line_after_load = module_view.load_data()   
else:
    thuchien_after_load, kehoach_after_load, nhanvien_after_load, dichvu_after_load,line_after_load = load_data_ldp()
    line_after_load = load_line_manage()
    
main_user = MAIN_USER()
main_user.user()
module_config.add_sidebar_footer()