import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import io
import time
import PROJECTS.module_users as module_users
import PROJECTS.module_expand as module_expand
import PROJECTS.config as module_config
import PROJECTS.module_view as module_view
import documentation.module_documentation as module_documentation

# PART CHECK LOGIN
if not st.session_state.get("is_logged_in", False):
    with st.spinner("🔐 Đang chuyển hướng đến trang đăng nhập..."):
        time.sleep(2)
    st.session_state.is_logged_in = False
    st.session_state.role_access_admin = False
    st.session_state.line_access = None
    st.switch_page("main.py")
    st.stop()
# PART CONFIG
with open('src/style.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('src/style_general.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('src/style_expand.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
# PART DESIGN FRONTEND
class DESIGN_FRONTEND_MANAGE():
    def __init__(self):
        self.array_line =  line_after_load["ten_line"].tolist()
        self.array_user = ['manage','user']
    def ui_info(self, text,loai_data):
        container_title_manage_expand = st.container(key="container_title_manage_expand")
        with container_title_manage_expand:
            col_title_dmanage_expand = st.columns([5,2])
            col_title_dmanage_expand[0].markdown(f"""<h3 style='text-align: left; padding:0; margin-bottom:5px;'>{text}</h3>
                                            <p style='text-align: left; padding:0'>Thao tác quản lý <span style="color:#c4c411; font-weight:bolder;"> {loai_data} </span> cho line</p>""", unsafe_allow_html=True)
            with col_title_dmanage_expand[1]:
                with st.form(key="search_form", enter_to_submit=True,border=False):
                    cols_search = st.columns([6,1])
                    search_term = cols_search[0].text_input(label=" ",placeholder="Tìm kiếm thông tin", key="search_term",type="default")
                    if cols_search[1].form_submit_button("🔍",use_container_width=True):
                        if search_term:
                            return search_term
                        else:
                            st.toast(f"##### Vui lòng nhập thông tin!", icon="⚠️")
                            return None
    @st.dialog(f"Chỉnh sửa thông tin người dùng 👨‍🎓")
    def show_confirmation_dialog_edit(self,index_for_edit,index_for_edit_role):
        if "dialog_open_edit_user" not in st.session_state:
            st.session_state.dialog_open_edit_user = False
        if st.session_state.dialog_open_edit_user:
            cols_main_dialog_update = st.columns([1,1])
            new_ten = cols_main_dialog_update[0].text_input("Username mới", str(st.session_state.edit_username), key="edit_username_input_page_manage_users")
            new_line = cols_main_dialog_update[1].selectbox("Line mới", options=self.array_line, index=index_for_edit, key="edit_line_input_page_manage_users")
            new_role = cols_main_dialog_update[0].selectbox("Role mới",options=self.array_user, index=index_for_edit_role, key="edit_role_input_page_manage_users")
            new_display_name = cols_main_dialog_update[1].text_input("Display name mới", str(st.session_state.edit_display_name), key="edit_display_name_input_page_manage_users")
            new_ma_nv = st.text_input("Mã nhân viên", str(st.session_state.edit_ma_nv), key="edit_ma_nv_input_page_manage_users")
            cols_user_edit = st.columns([1,1])
            button_update_user = cols_user_edit[0].button("Lưu", key="save_editpagemanagermentusers", type="primary", icon=":material/save:",use_container_width=True)
            button_cancel_user = cols_user_edit[1].button("Hủy", key="cancel_editpagemanagermentusers", icon=":material/cancel:",use_container_width=True)
            if button_update_user:
                with st.spinner("Đang cập nhật..."):
                    new_line = line_after_load[line_after_load["ten_line"] == new_line]["ma_line"].values[0]
                    if module_expand.update_user_by_id(int(st.session_state.edit_id), new_line, new_ten, new_display_name, new_role,new_ma_nv):
                        st.success("Đã cập nhật thông tin người dùng",icon="✅")
                        st.session_state.pop("edit_id")
                        st.session_state.pop("edit_username")
                        st.session_state.pop("edit_line")
                        st.session_state.pop("edit_role")
                        st.session_state.pop("edit_display_name")
                        st.session_state.pop("edit_ma_nv")
                        module_users.insert_action_check_user(st.session_state.usernamevnpt,st.session_state.line_access,f"Chỉnh sửa thông tin người dùng {new_ten}")
                        module_users.load_action_check_user.clear()
                        st.cache_data.clear()
                        st.session_state.dialog_open_edit_user = False
                        st.rerun()
                    else:
                        st.warning("Username hoặc mã nhân viên trùng lặp", icon="⚠️")
            if button_cancel_user:
                st.session_state.pop("edit_id")
                st.session_state.pop("edit_username")
                st.session_state.pop("edit_line")
                st.session_state.pop("edit_role")
                st.session_state.pop("edit_display_name")
                st.session_state.pop("edit_ma_nv")
                st.session_state.dialog_open_edit_user = False
                st.rerun()
    @st.dialog("Thêm người dùng 👨‍🎓")
    def show_confirmation_dialog_insert(self):
        if "dialog_open_insert_user" not in st.session_state:
            st.session_state.dialog_open_insert_user = False
        if "confirmation_insert" not in st.session_state:
            st.session_state.confirmation_insert = None
        if st.session_state.dialog_open_insert_user:
            st.write(f"🤔 Thêm người dùng mới vào csdl❗")
            cols_add_user = st.columns(2)
            with cols_add_user[0]:
                new_username = st.text_input("Username mới", key="new_username_input_page_manage_users")
                new_role = st.selectbox("Role mới",self.array_user, key="new_role_input_page_manage_users")
            with cols_add_user[1]:
                new_password = st.text_input("Password mới", type="password", key="new_password_input_page_manage_users")
                new_manv = st.text_input("Mã nhân viên", key="new_manv_input_page_manage_users")
            new_line = st.selectbox("Line", self.array_line, key="new_line_input_page_manage_users")
            new_display_name = st.text_input("Display name mới", key="new_display_name_input_page_manage_users")
            col1, col2 = st.columns(2)
            button_insert_user = col1.button("Đồng ý", key="add_new_user_page_manage_users", use_container_width=True, icon=":material/person_add:")
            button_cancel_user = col2.button("Bỏ qua", key="cancel_new_user_page_manage_users", use_container_width=True, icon=":material/cancel:")
            if button_insert_user:
                with st.spinner("Đang thêm..."):
                    st.session_state.confirmation_insert = "Yes"
                    if not new_username or not new_line or not new_role or not new_password or not new_display_name or not new_manv:
                        st.error("Vui lòng nhập đầy đủ thông tin", icon="⚠️")
                    else:
                        if not new_username.endswith("@vnpt.vn"):
                            st.warning("Username phải có dạng email với đuôi @vnpt.vn", icon="⚠️")
                        else:
                            new_line = line_after_load[line_after_load["ten_line"] == new_line]["ma_line"].values[0]
                            st.session_state.dialog_open_insert_user = False
                            if module_expand.add_user(new_username,new_display_name,new_role, new_line , new_password, new_manv):
                                st.success("Đã thêm người dùng mới", icon="✅")
                                module_users.insert_action_check_user(st.session_state.usernamevnpt,st.session_state.line_access,f"Thêm người dùng {new_username}")
                                module_users.load_action_check_user.clear()
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.warning(f"Username hoặc mã nhân viên trùng lặp!", icon="⚠️")
                                st.rerun()
            if button_cancel_user:
                st.session_state.confirmation_insert = "No"
                st.session_state.dialog_open_insert_user = False
                st.rerun()
    def streamlit_menu_sidebar_delete(self):
        with st.sidebar:
            module_config.show_expander_sidebar()
            if (st.session_state.role_access_admin == "admin" or st.session_state.role_access_admin == "manage") and st.session_state.line_access != "LDPVNPT":
                selected = option_menu(
                    menu_title= None,  # required
                    options=["Quản lý tài khoản", "Tài liệu hướng dẫn"],  # required
                    icons=["bag-check-fill", "journal-text"],  
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
            else:
                selected = option_menu(
                    menu_title= None,  # required
                    options=["Tài liệu hướng dẫn"],  # required
                    icons=["journal-text"],  
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
    def manage_users(self, load_data_users, search_term=None):
        if search_term:
            load_data_users = [i for i in load_data_users if search_term.lower() in i['username'].lower() or search_term.lower() in i['line'].lower() or search_term.lower() in i['role'].lower() or search_term.lower() in i['display_name'].lower()]
        else:
            load_data_users = load_data_users
        # Xuất dữ liệu ra file Excel
        df_download_data = pd.DataFrame(load_data_users)
        output_xlsx_download = io.BytesIO()
        with pd.ExcelWriter(output_xlsx_download, engine='xlsxwriter') as writer:
            df_download_data.to_excel(writer, sheet_name='Sheet1', index=False)
        
        container_title_manage_user = st.container(key="container_title_manage_user")
        with container_title_manage_user:
            container_header_manage_user = st.container(key="container_header_manage_user")
            with container_header_manage_user:
                col_header_manage_user = st.columns([9,9,9,44])
                refresh_cache = col_header_manage_user[0].button("Load",icon=":material/published_with_changes:", key="refresh_page_manage_users",use_container_width=True, help="Làm mới")
                export_user_info =col_header_manage_user[1].download_button("Excel",icon=":material/file_export:", key="export_excel_page_manage_users",use_container_width=True, help="Xuất excel",
                                                                            data=output_xlsx_download.getvalue(),
                                                                            file_name="user_info.xlsx",
                                                                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                button_submit_add_user = col_header_manage_user[2].button("Users", icon=":material/person_add:", key="add_user_page_manage_users", type="primary",use_container_width=True, help="Thêm người")
                if refresh_cache:
                    st.cache_data.clear()
                    st.rerun()
                # PART ADD USER
                if button_submit_add_user:
                    st.session_state.dialog_open_insert_user = True
                if st.session_state.get("dialog_open_insert_user", False):
                        self.show_confirmation_dialog_insert()
                if "confirmation_insert" in st.session_state:
                        if st.session_state.confirmation_insert == "Yes":
                            st.session_state.confirmation_insert = None
            container_second_show_table_manage = st.container(key="container_second_show_table_manage")
            with container_second_show_table_manage:
                # with st.expander("Quản lý các Line", expanded=True):
                data = load_data_users
                for item in data:
                    item["line"] = line_after_load[line_after_load["ma_line"] == item["line"]]["ten_line"].values[0] \
                        if not line_after_load[line_after_load["ma_line"] == item["line"]].empty else "Unknown"
                if "dialog_open_edit_user" not in st.session_state:
                        st.session_state.dialog_open_edit_user = False
                # Hien thi phan trang
                users_per_page = 4
                total_pages = (len(data) + users_per_page - 1) // users_per_page
                current_page = st.session_state.get("current_page", 1)

                start_idx = (current_page - 1) * users_per_page
                end_idx = start_idx + users_per_page
                ctn_header_table_manage = st.container(key="ctn_header_table_manage")
                with ctn_header_table_manage:
                    cols_header_manage_foreach = ctn_header_table_manage.columns([1, 1, 1, 1, 1, 2])
                    with cols_header_manage_foreach[0]:
                        st.markdown("<p style='text-align: center;'>Tên đăng nhập</p>", unsafe_allow_html=True)
                    with cols_header_manage_foreach[1]:
                        st.markdown("<p style='text-align: center;'>Line</p>", unsafe_allow_html=True)
                    with cols_header_manage_foreach[2]:
                        st.markdown("<p style='text-align: center;'>Vai trò</p>", unsafe_allow_html=True)
                    with cols_header_manage_foreach[3]:
                        st.markdown("<p style='text-align: center;'>Tên hiển thị</p>", unsafe_allow_html=True)
                    with cols_header_manage_foreach[4]:
                        st.markdown("<p style='text-align: center;'>Mã NV</p>", unsafe_allow_html=True)
                    with cols_header_manage_foreach[5]:
                        st.markdown("<p style='text-align: center;'>Hành động</p>", unsafe_allow_html=True)
                for idx, row in enumerate(data[start_idx:end_idx]):
                    cols_user_manager_foreach = st.columns([1,1, 1, 1, 1,2])
                    with cols_user_manager_foreach[0]:
                        st.markdown(f"<p style='text-align: center;'>{row['username']}</p>", unsafe_allow_html=True)
                    with cols_user_manager_foreach[1]:
                        st.markdown(f"<p style='text-align: center;'>{row['line']}</p>", unsafe_allow_html=True)
                    with cols_user_manager_foreach[2]:
                        st.markdown(f"<p style='text-align: center;'>{row['role']}</p>", unsafe_allow_html=True)
                    with cols_user_manager_foreach[3]:
                        st.markdown(f"<p style='text-align: center;'>{row['display_name']}</p>", unsafe_allow_html=True)
                    with cols_user_manager_foreach[4]:
                        st.markdown(f"<p style='text-align: center;'>{row['ma_nv']}</p>", unsafe_allow_html=True)
                    with cols_user_manager_foreach[5]:
                        cols_child_foreach_manage = st.columns([1, 1])
                        with cols_child_foreach_manage[0]:
                            if st.button("🗑️Xóa", key=f"delete_{row['id']}", use_container_width=True):
                                if module_expand.delete_user_by_id(int(row['id'])):
                                    st.toast("##### Đã xóa user", icon="✅")
                                    time.sleep(1)
                                    module_users.insert_action_check_user(st.session_state.usernamevnpt, st.session_state.line_access, f"Xóa người dùng {row['username']}")
                                    module_users.load_action_check_user.clear()
                                    st.cache_data.clear()
                                    st.session_state['rerun'] = True
                                else:
                                    st.error("Có lỗi xảy ra khi xóa user")
                        with cols_child_foreach_manage[1]:
                            if st.button("✏️Sửa", key=f"edit_{row['id']}", use_container_width=True):
                                st.session_state.edit_id = row['id']
                                st.session_state.edit_username = row['username']
                                st.session_state.edit_line = row['line']
                                st.session_state.edit_role = row['role']
                                st.session_state.edit_display_name = row['display_name']
                                st.session_state.edit_ma_nv = row['ma_nv']
                                st.session_state.dialog_open_edit_user = True
                                st.session_state['rerun'] = True
                    if idx < len(data[start_idx:end_idx]) - 1:
                        st.markdown("<hr style='margin: 0 auto;'>", unsafe_allow_html=True)

                if total_pages > 1:
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col1:
                        if current_page > 1:
                            if st.button("Previous", use_container_width=True):
                                st.session_state.current_page = current_page - 1
                                st.rerun()
                    with col2:
                        st.write(f"Page {current_page} of {total_pages}")
                    with col3:
                        if current_page < total_pages:
                            if st.button("Next", use_container_width=True):
                                st.session_state.current_page = current_page + 1
                                st.rerun()
                # End phan trang

                if 'rerun' in st.session_state and st.session_state['rerun']:
                    st.session_state['rerun'] = False
                    st.rerun()

                if "edit_id" in st.session_state and "edit_username" in st.session_state and "edit_line" in st.session_state and "edit_role" in st.session_state and "edit_display_name" in st.session_state:
                    if st.session_state.edit_line in self.array_line:
                        index_for_edit = self.array_line.index(st.session_state.edit_line)
                    else:
                        index_for_edit = 0
                    if st.session_state.edit_role in self.array_user:
                        index_for_edit_role = self.array_user.index(st.session_state.edit_role)
                    else:
                        index_for_edit_role = 0
                    if  st.session_state.get("dialog_open_edit_user", False):
                        self.show_confirmation_dialog_edit(index_for_edit,index_for_edit_role)
    def documentaion_ui_design(self, search_term=None):
        docs = [
            {"id": 1, "title": "Hướng dẫn xem dạng dashboard", "author": "KHDN3", "source": "documentation/view_app/dashboard.html", "image": "../src/dashboard_doc.png"},
            {"id": 2, "title": "Hướng dẫn xem dạng table", "author": "KHDN3", "source": "../documentation/view_app/dashboard.md", "image": "../src/documentation.png"},
            {"id": 3, "title": "Thêm dữ liệu", "author": "KHDN3", "source": "../documentation/view_app/dashboard.md", "image": "../src/kehoach_insert_doc.png"},
            {"id": 4, "title": "Quản lý dịch vụ", "author": "KHDN3", "source": "../documentation/view_app/dashboard.md", "image": "../src/mangerment_service_doc.png"},
            {"id": 5, "title": "Xem biểu mẫu", "author": "KHDN3", "source": "../documentation/view_app/dashboard.md", "image": "../src/bieumau_doc.png"},
            {"id": 6, "title": "Cài đặt người dùng", "author": "KHDN3", "source": "../documentation/view_app/dashboard.md", "image": "../src/user_doc.png"},
            {"id": 7, "title": "Mở rộng - Quản lý tài khoản", "author": "KHDN3", "source": "../documentation/view_app/dashboard.md", "image": "../src/managerment_user_doc.png"},
            {"id": 8, "title": "Xóa dữ liệu", "author": "KHDN3", "source": "../documentation/view_app/dashboard.md", "image": "../src/delete_data_doc.png"},
        
        ]

        # Kiểm tra trạng thái tài liệu đang được chọn
        if "selected_documentation" not in st.session_state:
            st.session_state.selected_documentation = None

        def show_document_detail(doc_id):
            """Hiển thị chi tiết tài liệu dựa trên ID."""
            st.session_state.selected_documentation = next((doc for doc in docs if doc["id"] == doc_id), None)

        def back_to_home_doc():
            """Trở về trang chủ tài liệu."""
            st.session_state.selected_documentation = None

        def back_to_list(selected_doc_index):
            """Quay lại tài liệu trước đó."""
            selected_doc_index = (selected_doc_index - 1) % len(docs)  # Điều hướng vòng lặp
            st.session_state.selected_documentation = docs[selected_doc_index-1]

        def next_to_list(selected_doc_index):
            """Chuyển đến tài liệu tiếp theo."""
            selected_doc_index = (selected_doc_index + 1) % len(docs)  # Điều hướng vòng lặp
            st.session_state.selected_documentation = docs[selected_doc_index-1]


        # Hiển thị chi tiết tài liệu nếu có
        if st.session_state.selected_documentation:
            doc = st.session_state.selected_documentation
            key_id_doc = doc["id"]

            cols_show_doc = st.columns([1, 1, 1, 1, 1])

            if key_id_doc > 1:
                cols_show_doc[0].button("Quay lại", icon=":material/arrow_back:", key=f"back_to_list_{key_id_doc}", on_click=back_to_list, args=(key_id_doc,),  use_container_width=True)
            cols_show_doc[2].button("Trang chính", icon=":material/home:", on_click=back_to_home_doc, use_container_width=True)
            if key_id_doc < len(docs):
                cols_show_doc[4].button("Tiếp theo", icon=":material/arrow_forward:",  key=f"next_to_list_{key_id_doc}",  on_click=next_to_list, args=(key_id_doc,),use_container_width=True)
            st.markdown(f"""<h4 style="text-align:center; margin-top:0;">{doc["title"]}</h4>""",unsafe_allow_html=True)
            

            if doc["id"] == 1:
                module_documentation.dashboard_documentation()
            elif doc["id"] == 2:
                module_documentation.table_documentation()
            elif doc["id"] == 3:
                module_documentation.insert_data_documentation()
            elif doc["id"] == 4:
                module_documentation.managerment_service_documentation()
            elif doc["id"] == 6:
                module_documentation.user_documentation()
            elif doc["id"] == 7:
                module_documentation.expand_and_management_user()
            elif doc["id"] == 8:
                module_documentation.delete_data_documentation()
            
        else:
            container_first_document = st.container(key="container_first_document")
            
            with container_first_document:
                columns_per_row = 4
                if search_term:
                    search_term = search_term.lower()
                    docs = [doc for doc in docs if search_term in doc["title"].lower() or search_term in doc["content"].lower()]
                    columns_per_row = len(docs) if len(docs) < 4 else 4
                docs_per_page = 8
                total_pages = (len(docs) + docs_per_page - 1) // docs_per_page
                current_page = st.session_state.get("current_page", 1)

                start_idx = (current_page - 1) * docs_per_page
                end_idx = start_idx + docs_per_page

                for i in range(start_idx, min(end_idx, len(docs)), columns_per_row):
                    cols = st.columns(columns_per_row)
                    for j in range(columns_per_row):
                        if i + j < len(docs):
                            doc = docs[i + j]
                            with cols[j]:
                                image_file_path = module_config.get_relative_file_path(doc["image"])
                                st.markdown(f"""<img src="data:image/png;base64,{image_file_path}" style="height:10vh;width:auto;"></img>""", unsafe_allow_html=True)
                                st.markdown(f"**{doc['title']}**")
                                st.write(f"Tác giả: **{doc['author']}**")
                                st.button("Xem chi tiết", icon=":material/description:" ,key=f"doc_{doc['id']}", on_click=show_document_detail, args=(doc["id"],))

                if total_pages > 1:
                    container_pagination = st.container(key="container_pagination")
                    with container_pagination:
                        col1, col2, col3 = st.columns([0.5, 2, 0.5])
                        with col1:
                            if current_page > 1:
                                if st.button("Previous", icon=":material/arrow_back:", use_container_width=True):
                                    st.session_state.current_page = current_page - 1
                                    st.rerun()
                        with col2:
                            st.write(f"Page {current_page} of {total_pages}")
                        with col3:
                            if current_page < total_pages:
                                if st.button("Next", icon=":material/arrow_forward:", use_container_width=True):
                                    st.session_state.current_page = current_page + 1
                                    st.rerun()
               

class MAIN_MANAGE():
    def __init__(self):
        self.loai_data = None
        self.search_term = None
        self.load_data_users = module_expand.load_data()
    def run_manage(self,selected):
        if selected == "Quản lý tài khoản":
            self.loai_data = "người dùng"
            self.search_term= DESIGN_FRONTEND_MANAGE().ui_info(text="🛠️Quản lý tài khoản",loai_data=self.loai_data)
            DESIGN_FRONTEND_MANAGE().manage_users(self.load_data_users,self.search_term)
        elif selected == "Tài liệu hướng dẫn":
            loai_data = "tài liệu"
            self.search_term = DESIGN_FRONTEND_MANAGE().ui_info(text="📰 Tài liệu hướng dẫn",loai_data=loai_data)
            DESIGN_FRONTEND_MANAGE().documentaion_ui_design(self.search_term)
            

thuchien_after_load, kehoach_after_load, nhanvien_after_load, dichvu_after_load,line_after_load = module_view.load_data()  
selected = DESIGN_FRONTEND_MANAGE().streamlit_menu_sidebar_delete()
MAIN_MANAGE().run_manage(selected)
module_config.add_sidebar_footer()
    