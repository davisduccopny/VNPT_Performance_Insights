import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import io
import time
import PROJECTS.config as module_config
import LDP_MODULE.ldp_view as module_view
import LDP_MODULE.ldp_delete as module_delete
import PROJECTS.module_users as module_users

# PATH CONFIG
with open('src/style.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('src/style_general.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('src/style_delete.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

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



class ORTHER_FUNCTION_INSERT():
    def __init__(self):
        pass
    def get_data_from_kehoach_for_view(self,radio_type_process_delete,kehoach_after_load_dl,line_delete, selected_year_delete, search_term=None):
        kehoach_after_filter = kehoach_after_load_dl[(kehoach_after_load_dl["year_insert"] == selected_year_delete) & 
                                                      (kehoach_after_load_dl["line"] == line_delete) &
                                                      (kehoach_after_load_dl["type_process"] == radio_type_process_delete)].reset_index(drop=True)
        unique_kehoach_for_delete = kehoach_after_load_dl[(kehoach_after_load_dl["year_insert"] == selected_year_delete) & 
                                  
                                  (kehoach_after_load_dl["type_process"] == radio_type_process_delete)][["year_insert", "line", "loaidoanhthu"]].drop_duplicates(subset=["year_insert", "line", "loaidoanhthu"]).reset_index(drop=True)
        unique_kehoach_for_delete["ten_line"] = unique_kehoach_for_delete["line"].map(lambda x: line_after_load_dl.loc[line_after_load_dl["ma_line"] == x, "ten_line"].values[0] if not line_after_load_dl.loc[line_after_load_dl["ma_line"] == x, "ten_line"].empty else None)
        if search_term:
            kehoach_after_filter = kehoach_after_filter[kehoach_after_filter.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)].reset_index(drop=True)
            unique_kehoach_for_delete = unique_kehoach_for_delete[unique_kehoach_for_delete.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)].reset_index(drop=True)
        else:
            pass
                                                    
        return kehoach_after_filter, unique_kehoach_for_delete
    def get_data_from_thuchien_for_view(self,radio_type_process_delete,thuchien_after_load_dl, selected_year_delete, selected_loaidoanhthu_delete, selected_month_delete, search_term=None):
        thuchien_after_filter = thuchien_after_load_dl[(thuchien_after_load_dl["type_process"] == radio_type_process_delete) &
                                                        (thuchien_after_load_dl["year_insert"] == selected_year_delete) &
                                                        (thuchien_after_load_dl["loaidoanhthu"] == selected_loaidoanhthu_delete) &
                                                        (thuchien_after_load_dl["thang"] == selected_month_delete)].reset_index(drop=True)
        unique_thuchien_for_delete = thuchien_after_load_dl[(thuchien_after_load_dl["type_process"] == radio_type_process_delete) &
                                                            (thuchien_after_load_dl["year_insert"] == selected_year_delete) &
                                                            (thuchien_after_load_dl["loaidoanhthu"] == selected_loaidoanhthu_delete)][["year_insert","thang", "loaidoanhthu"]].drop_duplicates(subset=["year_insert","thang", "loaidoanhthu"]).reset_index(drop=True)
        if search_term:
            thuchien_after_filter = thuchien_after_filter[thuchien_after_filter.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)].reset_index(drop=True)
            unique_thuchien_for_delete = unique_thuchien_for_delete[unique_thuchien_for_delete.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)].reset_index(drop=True)
        else:
            pass
        return thuchien_after_filter, unique_thuchien_for_delete
        
class FRONTEND_DESIGN_DELETE():
    def __init__(self):
        self.array_line_selectbox = line_after_load_dl.drop_duplicates()
        self.arr_line_select = {row["ma_line"]: row["ten_line"] for _, row in self.array_line_selectbox.iterrows()}
        self.selected_line_key =list(self.arr_line_select.keys())
    def ui_info(self, text,loai_data):
        container_title_delete = st.container(key="container_title_delete")
        with container_title_delete:
            col_title_delete = st.columns([5,2])
            col_title_delete[0].markdown(f"""<h3 style='text-align: left; padding:0'>{text}</h3>
                                            <p style='text-align: left; padding:0'>Thao tác xóa dữ liệu <span style="color:#c4c411; font-weight:bolder;"> {loai_data} </span> cho line</p>""", unsafe_allow_html=True)
            with col_title_delete[1]:
                with st.form(key="search_form", enter_to_submit=True,border=False):
                    cols_search = st.columns([6,1])
                    search_term = cols_search[0].text_input(label=" ",placeholder="Tìm kiếm thông tin", key="search_term",type="default")
                    if cols_search[1].form_submit_button("🔍",use_container_width=True):
                        if search_term:
                            return search_term
                        else:
                            st.toast(f"#### Vui lòng nhập thông tin!", icon="⚠️")
                            return None
        # reconnect = st.sidebar.button("reconnect", key="reconnect",on_click=module_config.reconnect_if_needed,type="primary", icon=":material/refresh:")
    def streamlit_menu_sidebar_delete(self):
        # st.sidebar.write("Chế độ xem:")
        with st.sidebar:
            module_config.show_expander_sidebar()
            selected = option_menu(
                menu_title= None,  # required
                options=["Kế hoạch", "Thực hiện"],  # required
                icons=["eyedropper", "bar-chart-line-fill"],  
                menu_icon= None,  
                default_index=0,  
                orientation="horizontal",  
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
    
    def ui_sidebar_option(self, selected):

        radio_type_process_delete = st.sidebar.radio("Chọn loại dữ liệu",["Theo tháng","Theo năm"], key="radio_type_process_delete",horizontal=True)
        radio_type_process_delete = "LDPVNPT" if radio_type_process_delete == "Theo năm" else "LINE"
        if selected == "Kế hoạch":
            line_delete = st.sidebar.selectbox("Chọn line", self.selected_line_key, format_func=lambda x: self.arr_line_select[x], key="line_delete")
            selected_year_delete = st.sidebar.selectbox("Chọn năm",kehoach_after_load_dl["year_insert"].astype(int).unique(), key="selected_year_delete")
            selected_loaidoanhthu_delete = None 
            selected_month_delete = None
        else:
            line_delete = st.session_state.line_access
            selected_year_delete = st.sidebar.selectbox("Chọn năm",thuchien_after_load_dl["year_insert"].astype(int).unique(), key="selected_year_delete")
            selected_loaidoanhthu_delete = st.sidebar.selectbox("Chọn loại doanh thu", thuchien_after_load_dl[thuchien_after_load_dl["type_process"]==radio_type_process_delete]["loaidoanhthu"].unique(), key="selected_loaidoanhthu_delete")
            selected_month_delete = st.sidebar.selectbox("Chọn tháng",thuchien_after_load_dl["thang"].unique(), key="selected_month_delete")
        return radio_type_process_delete,selected_year_delete, selected_loaidoanhthu_delete, selected_month_delete, line_delete
    def delete_kehoach(self,radio_type_process_delete,selected_year_delete,line_delete, search_term):
        kehoach_after_filter, unique_kehoach_for_delete = ORTHER_FUNCTION_INSERT().get_data_from_kehoach_for_view(radio_type_process_delete,kehoach_after_load_dl,line_delete, selected_year_delete, search_term)
        unique_kehoach_for_delete["Delete"] = False
        df_download_data = pd.DataFrame(kehoach_after_filter)
        output_xlsx_download = io.BytesIO()
        with pd.ExcelWriter(output_xlsx_download, engine='xlsxwriter') as writer:
            df_download_data.to_excel(writer, sheet_name='Sheet1', index=False)
            
        container_header_plan_delete = st.container(key="container_header_plan_delete")
        cols_plan_delete = container_header_plan_delete.columns([3,3,9.5,6,0.5])
        button_delete_kehoach = cols_plan_delete[3].button("Xóa khỏi csdl", key="delete_plan", type="primary",icon=":material/delete:",disabled=disabled_widget_experimental,use_container_width=True)
        button_refress_pade = cols_plan_delete[0].button("Load", key="refress_page_delete_plan", type="secondary",use_container_width=True,icon=":material/published_with_changes:")
        button_export_excel =cols_plan_delete[1].download_button("Excel", key="export_excel_page_plan",use_container_width=True, help="Xuất excel",
                                                                        data=output_xlsx_download.getvalue(),
                                                                        file_name="plan_after_filter.xlsx",
                                                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", icon=":material/file_export:")
        with container_header_plan_delete:
            container_delete_second = st.container(key="container_delete_second")
            with container_delete_second:
                tabs_plan_delete = st.tabs(["⚡Thao tác","📑Chi tiết"])
                with tabs_plan_delete[0]:
                    delete_data = st.data_editor(unique_kehoach_for_delete, num_rows="fixed",
                                                    column_config={"year_insert": "Năm",
                                                                "line": "Line",
                                                                "loaidoanhthu": "Loại doanh thu",
                                                                "Delete": "Chọn xóa"}, disabled=(("year_insert","line","loaidoanhthu")), use_container_width=True,
                                                    hide_index=True)
                    deleted_rows = delete_data[delete_data['Delete']].to_dict('records')
                    deleted_data_delete = [(row['year_insert'],row['line'],row['loaidoanhthu']) for row in deleted_rows]
                    if button_delete_kehoach:
                        
                        
                        if deleted_rows == [] or deleted_rows == None:
                            st.toast("##### Bạn chưa chọn dữ liệu để xóa!", icon="⚠️")
                            time.sleep(2)
                        else:
                            st.session_state.dialog_open = True
                    if st.session_state.get("dialog_open", False):
                        module_config.show_confirmation_dialog("xóa dữ liệu")
                    if "confirmation" in st.session_state:
                        if st.session_state.confirmation == "Yes":
                            st.session_state.confirmation = None
                            with st.spinner("⛔ Đang xóa dữ liệu..."):
                                time.sleep(2)
                            
                            if module_delete.delete_plan(radio_type_process_delete,deleted_data_delete):
                                st.success("Xóa dữ liệu thành công!")
                                time.sleep(2)
                                module_users.insert_action_check_user(st.session_state.usernamevnpt,line_delete,f"Xóa dữ liệu kế hoạch {deleted_data_delete}")
                                module_users.load_action_check_user.clear()
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error("Xóa dữ liệu thất bại!")
                with tabs_plan_delete[1]:
                    st.dataframe(kehoach_after_filter,use_container_width=True, hide_index=True)
    def delete_thuchien(self,radio_type_process_delete, thuchien_after_load_dl,line_delete, selected_year_delete, selected_loaidoanhthu_delete, selected_month_delete, search_term):
        thuchien_after_filter, unique_thuchien_for_delete = ORTHER_FUNCTION_INSERT().get_data_from_thuchien_for_view(radio_type_process_delete,thuchien_after_load_dl, selected_year_delete, selected_loaidoanhthu_delete, selected_month_delete, search_term)
        unique_thuchien_for_delete["Delete"] = False
        # download excel
        df_download_data = pd.DataFrame(thuchien_after_filter)
        output_xlsx_download = io.BytesIO()
        with pd.ExcelWriter(output_xlsx_download, engine='xlsxwriter') as writer:
            df_download_data.to_excel(writer, sheet_name='Sheet1', index=False)
        container_header_do_delete = st.container(key="container_header_do_delete")
        with container_header_do_delete:
            cols_do_delete = container_header_do_delete.columns([3,3,9.5,6,0.5])
            button_delete_do = cols_do_delete[3].button("Xóa khỏi csdl", key="delete_do_out_db", type="primary",icon=":material/delete:",disabled=disabled_widget_experimental,use_container_width=True)
            button_refress_pade = cols_do_delete[0].button("Load", key="refress_page_delete", type="secondary",use_container_width=True,icon=":material/published_with_changes:")
            button_export_excel =cols_do_delete[1].download_button("Excel", key="export_excel_page_do",use_container_width=True, help="Xuất excel",
                                                                        data=output_xlsx_download.getvalue(),
                                                                        file_name="Do_after_filter.xlsx",
                                                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", icon=":material/file_export:")
            with container_header_do_delete:
                container_delete_second = st.container(key="container_delete_second")
                with container_delete_second:
                    tabs_do_delete = st.tabs(["⚡Thao tác","📑Chi tiết"])
                    with tabs_do_delete[0]:
                        delete_data = st.data_editor(unique_thuchien_for_delete, num_rows="fixed",
                                                        column_config={"year_insert": "Năm",
                                                                    "thang": "Tháng",
                                                                    "loaidoanhthu": "Loại doanh thu",
                                                                    "Delete": "Chọn xóa"}, 
                                                        disabled=(("year_insert","thang","loaidoanhthu")), use_container_width=True,
                                                        hide_index=True)
                        deleted_rows = delete_data[delete_data['Delete']].to_dict('records')
                        deleted_data_delete = [(row['thang'],row['year_insert'],row['loaidoanhthu']) for row in deleted_rows]
                        if button_delete_do:
                            if deleted_rows == [] or deleted_rows == None:
                                st.toast("##### Bạn chưa chọn dữ liệu để xóa!", icon="⚠️")
                                time.sleep(2)
                            else:
                                st.session_state.dialog_open = True
                        if st.session_state.get("dialog_open", False):
                            module_config.show_confirmation_dialog("xóa dữ liệu")
                        if "confirmation" in st.session_state:
                            if st.session_state.confirmation == "Yes":
                                st.session_state.confirmation = None
                                with st.spinner("⛔ Đang xóa dữ liệu..."):
                                    time.sleep(2)
                                if module_delete.delete_thuchien_from_data(radio_type_process_delete,deleted_data_delete):
                                    st.success("Xóa dữ liệu thành công!")
                                    time.sleep(2)
                                    module_users.insert_action_check_user(st.session_state.usernamevnpt,line_delete,f"Xóa dữ liệu thực hiện tháng {deleted_data_delete}")
                                    module_users.load_action_check_user.clear()
                                    st.cache_data.clear()
                                    st.rerun()
                                else:
                                    st.error("Xóa dữ liệu thất bại!")
                                
                        
                    with tabs_do_delete[1]:
                        st.dataframe(thuchien_after_filter,use_container_width=True, hide_index=True)
class MAIN_APP_DELETE():
    def __init__(self):
        pass
    def main(self, selected):
        ui = FRONTEND_DESIGN_DELETE()
        self.loai_data = None
        self.search_term = None

        if selected == "Kế hoạch":
            self.loai_data = "Kế hoạch"
            radio_type_process_delete,selected_year_delete, selected_loaidoanhthu_delete, selected_month_delete, line_delete = ui.ui_sidebar_option(selected)
            self.search_term = ui.ui_info(text="XÓA DỮ LIỆU - 📝KẾ HOẠCH",loai_data=self.loai_data)
            ui.delete_kehoach(radio_type_process_delete,selected_year_delete,line_delete, self.search_term)
        elif selected == "Thực hiện":
            self.loai_data = "Thực hiện"
            radio_type_process_delete,selected_year_delete, selected_loaidoanhthu_delete, selected_month_delete, line_delete = ui.ui_sidebar_option(selected)
            self.search_term = ui.ui_info(text="XÓA DỮ LIỆU - 📇THỰC HIỆN",loai_data=self.loai_data)
            ui.delete_thuchien(radio_type_process_delete,thuchien_after_load_dl,line_delete, selected_year_delete, selected_loaidoanhthu_delete, selected_month_delete, self.search_term)

            
        

thuchien_after_load_dl, kehoach_after_load_dl, nhanvien_after_load_dl, dichvu_after_load_dl,line_after_load_dl = module_view.load_data_ldp()
ui = FRONTEND_DESIGN_DELETE()
main_app_delete = MAIN_APP_DELETE()
selected_sidebar_menu = ui.streamlit_menu_sidebar_delete()
main_app_delete.main(selected_sidebar_menu)
module_config.add_sidebar_footer()
        