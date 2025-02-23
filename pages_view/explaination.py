import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import datetime
import EM_MODULE.config as module_config
from EM_MODULE.module_insert import load_data_service
from EM_MODULE.module_todo import load_tasks as load_data_todo
from EM_MODULE.module_view import load_data as load_data_from_all
from EM_MODULE.module_view import format_number as format_number
from LDP_MODULE.ldp_view import load_data_ldp
import EM_MODULE.module_explaination as module_explaination

with open('src/style_general.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True) 
with open('src/style_explaination.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
     
class Explaination:
    def __init__(self):
        self.employee_array = nhanvien_after_load[nhanvien_after_load["line_nv"]==st.session_state.line_access]
        self.year_select = thuchien_after_load["year_insert"].unique()
        self.month_select = {"Tháng 1" : 1,"Tháng 2" : 2,"Tháng 3" : 3,"Tháng 4" : 4,"Tháng 5" : 5,"Tháng 6" : 6,"Tháng 7" : 7,"Tháng 8" : 8,"Tháng 9" : 9,"Tháng 10" : 10,"Tháng 11" : 11,"Tháng 12" : 12}
        self.month_key_show = self.month_select.keys()
        
        self.unique_months = thuchien_after_load[(thuchien_after_load["year_insert"] == thuchien_after_load["year_insert"].unique().max()) &
                                                 (thuchien_after_load["type_process"] == "LINE")]["thang"].unique()
        self.unique_months = [int(month) for month in self.unique_months]
        self.max_month = max(self.unique_months)
        self.month_now_index = list(self.month_select.values()).index(self.max_month)
    def explaination_dashboard(self):
        ctn_header_explain = st.container(key="ctn_header_explain")
        with ctn_header_explain:
            cols_header = st.columns([1.2, 1, 1, 1, 1])
            with cols_header[1]:
                year_selected = st.selectbox("Năm", self.year_select, index=list(self.year_select).index(self.year_select.max()), key="year_selected_explain")
            with cols_header[2]:
                month_selected = st.selectbox("Tháng",self.month_key_show, index=self.month_now_index , key="month_selected_explain")
                month_selected = self.month_select[month_selected]
            with cols_header[3]:
                loaidoanhthu_selected = st.selectbox("Loại doanh thu",[ "Phát triển mới","Hiện hữu"], key="loaidoanhthu_selected_explain")
            with cols_header[4]:
                array_explan_em = self.employee_array[["ma_nv", "ten_nv"]].drop_duplicates()
                em_select_array = {row["ma_nv"]: row["ten_nv"] for _, row in array_explan_em.iterrows()}
                employee_keys = [""] + list(em_select_array.keys())
                employee_selected = st.selectbox("Nhân viên",
                                                 options=employee_keys,
                                                 format_func=lambda x: em_select_array[x] if x else ""
                                                 , key="employee_selected_explain")
            with cols_header[0]:
                st.subheader("Compare dashboard")
        data_task_show,thuchien_show,kehoach_show,nhanvien_show = module_explaination.data_layer_set(data_task_all,thuchien_after_load,kehoach_after_load,nhanvien_after_load,int(year_selected),int(month_selected),loaidoanhthu_selected,employee_selected)
        ctn_first_main_explain = st.container(key="ctn_first_main_explain")
        with ctn_first_main_explain:
            cols_first_main_ex = st.columns(2)
            with cols_first_main_ex[0]:
                column_chart,data_result = module_explaination.Column_chart_fisrt_ctn(data_task_show,thuchien_show,nhanvien_show)
                if column_chart is not None:
                    select_param = st.altair_chart(column_chart, on_select="rerun", key="column_chart_explain", use_container_width=True)
                else:
                    select_param = None
                    st.write("Không có dữ liệu")
            with cols_first_main_ex[1]:
                donut_chart = module_explaination.Donut_chart_explain(data_result, select_param)
                if donut_chart is not None:
                    st.altair_chart(donut_chart, use_container_width=True,key="donut_chart_explain")
        ctn_second_main_explain = st.container(key="ctn_second_main_explain")
        with ctn_second_main_explain:
            cols_second_main_ex = st.columns([1,1])
            with cols_second_main_ex[0]:
                
                    data_compare = module_explaination.Table_service_filter(data_task_show,nhanvien_after_load,dichvu_after_load,thuchien_show,select_param)
                    st.dataframe(data_compare, column_config={
                        "employee": "Nhân viên",
                        "service": "Dịch vụ",
                        "revenue_th": "Thực nhập",
                        "revenue": "Kế toán",
                        "rate": "Tỷ lệ",
                        "subtract": "Chênh lệch"
                    },height=240,hide_index=True,use_container_width=True)
            with cols_second_main_ex[1]:
                if data_compare is not None:
                    metric_count_subtract = data_compare[data_compare["subtract"] > 0]["subtract"].count()
                    metric_sum_subtract = data_compare[data_compare["subtract"] > 0]["subtract"].sum()
                    metric_not_complete = data_compare[data_compare["subtract"] < 0]["subtract"].count()
                    metric_sum_not_complete = abs(data_compare[data_compare["subtract"] < 0]["subtract"].sum())
                else:
                    metric_count_subtract = 0
                    metric_sum_subtract = 0
                    metric_not_complete = 0
                    metric_sum_not_complete = 0
                ctn_chidren = st.container(key="ctn_chidren_second_main_explain")
                
                
                with ctn_chidren:
                    cols_metric = st.columns(2)
                    with cols_metric[0]:
                        ctn_children_1 = st.container(key="ctn_children_1")
                        ctn_children_2 = st.container(key="ctn_children_2")
                        ctn_children_1.metric(label="Số dịch vụ chênh lệch", value=metric_count_subtract)
                        ctn_children_1.caption("Chênh lệch dương ")
                        ctn_children_2.metric(label="Tổng chênh lệch", value=format_number(metric_sum_subtract))
                        ctn_children_2.caption("Tổng chênh lệch dương")
                    with cols_metric[1]:
                        ctn_children_3 = st.container(key="ctn_children_3")
                        ctn_children_4 = st.container(key="ctn_children_4")
                        ctn_children_3.metric(label="Số dịch vụ chưa hoàn thành", value=metric_not_complete)
                        ctn_children_3.caption("Chênh lệch âm")
                        ctn_children_4.metric(label="Tổng số chưa hoàn thành", value=format_number(metric_sum_not_complete))
                        ctn_children_4.caption("Tổng chênh lệch âm")
    def management_explaination(self):
        ctn_first_manage_explain = st.container(key="ctn_first_manage_explain")
        with ctn_first_manage_explain:
            with st.expander("__", expanded=True):
                st.subheader("Thêm giải trình")
                cols_fist_main = st.columns([4,1])
                with cols_fist_main[1]: 
                    audio_change_recorder = st.audio_input("____", key="audio_change_recorder", on_change=module_explaination.audio_to_text, args=("audio_change_recorder","content_explain_text"))                  
                with cols_fist_main[0]:
                    content_explain_text = st.text_area("Nội dung giải trình",value=st.session_state.get("content_explain_text", ""), key="content_explain_text",)
                submit_button_explain = st.button("Submit",key="submit_explain",on_click=module_explaination.insert_explain_to_database, args=(content_explain_text,))
        ctn_second_manage_explain = st.container(key="ctn_second_manage_explain")
        with ctn_second_manage_explain:
            month_explaination_edit = datetime.datetime.now().month
            with st.expander(f"Chỉnh sửa giải trình tháng {month_explaination_edit}"):
                st.subheader("Thông tin chỉnh sửa")
                if "content_explain_text_edit" not in st.session_state:
                    data_edit = module_explaination.get_explain_by_user_from_database()
                    if data_edit is not None:
                        st.session_state.content_explain_text_edit = data_edit
                
                audio_change_recorder_edit = st.audio_input("____", key="audio_change_recorder_edit", on_change=module_explaination.audio_to_text, args=("audio_change_recorder_edit","content_explain_text_edit"))
                content_explain_text_edit = st.text_area("Nội dung giải trình",value=st.session_state.get("content_explain_text_edit", ""), key="content_explain_text_edit",)
                submit_button_explain_edit = st.button("Submit",key="submit_explain_edit", on_click=module_explaination.edit_explain_to_database, args=(content_explain_text_edit,))
            with st.expander("Quản lý",expanded=True):
                st.subheader("Danh sách giải trình")
                data_show_list_explain = module_explaination.query_explain_by_user_from_database()
                if data_show_list_explain is not None:
                    data_show_list_explain = data_show_list_explain[["id","content","line","month","year","created_at"]]
                    data_show_list_explain["line"] = data_show_list_explain["line"].map(line_after_load.set_index("ma_line")["ten_line"])
                    
                    st.dataframe(data_show_list_explain, column_config={
                        "id": "ID",
                        "content": "Nội dung",
                        "line": "Line",
                        "month": "Tháng",
                        "year": "Năm",
                        "created_at": "Ngày tạo"
                    },hide_index=True,use_container_width=True)
                else:
                    st.write("Không có dữ liệu")   
    def management_explain_linelv(self):
        with st.expander("Quản lý",expanded=True):
            st.subheader("Danh sách giải trình")
            data_show_list_explain = module_explaination.query_explain_by_user_from_database()
            if data_show_list_explain is not None:
                data_show_list_explain = data_show_list_explain[["id","content","line","month","year","created_at"]]
                data_show_list_explain["line"] = data_show_list_explain["line"].map(line_after_load.set_index("ma_line")["ten_line"])
                st.dataframe(data_show_list_explain, column_config={
                    "id": "ID",
                    "content": "Nội dung",
                    "line": "Line",
                    "month": "Tháng",
                    "year": "Năm",
                    "created_at": "Ngày tạo"
                },hide_index=True,use_container_width=True)
            else:
                st.write("Không có dữ liệu")                     
class MAIN_EXPLAINATION():
    def __init__(self):
        self.explaination = Explaination()
    def explaination_sidebar_ui(self):
        if (st.session_state.type_process != "LDPVNPT" or st.session_state.role_access_admin != "admin"):
            option_show_menu = ["Compare Dashboard", "Quản lý"]
            icons_show_menu = ["clipboard-data", "calendar2-check"]
        else:
            option_show_menu = ["Quản lý"]
            icons_show_menu = ["calendar2-check"]
        with st.sidebar:
            selected = option_menu(
                    menu_title= None,  # required
                    options=option_show_menu,  # required
                    icons=icons_show_menu,
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
    def ui_info(self, text,loai_data):
        container_title_explain = st.container(key="container_title_explain")
        with container_title_explain:
            col_title_dmanage_expand = st.columns([5,2])
            col_title_dmanage_expand[0].markdown(f"""<h3 style='text-align: left; padding:0; margin-bottom:5px;'>{text}</h3>
                                            <p style='text-align: left; padding:0'>Thao tác quản lý <span style="color:#c4c411; font-weight:bolder;"> {loai_data} </span> cho line</p>""", unsafe_allow_html=True)
    def run(self):
        selected = self.explaination_sidebar_ui()
        if selected == "Compare Dashboard":
            self.explaination.explaination_dashboard()
        else:
            self.ui_info("Giải trình", "giải trình")
            if st.session_state.type_process != "LDPVNPT":
                self.explaination.management_explaination()
            else:
                self.explaination.management_explain_linelv()
if st.session_state.type_process == "LDPVNPT":
    thuchien_after_load, kehoach_after_load, nhanvien_after_load, dichvu_after_load,line_after_load = load_data_ldp()
else:
    thuchien_after_load, kehoach_after_load, nhanvien_after_load, dichvu_after_load,line_after_load = load_data_from_all() 
data_task_all = pd.DataFrame(load_data_todo())
data_service_all =load_data_service()  
MAIN_EXPLAINATION().run()
module_config.add_sidebar_footer()