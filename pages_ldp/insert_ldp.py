import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import io
import time
import datetime
import streamlit.components.v1 as components
import EM_MODULE.config as module_config
import LDP_MODULE.ldp_insert as module_insert
import LDP_MODULE.ldp_view as module_view
import EM_MODULE.module_users as module_users
#  PART CHECK LOGIN
if not st.session_state.get("is_logged_in", False):
    with st.spinner("🔐 Đang chuyển hướng đến trang đăng nhập..."):
        time.sleep(2)
    st.session_state.is_logged_in = False
    st.session_state.role_access_admin = False
    st.session_state.line_access = None
    st.switch_page("main.py")
    st.stop()
if st.session_state.line_access != "LDPVNPT":
    st.warning("Chế độ xem tham khảo, không cho phép chỉnh sửa!")
    disabled_widget_experimental = True
else:
    disabled_widget_experimental = False
# PATH CONFIG
with open('src/style.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('src/style_general.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('src/style_insert.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


class ORTHER_FUNCTION_INSERT():
    def __init__(self):
        pass
    
    def check_duplicate(self,data, column_name):
        """Kiểm tra trùng dữ liệu trong cột cụ thể."""
        duplicates = data[column_name].duplicated(keep=False)
        return data[duplicates]
    def check_null_value(self,edited_data):
        edited_check = pd.DataFrame(edited_data, columns=["ma_dv_id66", "ten_dv"])
        if edited_check.empty or edited_check.isna().any().any() or edited_check.isnull().any().any():
            st.toast("Dữ liệu trống hoặc chứa giá trị null!", icon="⚠️")
            return False
        empty_rows = {}
        columns=["ma_dv_id66", "ten_dv"]
        for column in columns:
            # Kiểm tra giá trị rỗng hoặc chỉ chứa khoảng trắng
            mask = edited_data[column].apply(lambda x: isinstance(x, str) and x.strip() == "")
            if mask.any():
                empty_rows[column] = edited_data[mask].index.tolist()
        if empty_rows:
            st.toast("Dữ liệu trống hoặc chứa giá trị null!", icon="⚠️")
            return False
        return True
    def validate_data_for_duplicates(self,edited_data, existing_data):
        """Kiểm tra trùng dữ liệu trong edited_data với dữ liệu hiện tại từ cơ sở dữ liệu."""
        status_check_na = self.check_null_value(edited_data)
        if status_check_na == False:
            return False
        duplicate_ma_dv_id66 = self.check_duplicate(edited_data, "ma_dv_id66")
        if not duplicate_ma_dv_id66.empty:
            st.warning("Mã dịch vụ (ma_dv_id66) bị trùng: " + ', '.join(duplicate_ma_dv_id66["ma_dv_id66"].values), icon="⚠️")
            return False
        existing_ma_dv_id66 = [row['ma_dv_id66'] for row in existing_data]
        duplicate_ma_dv_id66_db = edited_data[edited_data["ma_dv_id66"].isin(existing_ma_dv_id66)]
        if not duplicate_ma_dv_id66_db.empty:
            st.warning("Mã dịch vụ đã tồn tại trong cơ sở dữ liệu: " + ', '.join(duplicate_ma_dv_id66_db["ma_dv_id66"].values), icon="⚠️")
            return False
        return True
    def insert_service_to_database_ui(self,ma_dv_id66,ten_dv,danh_muc_tt):
        st.session_state.confirmation_insert = "Yes"
        conn = module_config.connect_to_mysql()
        existing_data = module_insert.fetch_all_services(conn)
        edited_data = pd.DataFrame({"ma_dv_id66": [ma_dv_id66], "ten_dv": [ten_dv], "danh_muc_tt": [danh_muc_tt]})
        if self.validate_data_for_duplicates(edited_data, existing_data):
            st.session_state.dialog_open_insert_service = False
            if module_insert.add_service_manage(ma_dv_id66,ten_dv,danh_muc_tt, conn):
                st.success("Dữ liệu đã được thêm thành công!", icon="✅")
                time.sleep(1.5)
                module_insert.load_data_service.clear()
                module_users.insert_action_check_user(st.session_state.usernamevnpt,st.session_state.line_access,"Thêm dịch vụ mới vào hệ thống")
                module_users.load_action_check_user.clear()
                st.rerun()
            else:
                st.error("Thêm dữ liệu thất bại.", icon="❌")
                time.sleep(1.5)
    @st.dialog("Thêm dịch vụ vào csdl", width="small")
    def dialog_open_for_insert(self):
        if "dialog_open_insert_service" not in st.session_state:
            st.session_state.dialog_open_insert_service = False
        if "confirmation_service_insert_dialog" not in st.session_state:
            st.session_state.confirmation_service_insert_dialog = None   
        if st.session_state.dialog_open_insert_service:
            
            st.write(f"🤔 Thêm dịch vụ mới vào csdl❗")
            dialog_insert_name_service = st.text_input("Nhập tên dịch vụ", key="dialog_insert_name_service")
            id_service_insert_dialog = st.text_input("Nhập mã dịch vụ", key="id_service_insert_dialog")
            category_service_dialog_insert = st.text_input("Nhập danh mục thông tin", key="category_service_dialog_insert")
            cols_insert_service_dialog = st.columns([1,1,1,1])
            button_insert_service = cols_insert_service_dialog[0].button(
                "Thêm",
                key="button_add_service_confirm",
                icon=":material/add_diamond:",
                type="secondary",use_container_width=True
            )
            if button_insert_service:
                if dialog_insert_name_service and id_service_insert_dialog:
                    if category_service_dialog_insert == None or category_service_dialog_insert == "":
                        category_service_dialog_insert = None
                    self.insert_service_to_database_ui(id_service_insert_dialog,dialog_insert_name_service,category_service_dialog_insert)
                else:
                    st.warning("Vui lòng nhập đủ thông tin!", icon="⚠️")
            button_cancel_service = cols_insert_service_dialog[1].button("Hủy",type="primary", icon=":material/close:", key="button_cancel_service",use_container_width=True)
        if button_cancel_service:
            st.session_state.confirmation_service_insert_dialog = "No"
            st.session_state.dialog_open_insert_service = False
            st.rerun()
        
    def upload_excel(self, key):
        uploaded_file = st.file_uploader("Chọn file Excel", type=["xlsx", "xls"], key=key)
        if uploaded_file is not None:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            if len(sheet_names) > 1:
                selected_sheet = st.selectbox("Chọn tab (sheet):", sheet_names)
            else:
                selected_sheet = sheet_names[0]
            try:
                # Đọc dữ liệu từ file Excel
                df = pd.read_excel(uploaded_file, sheet_name=selected_sheet, engine="openpyxl")
                st.dataframe(df, use_container_width=True)
                return df
            except Exception as e:
                st.error(f"Đã xảy ra lỗi: {str(e)}")
    

        
class FRONTEND_DESIGN_INSERT():
    def __init__(self):
        self.array_year_insert = range(2021,2030)
        self.now_year_index = self.array_year_insert.index(datetime.datetime.now().year)
        self.employee_list = nhanvien_after_load[nhanvien_after_load["line_nv"]==st.session_state.line_access]
        self.array_explan_em = self.employee_list[["ma_nv", "ten_nv"]].drop_duplicates()
        self.em_select_array = {row["ma_nv"]: row["ten_nv"] for _, row in self.array_explan_em.iterrows()}
        self.employee_keys = list(self.em_select_array.keys())
        
        # init line 
        self.array_line_selectbox = line_after_load.drop_duplicates()
        self.arr_line_select = {row["ma_line"]: row["ten_line"] for _, row in self.array_line_selectbox.iterrows()}
        self.selected_line_key =list(self.arr_line_select.keys())
    def spinner_load(self):
        with st.spinner("✨Đang thực hiện thao tác..."):
            time.sleep(2)
    
    def ui_info(self, text):
        st.markdown(f"<h3 style='text-align: left;'>{text}</h3>", unsafe_allow_html=True)
    def ui_info_add_search(self, text,loai_data):
        container_title_manage_expand = st.container(key="container_title_manage_expand")
        with container_title_manage_expand:
            col_title_dmanage_expand = st.columns([5,2])
            col_title_dmanage_expand[0].markdown(f"""<h3 style='text-align: left; padding:0'>{text}</h3>
                                            <p style='text-align: left; padding:0; margin-top: 5px;'>Danh sách các <span style="color:#c4c411; font-weight:bolder;"> {loai_data} </span></p>""", unsafe_allow_html=True)
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
    
            
    def streamlit_menu_sidebar_insert(self):
        with st.sidebar:
            module_config.show_expander_sidebar()
        container_sidebar_add_data = st.sidebar.container(key="container_sidebar_add_data")
        container_sidebar_add_data.markdown("<h3 style='text-align: center; padding:0; margin-bottom:5px;'>👨‍💼 THÊM DỮ LIỆU</h3>", unsafe_allow_html=True)
        with container_sidebar_add_data:
            selected = option_menu(
                menu_title= None,  # required
                options=["Kế hoạch", "Thực hiện","Quản lý dịch vụ","Biểu mẫu"],  # required
                icons=["eyedropper", "bar-chart-line-fill","gear-wide","filetype-xlsx"],  # optional
                menu_icon= None,  # optional
                default_index=0,  # optional
                orientation="vertical",
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

    def ui_plan_insert(self):
        container_plan_header = st.container(key="container_plan_insert_header")
        with container_plan_header:
            col_plan_insert_header = st.columns([20,10,10])
            with col_plan_insert_header[0]:
                self.ui_info(text="THÊM DỮ LIỆU - 📝KẾ HOẠCH")
            with col_plan_insert_header[1]:
                with st.popover("Thao tác",use_container_width=True, icon=":material/tune:"):
                    radio_option_action_in_plan = st.radio("📌Chọn chế độ:", ["Thêm", "Sửa","Xem"], key="radio_option_action_in_plan",horizontal=True)
                    form_service_selected_insert = st.selectbox("Chọn form dịch vụ phù hợp",["Thu gọn","Đầy đủ"],key="form_service_selected_insert")
            with col_plan_insert_header[2]:
                button_insert_plan = st.button("Up database", icon=":material/cloud_upload:", key="button_insert_plan",type="primary", 
                                               help="🔍Thêm dữ liệu vào csdl", use_container_width=True,
                                            #    on_click=self.spinner_load,
                                               disabled=(radio_option_action_in_plan == "Xem" or disabled_widget_experimental))
            
        if radio_option_action_in_plan == "Thêm":
            col_plan_insert_1,col_plan_insert_2 = st.columns(2)
            with col_plan_insert_1:
                selected_radio_plan = st.selectbox("Loại dữ liệu nhập:",["Theo tháng","Theo năm"], key="selected_radio_plan")
                
                selected_year_plan = st.selectbox("Chọn năm kế hoạch",self.array_year_insert, self.now_year_index , key="selected_year_plan")
                
            with col_plan_insert_2:
                if selected_radio_plan == "Theo tháng":
                    selected_revenue_plan = st.selectbox("Chọn doanh thu kế hoạch", ["Hiện hữu","Phát triển mới"], key="selected_revenue_plan")
                else:
                    selected_revenue_plan = st.selectbox("Chọn doanh thu kế hoạch", ["hiện hữu","mới trong tháng","mới trong năm","tổng doanh thu"], key="selected_revenue_plan")
                    
                selected_line_access = st.selectbox("Chọn line",options=self.selected_line_key, 
                                                format_func= lambda x: self.arr_line_select[x] if x else "",
                                                key = "selected_line_access_plan")
            file_upload_insert_value = ORTHER_FUNCTION_INSERT().upload_excel(key="file_upload_plan_insert")
                # part insert data
            if button_insert_plan:
                if file_upload_insert_value is not None:
                    module_config.create_db_pool()
                    conn = module_config.connect_to_mysql()
                    check_missing_columns_df = module_insert.validate_columns(file_upload_insert_value)
                    if check_missing_columns_df is False:
                        selected_radio_plan = "LDPVNPT" if selected_radio_plan == "Theo năm" else "LINE"
                        check_status_duplicate = module_insert.query_kehoach_by_line_year(selected_radio_plan,selected_line_access, selected_year_plan,selected_revenue_plan,conn)
                        if (check_status_duplicate.empty):
                            st.session_state.dialog_open = True
                        else:
                            st.toast("##### Dữ liệu đã tồn tại trong cơ sở dữ liệu!", icon="❌")
                            time.sleep(2)
                    else:
                        st.toast(f"##### Dữ liệu không đủ! Các cột bị thiếu: {', '.join(check_missing_columns_df)}",icon="⚠️")
                        time.sleep(2)
                else:
                    st.toast("##### Vui lòng tải lên file excel trước khi thực hiện thao tác!",icon="⚠️")
                    time.sleep(2)
            if st.session_state.get("dialog_open", False):
                module_config.show_confirmation_dialog("thêm dữ liệu kế hoạch")
            if "confirmation" in st.session_state:
                if st.session_state.confirmation == "Yes":
                    
                    module_config.create_db_pool()
                    conn = module_config.connect_to_mysql()
                    st.session_state.confirmation = None
                    result_services = module_insert.query_dichvu_from_database(conn)
                    data_insert_df = module_insert.select_rows_kehoach_for_insert(file_upload_insert_value, result_services,form_service_selected_insert)
                    selected_radio_plan = "LDPVNPT" if selected_radio_plan == "Theo năm" else "LINE"
                    result_insert_to_database = module_insert.insertData_kehoach_to_database(selected_radio_plan,selected_line_access,selected_year_plan,selected_revenue_plan,data_insert_df,conn)
                    if result_insert_to_database is True:
                        st.toast("##### Dữ liệu đã được thêm vào cơ sở dữ liệu!", icon="✅")
                        module_users.insert_action_check_user(st.session_state.usernamevnpt,selected_line_access,f"Thêm dữ liệu kế hoạch năm {selected_year_plan} loại - {selected_revenue_plan}")
                        module_users.load_action_check_user.clear()
                        time.sleep(2)
                        module_view.load_data_ldp.clear()
                        st.rerun()
                    else:
                        st.error(result_insert_to_database)
                        st.toast("##### Thêm dữ liệu thất bại!", icon="❌")
                        time.sleep(2)
        elif radio_option_action_in_plan == "Sửa":
            st.success("📌Chọn thông tin cần để sửa")
            cols_update_plan = st.columns(4)
            type_process_update_plan = cols_update_plan[0].selectbox("Chọn loại dữ liệu", ["Theo tháng","Theo năm"], key="type_process_update_plan")
            
            selected_year_update_plan = cols_update_plan[1].selectbox("Chọn năm kế hoạch",self.array_year_insert, self.now_year_index , key="selected_year_update_plan")
            if type_process_update_plan == "Theo tháng":
                selected_revenue_update_plan = cols_update_plan[3].selectbox("Chọn doanh thu kế hoạch", ["Hiện hữu","Phát triển mới"], key="selected_revenue_update_plan")
            else:
                selected_revenue_update_plan = cols_update_plan[3].selectbox("Chọn doanh thu kế hoạch", ["hiện hữu","mới trong tháng","mới trong năm","tổng doanh thu"], key="selected_revenue_update_plan")
            selected_line_update_plan = cols_update_plan[2].selectbox("Chọn line",options=self.selected_line_key,
                                                format_func= lambda x: self.arr_line_select[x] if x else "",
                                                key = "selected_line_update_plan")
            type_process_update_plan = "LDPVNPT" if type_process_update_plan == "Theo năm" else "LINE"
            data_source_update_plan = kehoach_after_load[(kehoach_after_load["type_process"] == type_process_update_plan) &
                                                        (kehoach_after_load["year_insert"] == selected_year_update_plan) & 
                                                        (kehoach_after_load["loaidoanhthu"] == selected_revenue_update_plan) & 
                                                        (kehoach_after_load["line"] == selected_line_update_plan)]
            if data_source_update_plan.empty:
                st.warning("Không có dữ liệu!")
            else:
                data_show_edit_plan = data_source_update_plan[["id_dv_606","t1","t2","t3","t4","t5","t6","t7","t8","t9","t10","t11","t12"]]
                for col in ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "t11", "t12"]:
                    data_show_edit_plan[col] = data_show_edit_plan[col] / 1000000
                data_show_edit_plan["ten_dv"] = data_show_edit_plan["id_dv_606"].map(dichvu_after_load.set_index("ma_dv_id66")["ten_dv"])
                data_show_edit_plan = data_show_edit_plan[["id_dv_606", "ten_dv", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "t11", "t12"]]
                edited_data_editor = st.data_editor(data_show_edit_plan, num_rows="fixed"
                                                    ,key="data_plan_editor_key", use_container_width=True,
                                                    disabled=(("id_dv_606","ten_dv")),hide_index=True)
                if button_insert_plan:
                    # Replace None or empty values with 0
                    edited_data_editor = edited_data_editor.fillna(0)
                    edited_data_editor = edited_data_editor.replace("", 0)
                    edited_data_editor = edited_data_editor.drop(columns=["ten_dv"])
                    data_show_updated = data_source_update_plan.copy()
                    data_show_updated.update(edited_data_editor)
                    
                    return_value_update = module_insert.update_table_kehoach(data_show_updated)
                    if return_value_update is True:
                        st.toast("##### Dữ liệu đã được cập nhật thành công!", icon="✅")
                        time.sleep(1.5)
                        module_view.load_data_ldp.clear()
                        st.rerun()
                    else:
                        st.toast("##### Cập nhật dữ liệu thất bại!", icon="❌")
                        st.warning(return_value_update)
                        time.sleep(1.5)
            
            # part view data
        else:
            cols_plan_view_before = st.columns(2)
            input_year_preview_plan = cols_plan_view_before[1].number_input("Nhập năm", min_value=2023, max_value=2030, key="input_year_preview_plan")
            selected_line_view_access_plan = cols_plan_view_before[1].selectbox("Chọn line",options=self.selected_line_key,
                                                format_func= lambda x: self.arr_line_select[x] if x else "",
                                                key = "selected_line_view_access_plan")
            selected_data_view_plan = cols_plan_view_before[0].selectbox("Chọn loại dữ liệu xem", ["Theo tháng","Theo năm"], key="selected_data_view_plan")
            if selected_data_view_plan == "Theo tháng":
                selected_view_plan = cols_plan_view_before[0].selectbox(label="Chọn loại doanh thu", options=["Hiện hữu","Phát triển mới"], key="selected_view_plan")
            else:
                selected_view_plan = cols_plan_view_before[0].selectbox(label="Chọn loại doanh thu", options=["hiện hữu","mới trong tháng","mới trong năm","tổng doanh thu"], key="selected_view_plan")
            button_view_plan = st.button("Xem data",icon=":material/frame_inspect:", key="button_view_plan", type="primary",on_click=self.spinner_load)
            if button_view_plan:
                selected_data_view_plan = "LDPVNPT" if selected_data_view_plan == "Theo năm" else "LINE"
                module_config.create_db_pool()
                conn = module_config.connect_to_mysql()
                data_kehoach_preview = module_insert.query_kehoach_by_line_year(selected_data_view_plan,selected_line_view_access_plan, input_year_preview_plan,selected_view_plan,conn)
                if data_kehoach_preview.empty:
                    st.warning("Không có dữ liệu!")
                else:
                    st.dataframe(data_kehoach_preview, use_container_width=True)
        
    def ui_make_project_insert(self):
        container_make_header = st.container(key="container_make_project_header")
        with container_make_header:
            col_make_project_header = st.columns([30,10,10])
            with col_make_project_header[0]:
                self.ui_info(text="THÊM DỮ LIỆU - 📇THỰC HIỆN")
            with col_make_project_header[2]:
                button_insert_project = st.button("Up database", icon=":material/cloud_upload:", key="button_insert_project",
                                                  type="primary", help="🔍Thêm dữ liệu vào csdl", use_container_width=True,
                                                  disabled=disabled_widget_experimental)
            with col_make_project_header[1]:
                with st.popover("Xem data", icon="👁️‍🗨️", help="🔍Xem data đang tồn tại trong csdl.", use_container_width=True):
                    radio_type_data_for_preview = st.radio(label="Chọn loại dữ liệu", options=["Theo tháng","Theo năm"], key="radio_type_data_for_preview",horizontal=True)
                    if radio_type_data_for_preview == "Theo tháng":
                        selectbox_preview_make_project = st.selectbox("Chọn loại doanh thu", ["Hiện hữu","Phát triển mới"], key="selectbox_preview_make_project")
                    else:
                        selectbox_preview_make_project = st.selectbox("Chọn loại doanh thu", ["hiện hữu","mới trong tháng","mới trong năm"], key="selectbox_preview_make_project")
                    radio_type_data_for_preview = "LDPVNPT" if radio_type_data_for_preview == "Theo năm" else "LINE"
                    input_year_preview_make_project = st.number_input("Nhập năm", min_value=2021, max_value=2030, key="input_year_preview_make_project")
                    button_view_make_project = st.button("🔍Xem data", key="button_view_make_project", type="primary")
        col_project_head_make_insert = st.columns(2)
        selected_type_data_make_insert = col_project_head_make_insert[0].selectbox("Chọn loại dữ liệu", ["Theo tháng","Theo năm"], key="selected_type_data_make_insert")
        with col_project_head_make_insert[1]:
            if selected_type_data_make_insert == "Theo tháng":
                selected_revenue_project = st.selectbox("Chọn doanh thu dự án", ["Hiện hữu","Phát triển mới"], key="selected_revenue_project")
            else:
                selected_revenue_project = st.selectbox("Chọn doanh thu dự án", ["hiện hữu","mới trong tháng","mới trong năm"], key="selected_revenue_project")
        col_project_insert_1,col_project_insert_2 = st.columns(2)
        with col_project_insert_1:
            selected_year_project = st.number_input("Chọn năm dự án",  min_value=2021, max_value=2030, key="selected_year_project")
        with col_project_insert_2:
            selected_month_make_value = st.selectbox("Chọn tháng thực hiện", [1,2,3,4,5,6,7,8,9,10,11,12], key="selected_month_make_value")
        
        selected_type_data_make_insert = "LDPVNPT" if selected_type_data_make_insert == "Theo năm" else "LINE"        
        file_upload_insert_make_value = ORTHER_FUNCTION_INSERT().upload_excel(key="file_upload_make_project_insert")
        if button_insert_project:
            
            if file_upload_insert_make_value is not None:
                check_data_frame_upload = module_insert.validate_thuchien_columns(file_upload_insert_make_value,selected_type_data_make_insert)
                if check_data_frame_upload is False:
                    module_config.create_db_pool()
                    conn = module_config.connect_to_mysql()
                    data_make_project_preview = module_insert.get_data_thuchien(selected_type_data_make_insert,selected_month_make_value,selected_year_project,selected_revenue_project,conn)
                    if data_make_project_preview.empty:
                        st.session_state.dialog_open = True
                    else:
                        st.toast("##### Dữ liệu đã tồn tại trong cơ sở dữ liệu!", icon="❌")
                        time.sleep(2)
                else:
                    st.toast(f"##### Dữ liệu không đủ! Cần thêm các cột sau: {', '.join(check_data_frame_upload)}",icon="⚠️")
                    time.sleep(2)
            else:
                st.toast("##### Vui lòng tải lên file excel trước khi thực hiện thao tác!",icon="⚠️")
                time.sleep(2)

        if st.session_state.get("dialog_open", False):
            module_config.show_confirmation_dialog("thêm dữ liệu")
        if "confirmation" in st.session_state:
            if st.session_state.confirmation == "Yes":
                st.session_state.confirmation = None
                self.spinner_load()
                module_config.create_db_pool()
                conn = module_config.connect_to_mysql()
                data_group_for_make_insert = module_insert.group_data_for_insert_thuchien(file_upload_insert_make_value,selected_type_data_make_insert)
                results_make_insert_status = module_insert.insert_data_to_thuchien(selected_type_data_make_insert,selected_month_make_value,selected_year_project,selected_revenue_project,data_group_for_make_insert,conn)
                if results_make_insert_status:
                    st.toast("##### Dữ liệu đã được thêm vào cơ sở dữ liệu!", icon="✅")
                    time.sleep(2)
                    module_users.insert_action_check_user(st.session_state.usernamevnpt,st.session_state.line_access,f"Thêm dữ liệu thực hiện năm {selected_year_project} tháng {selected_month_make_value} loại - {selected_revenue_project}")
                    module_users.load_action_check_user.clear()
                    module_view.load_data_ldp.clear()
                    st.rerun()
                else:
                    st.toast("##### Thêm dữ liệu thất bại!", icon="❌")
                    time.sleep(2)
        if button_view_make_project:
            self.spinner_load()
            module_config.create_db_pool()
            conn = module_config.connect_to_mysql()
            data_make_project_preview = module_insert.get_data_preview_for_insert_database(radio_type_data_for_preview,input_year_preview_make_project,selectbox_preview_make_project,conn)
            if data_make_project_preview.empty:
                st.warning("Không có dữ liệu!")
            else:
                st.dataframe(data_make_project_preview, use_container_width=True)
    def ui_management_service_insert(self, search_term_manage_service=None):
        module_config.create_db_pool()
        conn = module_config.connect_to_mysql()
        data = module_insert.load_data_service()
        data["delete"] = False
        
        if search_term_manage_service:
            data = data[data["ten_dv"].str.contains(search_term_manage_service, case=False)]
        # DOWNLOAD DATA   
        df_download_data = pd.DataFrame(data)
        output_xlsx_download = io.BytesIO()
        with pd.ExcelWriter(output_xlsx_download, engine='xlsxwriter') as writer:
            df_download_data.to_excel(writer, sheet_name='Sheet1', index=False)

        col_service_manage = st.columns([5,5,5,8,5])
        with col_service_manage[1]:
            insert_data_service = st.button("Thêm",use_container_width=True,icon=":material/variable_add:", key="insert_data_service", type="primary", help="Thêm dịch vụ mới")
        with col_service_manage[2]:
            download_data_service = st.download_button(label="Tải xuống", use_container_width=True, icon=":material/download:", data=output_xlsx_download, file_name="data_dichvu.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="download_data_service", type="primary", help="Tải xuống dữ liệu")
                
        with col_service_manage[0]:
            with st.popover("Chế độ",use_container_width=True, icon=":material/tune:"):
                view_mode_manage_service = st.radio("📌Chọn chế độ:", ["Xem", "Chỉnh sửa","Xóa"], key="view_mode_manage_service")
        with col_service_manage[4]:
            action_button_update_service = st.button("Cập nhật",icon=":material/sync_alt:", key="action_button_update_service", type="primary", use_container_width=True)
        container_second_service_content = st.container(key="container_second_service_content")
        with container_second_service_content:
            if view_mode_manage_service == "Xem":
                edited_data = st.data_editor(data, num_rows="dynamic",
                                                column_config={"ma_dv_id66": "Mã dịch vụ",
                                                            "ten_dv": "Tên dịch vụ",
                                                            "danh_muc_tt": "Danh mục cha",
                                                            "delete": "Chọn xóa"}, disabled=True, use_container_width=True)
            elif view_mode_manage_service == "Chỉnh sửa":
                default_index_for_select = data.columns.get_loc("ma_dv_id66")
                data = data.drop(columns=["delete"])
                edited_data = st.data_editor(data, num_rows="fixed",
                                                column_config={"ma_dv_id66": "Mã Dịch Vụ",
                                                                "ten_dv": "Tên Dịch Vụ",
                                                                "danh_muc_tt": "Danh Mục Thông Tin"
                                                                },disabled=(("ma_dv_id66",)) ,use_container_width=True)
            elif view_mode_manage_service == "Xóa":
                edited_data = st.data_editor(data, num_rows="fixed",
                                                column_config={"ma_dv_id66": "Mã dịch vụ",
                                                            "ten_dv": "Tên dịch vụ",
                                                            "danh_muc_tt": "Danh mục",
                                                            "delete": "Chọn xóa"}, disabled=(("ma_dv_id66","ten_dv","danh_muc_tt")), use_container_width=True)
        
        if insert_data_service:
            st.session_state.dialog_open_insert_service = True
        if st.session_state.get("dialog_open_insert_service", False):
            ORTHER_FUNCTION_INSERT().dialog_open_for_insert()
        if "confirmation_service_insert_dialog" in st.session_state:
            if st.session_state.confirmation_service_insert_dialog == "Yes":
                st.session_state.confirmation_service_insert_dialog = None  
        if action_button_update_service:
            orther_class_service = ORTHER_FUNCTION_INSERT()
            if view_mode_manage_service == "Chỉnh sửa":
                updated_rows = edited_data.to_dict('records')
                updated_data = [(row['ten_dv'], row['danh_muc_tt'], row['ma_dv_id66']) for row in updated_rows]
                if orther_class_service.check_null_value(edited_data) is True:
                    if module_insert.update_service_manage(updated_data, conn):
                        st.toast("##### Dữ liệu đã được cập nhật thành công!", icon="✅")
                        time.sleep(1.5)
                        module_insert.load_data_service.clear()
                        module_users.insert_action_check_user(st.session_state.usernamevnpt,st.session_state.line_access,"Cập nhật dữ liệu dịch vụ")
                        module_users.load_action_check_user.clear()
                        st.rerun()
                    else:
                        st.toast("##### Cập nhật dữ liệu thất bại. Tên hoặc mã dịch vụ có thể trùng lặp", icon="❌")
                        time.sleep(1.5)
            elif view_mode_manage_service == "Xóa":
                deleted_rows = edited_data[edited_data['delete']].to_dict('records')
                deleted_data = [(row['ma_dv_id66'],) for row in deleted_rows]
                if module_insert.delete_service_manage(deleted_data, conn):
                    st.toast("##### Dữ liệu đã được xóa thành công!", icon="✅")
                    time.sleep(1.5)
                    module_users.insert_action_check_user(st.session_state.usernamevnpt,st.session_state.line_access,f"Xóa dữ liệu dịch vụ{deleted_data}")
                    module_users.load_action_check_user.clear()
                    module_insert.load_data_service.clear()
                    st.rerun()
                else:
                    st.toast("##### Xóa dữ liệu thất bại.", icon="❌")
                    time.sleep(1.5)
            else:
                st.toast("##### Vui lòng chọn chế độ xem!",icon="⚠️")
                time.sleep(1.5)

    def ui_document_design(self, search_term=None):
        # Dữ liệu danh sách tài liệu
            
        docs = [
            {"id": 1, "title": "Mẫu thực hiện - Theo tháng", "author": "KHDN3", "source": "https://docs.google.com/spreadsheets/d/1slmL07m06EjaxTdjrmH3ScwhtqxykLQqD2CdmqDvc4A/edit?usp=sharing", "image": "../src/image_ex/logo_excel.png", "content": "Nội dung mẫu thực hiện - Theo tháng.","file_path":"data/form_data/form_thuchien_theothang.xlsx"},
            {"id": 2, "title": "Mẫu thực hiện - Theo năm", "author": "KHDN3", "source": "https://docs.google.com/spreadsheets/d/1nvOHWM_JN4DFfkQfx6hZyMf3rCrH0y5sVWBRTCn5cs4/edit?usp=sharing", "image": "../src/image_ex/logo_excel.png", "content": "Nội dung mẫu thực hiện - Theo năm.", "file_path":"data/form_data/form_thuchien_theonam.xlsx"},
            {"id": 3, "title": "Mẫu kế hoạch - Theo tháng", "author": "KHDN3", "source": "https://docs.google.com/spreadsheets/d/1Pdz9mjsi91D2BlQeaKJkf2211Z8q5zQi5hk3A-5Vezo/edit?usp=sharing", "image": "../src/image_ex/logo_excel.png", "content": "Nội dung mẫu kế hoạch - Theo tháng.","file_path":"data/form_data/form_kehoach_theothang.xlsx"},
            {"id": 4, "title": "Mẫu kế hoạch - Theo năm", "author": "KHDN3", "source": "https://docs.google.com/spreadsheets/d/1zkOQ6ibEuaGb-_bxatvMqMerG5rG2npisLW3JtNDWiM/edit?usp=sharing", "image": "../src/image_ex/logo_excel.png", "content": "Nội dung mẫu kế hoạch - Theo năm.","file_path":"data/form_data/form_kehoach_theonam.xlsx"},
        ]

        # Kiểm tra trạng thái tài liệu đang được chọn
        if "selected_doc" not in st.session_state:
            st.session_state.selected_doc = None

        def show_document_detail(doc_id):
            """Hiển thị chi tiết tài liệu."""
            st.session_state.selected_doc = next((doc for doc in docs if doc["id"] == doc_id), None)

        def back_to_list():
            """Quay lại danh sách tài liệu."""
            st.session_state.selected_doc = None

        # Hiển thị chi tiết tài liệu nếu có
        if st.session_state.selected_doc:
            doc = st.session_state.selected_doc
            st.markdown(f"""<h4 style="text-align:center; margin-top:0;">{doc["title"]}</h4>""",unsafe_allow_html=True)
            cols_show_doc = st.columns([0.6,0.8,0.7,1,1,1])
            cols_show_doc[0].button("Quay lại",icon=":material/arrow_back:", on_click=back_to_list)
            cols_show_doc[1].button(
                "Google Sheet",
                icon=":material/open_in_new:",
                on_click=lambda: module_insert.open_link(doc["source"])
            )

            file_content = module_insert.load_local_file(doc["file_path"])
            if file_content:
                cols_show_doc[2].download_button(
                    label="Tải xuống",
                    data=file_content,
                    file_name=f"{doc['title']}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    icon=":material/download:",
                )
            # container_iframe = st.container(key="container_iframe")
            # with container_iframe:
            components.html(f'<iframe src="{doc["source"]}" width="100%" height="1000px" style="border-radius:15px;border:None;"></iframe>', height=1000)
            
        else:
            container_first_document = st.container(key="container_first_document")
            
            with container_first_document:
                columns_per_row = 4
                if search_term:
                    search_term = search_term.lower()
                    docs = [doc for doc in docs if search_term in doc["title"].lower() or search_term in doc["content"].lower()]
                    columns_per_row = len(docs) if len(docs) < 4 else 4
                for i in range(0, len(docs), columns_per_row):
                    cols = st.columns(columns_per_row)
                    for j in range(columns_per_row):
                        if i + j < len(docs):
                            doc = docs[i + j]
                            with cols[j]:
                                image_file_path = module_config.get_relative_file_path(doc["image"])
                                st.markdown(f"""<img src="data:image/png;base64,{image_file_path}" style="height:10vh;"></img>""", unsafe_allow_html=True)
                                st.markdown(f"**{doc['title']}**")
                                st.write(f"Tác giả: **{doc['author']}**")
                                st.button("Xem chi tiết", icon=":material/description:" ,key=f"doc_{doc['id']}", on_click=show_document_detail, args=(doc["id"],))
    
class MAIN_APP_INSERT():
    def __init__(self):
        pass
    def main(self, selected):
        ui = FRONTEND_DESIGN_INSERT()
        if selected == "Kế hoạch":
            ui.ui_plan_insert()
        elif selected == "Thực hiện":
            ui.ui_make_project_insert()
        elif selected == "Quản lý dịch vụ":
            search_term_manage_service = ui.ui_info_add_search(text="⚙️QUẢN LÝ DỊCH VỤ",loai_data="dịch vụ")
            ui.ui_management_service_insert(search_term_manage_service)
        elif selected == "Biểu mẫu":
            search_term = ui.ui_info_add_search(text="📄BIỂU MẪU",loai_data="biểu mẫu")
            ui.ui_document_design(search_term)
            
        
thuchien_after_load, kehoach_after_load, nhanvien_after_load, dichvu_after_load,line_after_load = module_view.load_data_ldp()
ui = FRONTEND_DESIGN_INSERT()
main_app_insert = MAIN_APP_INSERT()
selected_sidebar_menu = ui.streamlit_menu_sidebar_insert()
main_app_insert.main(selected_sidebar_menu)
module_config.add_sidebar_footer()
    