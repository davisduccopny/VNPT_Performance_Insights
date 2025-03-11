import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import io
import altair as alt
import time
import datetime
import streamlit.components.v1 as components
import EM_MODULE.config as module_config
import EM_MODULE.module_insert as module_insert
import EM_MODULE.module_todo as module_todo
import EM_MODULE.module_view as module_view
from streamlit_calendar import calendar
import calendar as calendar_for_lv
import uuid
from zoneinfo import ZoneInfo
from streamlit_elements import elements, dashboard, mui


with open('src/style.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True) 
with open('src/style_general.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True) 
with open('src/style_todo.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True) 
class TOOL_FOR_UI():
    def __init__(self):
        pass
    def handle_timezone_change(self,date_click):
        utc_time_date_click = datetime.datetime.strptime(date_click, "%Y-%m-%dT%H:%M:%S.000Z")
        utc_time_date_click = utc_time_date_click.replace(tzinfo=ZoneInfo("UTC"))
        vietnam_time_click = utc_time_date_click.astimezone(ZoneInfo("Asia/Ho_Chi_Minh"))
        vietnam_time_click = vietnam_time_click.strftime("%Y-%m-%d")
        return vietnam_time_click
    def render_task_view(self,case):
        if case == "line_lv":

            st.markdown("""
            <h5 style='text-align: center; font-size: 1.3rem;padding:5px; font-weight: bold;border-bottom:2px solid blue;margin-bottom:15px;margin-top:20px'>Theo Line</h5>
            <h5 style='text-align: center; font-weight: bold;'> Các chế độ xem:</h5>
            <ul>
                <li>Dạng ngày</li>
                <li>Dạng danh sách</li>
                <li>Theo dịch vụ</li>
                <li>Theo nhân viên</li>
            </ul>
            <h5 style='text-align: center; font-weight: bold;'>Trạng thái</h5>
            <ul>
                <li>Chưa hoàn thành: <span style="color: #FF6C6C;">⬤</span></li>
                <li>Đã hoàn thành: <span style="color: rgb(111 238 128);">⬤</span></li>
                <li>Chờ: <span style="color: rgb(241 245 87);">⬤</span></li>
            </ul>
            """, unsafe_allow_html=True)
        if case == "employee_lv":
            st.markdown("""
            <h5 style='text-align: center; font-size: 1.3rem;padding:5px; font-weight: bold;border-bottom:2px solid blue;margin-bottom:5px;margin-top:20px'>Danh sách công việc</h5>
            <h5 style='text-align: center; font-weight: bold;'> Các chế độ xem:</h5>
            <ul>
                <li>Dạng ngày</li>
                <li>Dạng danh sách</li>
                <li>Theo dịch vụ</li>
                <li>Theo nhân viên</li>
            </ul>
            <h5 style='text-align: center; font-weight: bold;'>Trạng thái công việc</h5>
            <ul>
                <li>Chưa hoàn thành: <span style="color: #FF6C6C;">⬤</span></li>
                <li>Đã hoàn thành: <span style="color: rgb(111 238 128);">⬤</span></li>
                <li>Chờ: <span style="color: rgb(241 245 87);">⬤</span></li>
            </ul>
            """, unsafe_allow_html=True)
            
    def update_ui_calendar(self):
        st.session_state["events"] = str(uuid.uuid4())
        st.session_state["events_show_linelv"] = str(uuid.uuid4())
    def handle_row_click(self,params):
        st.toast(params["data"]["title"],params["data"]["name_service"],params["data"]["name_employee"],params["data"]["status"],params["data"]["start_date"],params["data"]["end_date"],params["data"]["revenue"],params["data"]["notes"])
    
class TODOCHECK_UI_DESIGN():
    def __init__(self):

        self.service_load_not_parent = dichvu_after_load[dichvu_after_load["danh_muc_tt"].notna()]
        self.service_load_not_parent = self.service_load_not_parent[~self.service_load_not_parent["danh_muc_tt"].isin(["1", "1.1.01", "1.1.02", "1.1.03", "1.1.05", "1.1.06", "1.1.07"])]
        self.employee_array = nhanvien_after_load[nhanvien_after_load["line_nv"]==st.session_state.line_access]
        
        self.em_select = {row["ma_nv"]: row["ten_nv"] for _, row in self.employee_array.iterrows()}
        self.selected_em_key =list(self.em_select.keys())
        self.time_now_init = data_task_all["end_date"].max() if not data_task_all.empty else datetime.datetime.now().date()
        self.time_now_init  = self.time_now_init.strftime("%Y-%m-%d")
        self.year_select = thuchien_after_load["year_insert"].unique()
        self.month_select = {"Tháng 1" : 1,"Tháng 2" : 2,"Tháng 3" : 3,"Tháng 4" : 4,"Tháng 5" : 5,"Tháng 6" : 6,"Tháng 7" : 7,"Tháng 8" : 8,"Tháng 9" : 9,"Tháng 10" : 10,"Tháng 11" : 11,"Tháng 12" : 12}
        self.month_key_show = self.month_select.keys()
        
        self.unique_months = thuchien_after_load[(thuchien_after_load["year_insert"] == thuchien_after_load["year_insert"].unique().max()) &
                                                 (thuchien_after_load["type_process"] == "LINE")]["thang"].unique()
        self.unique_months = [int(month) for month in self.unique_months]
        self.max_month = max(self.unique_months)
        self.month_now_index = list(self.month_select.values()).index(self.max_month)
    
    def calendar_show_line_lv_dash(self,data_task_all,options_show_radio,selected_em,selected_ser):
         # event
        data_task_all_show = data_task_all
        if selected_em != None:
            data_task_all_show = data_task_all_show[data_task_all_show["employee_id"] == selected_em]
        if selected_ser != "":
            data_task_all_show = data_task_all_show[data_task_all_show["service_id"] == selected_ser]
        if options_show_radio != "Theo nhân viên":
            data_tasks_renamed = data_task_all_show.rename(columns={
                "start_date": "start",
                "end_date": "end",
                "color": "color",
                "service_id": "resourceId",
            })
        else:
            data_tasks_renamed = data_task_all_show.rename(columns={
                "start_date": "start",
                "end_date": "end",
                "color": "color",
                "employee_id": "resourceId",
            })
        for col in ["start", "end"]:
            data_tasks_renamed[col] = pd.to_datetime(
                data_tasks_renamed[col], format="%d/%m/%Y", dayfirst=True
            ).dt.strftime("%Y-%m-%d")

        data_tasks_renamed= data_tasks_renamed[["id", "title", "start", "end", "color", "resourceId"]]
        events = data_tasks_renamed.to_dict('records')
        # service resource
        resource_service = self.service_load_not_parent.rename(columns={
            "ma_dv_id66": "id",
            "ten_dv": "title",
        })
        resource_service = resource_service[["id", "title"]]
        resource_service = resource_service[resource_service["id"].isin(data_tasks_renamed["resourceId"].unique())]
        resource_service = resource_service.to_dict("records")
        
        # employee resource
        resource_employee = self.employee_array.drop(columns=["id"])
        resource_employee = resource_employee.rename(columns={
            "ma_nv": "id",
            "ten_nv": "title",
        }).loc[:, ["id", "title"]]
        resource_employee = resource_employee.to_dict("records")
        
        calendar_options = {
            "editable": "true",
            "navLinks": "true",
            "resources": resource_service,
            "selectable": "true",
        }
        if options_show_radio == "Dạng ngày":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridDay,dayGridWeek,dayGridMonth",
                },
                "initialDate": self.time_now_init,
                "initialView": "dayGridMonth",
            }
        elif options_show_radio == "Dạng danh sách":
            calendar_options = {
                **calendar_options,
                "initialDate": self.time_now_init,
                "initialView": "listWeek",
                "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "listWeek",
            }}
        elif options_show_radio == "Theo dịch vụ":
            calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "prev,next",
                "center": "title",
                "right": "resourceTimelineMonth",
            },
            "initialDate": self.time_now_init,
            "initialView": "resourceTimelineMonth",
            "resourceGroupField": "title",
        }
        elif options_show_radio == "Theo nhân viên":
            calendar_options = {
            "editable": "true",
            "navLinks": "true",
            "selectable": "true",
            "headerToolbar": {
                "left": "prev,next",
                "center": "title",
                "right": "resourceTimelineMonth",
            },
            "initialDate": self.time_now_init,
            "initialView": "resourceTimelineMonth",
            "resources": resource_employee,
            "resourceGroupField": "title",
        }
        if not st.session_state.get("events_show_linelv", False):
            st.session_state["events_show_linelv"] = str(uuid.uuid4()) 
        state = calendar(
            events=events,
            options=calendar_options,
            callbacks="eventClick",
            custom_css="""
            .fc-event-past {
                opacity: 0.8;
            }
            .fc-event-time {
                font-style: italic;
            }
            .fc-event-title {
                font-weight: 600;
                color: rgb(0, 50, 73);
            }
            .fc-toolbar-title {
                font-size: 2rem;
            }
            """,
            key=str(st.session_state["events_show_linelv"]),
        )
        if state.get("eventClick"):
            task_id_viewed = state.get("eventClick")["event"]["id"]
            st.session_state.view_task_detail_linelv_dialog = True
            module_todo.view_task_linelv(data_service_all,data_task_all,task_id_viewed)
    @st.dialog("Thêm công việc mới")
    def add_new_task(self,data_service,date_click):
        if date_click:
            convert_dateclick = datetime.datetime.strptime(date_click, "%Y-%m-%d").date()
        else:
            convert_dateclick = datetime.datetime.now().date()
        data_service = data_service[data_service["danh_muc_tt"].notna()]
        data_service = data_service[~data_service["danh_muc_tt"].isin(["1", "1.1.01", "1.1.02", "1.1.03", "1.1.05", "1.1.06", "1.1.07"])]
        if "dialog_open_insert_tasks_2" not in st.session_state:
            st.session_state.dialog_open_insert_tasks_2 = False
        if "confirm_click_add" not in st.session_state:
            st.session_state.confirm_click_add = None   
        if st.session_state.dialog_open_insert_tasks_2:
            container_dialog_add_task = st.container(key="container_dialog_add_task")
            with container_dialog_add_task:                
                cols_dialog_add_task = st.columns([1,1])
                with cols_dialog_add_task[0]:
                    title_task_insert = st.text_input("Tiêu đề", key="click_title_task_insert")
                    service_task_insert = st.selectbox("Dịch vụ",data_service["ten_dv"].unique(), key="click_service_task_insert")
                    id_service_task_selected = data_service[data_service["ten_dv"] == service_task_insert]["ma_dv_id66"].values[0]
                    start_date_task_insert = st.date_input("Ngày bắt đầu",convert_dateclick,key="start_date_task_insert")
            
                with cols_dialog_add_task[1]:
                    status_task_insert = st.selectbox("Trạng thái",["Chưa hoàn thành","Đã hoàn thành","Chờ"], key="click_status_task_insert")
                    revenue_task_insert = st.number_input("Doanh thu", key="click_revenue_task_insert")
                    end_date_task_insert = st.date_input("Ngày kết thúc",convert_dateclick, key="click_end_date_task_insert")
                loai_doanh_thu = st.selectbox("Loại doanh thu",["Hiện hữu","Phát triển mới"], key="click_loai_doanh_thu")
                notes_task_insert = st.text_area("Ghi chú", key="click_notes_task_insert")
                if status_task_insert == "Chưa hoàn thành":
                    color_picker_insert_task = "#FF6C6C"
                elif status_task_insert == "Đã hoàn thành":
                    color_picker_insert_task = "rgb(111 238 128)"
                else:
                    color_picker_insert_task = "rgb(241 245 87)"
                cols_second_task_confirm = st.columns([1,1])
                button_insert_tasks = cols_second_task_confirm[0].button(
                        "Thêm",
                        key="click_button_add_task_confirm",
                        icon=":material/add_diamond:",
                        type="secondary",use_container_width=True
                        )
                button_cancel_tasks = cols_second_task_confirm[1].button("Hủy", key="click_button_cancel_task",icon=":material/close:",type="secondary",use_container_width=True)
                if button_cancel_tasks:
                    st.session_state.confirm_click_add = "No"
                    st.session_state.dialog_open_insert_tasks_2 = False
                    st.rerun()
                if button_insert_tasks:
                    with st.spinner("Đang thêm công việc..."):
                        if title_task_insert and service_task_insert and start_date_task_insert and status_task_insert and revenue_task_insert and end_date_task_insert:
                            if module_todo.insert_data_todocheck(title_task_insert,id_service_task_selected,st.session_state.employee_id,status_task_insert,start_date_task_insert,end_date_task_insert,revenue_task_insert,notes_task_insert,color_picker_insert_task,datetime.datetime.now(),loai_doanh_thu):
                                st.success("##### Thêm công việc thành công!")
                                time.sleep(1)
                                st.session_state.confirm_click_add = "Yes"
                                st.session_state.dialog_open_insert_tasks_2 = False
                                module_todo.load_tasks.clear()
                                st.session_state["events"] = str(uuid.uuid4())
                                st.rerun()
                            else:
                                st.warning("##### Có lỗi xảy ra, vui lòng thử lại sau!")
                        else:
                            st.warning("##### Vui lòng nhập đầy đủ thông tin!")
    
    def calendar_show_first_for_emlv(self,data_task_all,option_show_radio,action_on_board_calendar):
        # event
        if data_task_all is not None:
            if "employee_id" in st.session_state:
                data_task_all_show = data_task_all[data_task_all["employee_id"] == st.session_state.employee_id]
            if option_show_radio != "Theo nhân viên":
                data_tasks_renamed = data_task_all_show.rename(columns={
                    "start_date": "start",
                    "end_date": "end",
                    "color": "color",
                    "service_id": "resourceId",
                })
            else:
                data_tasks_renamed = data_task_all_show.rename(columns={
                    "start_date": "start",
                    "end_date": "end",
                    "color": "color",
                    "employee_id": "resourceId",
                })
            for col in ["start", "end"]:
                data_tasks_renamed[col] = pd.to_datetime(
                    data_tasks_renamed[col], format="%d/%m/%Y", dayfirst=True
                ).dt.strftime("%Y-%m-%d")

            data_tasks_renamed= data_tasks_renamed[["id", "title", "start", "end", "color", "resourceId"]]
            events = data_tasks_renamed.to_dict('records')
            # service resource
            resource_service = self.service_load_not_parent.rename(columns={
                "ma_dv_id66": "id",
                "ten_dv": "title",
            })
            resource_service = resource_service[["id", "title"]]
            resource_service = resource_service.to_dict("records")
            
            # employee resource
            resource_employee = self.employee_array.drop(columns=["id"])
            resource_employee = resource_employee.rename(columns={
                "ma_nv": "id",
                "ten_nv": "title",
            }).loc[:, ["id", "title"]]
            resource_employee = resource_employee.to_dict("records")
        else:
            events = []
            resource_service = ''
            resource_employee = ''
        
        calendar_options = {
            "editable": "true",
            "navLinks": "true",
            "resources": resource_service,
            "selectable": "true",
        }
        if option_show_radio == "Dạng ngày":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridDay,dayGridWeek,dayGridMonth",
                },
                "initialDate": self.time_now_init,
                "initialView": "dayGridMonth",
            }
        elif option_show_radio == "Dạng danh sách":
            calendar_options = {
                **calendar_options,
                "initialDate": self.time_now_init,
                "initialView": "listWeek",
                "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "listWeek",
            }}
        elif option_show_radio == "Theo dịch vụ":
            calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "prev,next",
                "center": "title",
                "right": "resourceTimelineMonth",
            },
            "initialDate": self.time_now_init,
            "initialView": "resourceTimelineMonth",
            "resourceGroupField": "title",
        }
        elif option_show_radio == "Theo nhân viên":
            calendar_options = {
            "editable": "true",
            "navLinks": "true",
            "selectable": "true",
            "headerToolbar": {
                "left": "prev,next",
                "center": "title",
                "right": "resourceTimelineMonth",
            },
            "initialDate": self.time_now_init,
            "initialView": "resourceTimelineMonth",
            "resources": resource_employee,
            "resourceGroupField": "title",
        }
        if not st.session_state.get("events", False):
            st.session_state["events"] = str(uuid.uuid4())  
        state = calendar(
            events=events,
            options=calendar_options,
            callbacks = ["viewSkeletonRender","dateClick","eventClick","eventsSet"],
            custom_css="""
            .fc-event-past {
                opacity: 0.8;
            }
            .fc-event-time {
                font-style: italic;
            }
            .fc-event-title {
                font-weight: 600;
                 color: rgb(0, 50, 73);
            }
            .fc-toolbar-title {
                font-size: 2rem;
            }
            """,
            key=str(st.session_state["events"]),
        )
        
        # callback 
        if state.get("dateClick"):
            date_click = state.get("dateClick")["date"]
            vietnam_time_click = TOOL_FOR_UI().handle_timezone_change(date_click)
            st.session_state.dialog_open_insert_tasks_2 = True
            self.add_new_task(data_service_all,vietnam_time_click)
        if state.get("eventClick"):
            task_id_updated = state.get("eventClick")["event"]["id"]
            st.write(task_id_updated)
            st.session_state.dialog_open_update_tasks = True
            module_todo.update_task(data_service_all,data_task_all,task_id_updated,action_on_board_calendar)
        if state.get("eventsSet") is not None:
            st.session_state["events"] = state["eventsSet"]
            
    def dashboard_todocheck(self,options_show_radio):
        # part init
        tool_for_ui = TOOL_FOR_UI()
        if not data_task_all.empty:
            data_tasks_show = data_task_all
            data_tasks_show["ten_dv"] = data_tasks_show["service_id"].map(
                dichvu_after_load.set_index("ma_dv_id66")["ten_dv"]
            )
            data_tasks_show["ten_nv"] = data_tasks_show["employee_id"].map(
                nhanvien_after_load.set_index("ma_nv")["ten_nv"]
            )
                    # if search_term:
            #     data_tasks_show = data_tasks_show[data_tasks_show["title"].str.contains(search_term, case=False)]
            data_tasks_show["start_date"] = pd.to_datetime(data_tasks_show["start_date"]).dt.strftime("%d/%m/%Y")
            data_tasks_show["end_date"] = pd.to_datetime(data_tasks_show["end_date"]).dt.strftime("%d/%m/%Y")
            data_tasks_show["time"] = data_tasks_show["start_date"] + " - " + data_tasks_show["end_date"]
            data_tasks_show = data_tasks_show[["title", "ten_dv", "ten_nv","employee_id", "status", "time", "revenue", "notes"]]
        else:
            data_tasks_show = pd.DataFrame(columns=["title", "ten_dv", "ten_nv", "employee_id", "status", "start_date", "end_date", "revenue", "notes"])

        
        container_main_task_dashboard = st.container(key="container_main_task_dashboard")
        with container_main_task_dashboard:
            calendar_first_cols = st.columns([3,1])
            with calendar_first_cols[1]:
                action_on_board_calendar = st.selectbox("Hành động với sự kiện được chọn:",["Sửa","Xóa"], key="action_on_board_calendar")
                tool_for_ui.render_task_view("employee_lv")
            with calendar_first_cols[0]:
                set_even_set = self.calendar_show_first_for_emlv(data_task_all if not data_task_all.empty else None,options_show_radio,action_on_board_calendar)
            

        container_table_second_task_main = st.container(key="container_table_second_task_main")
        with container_table_second_task_main:
            cols_filter_second_main_task = st.columns([2,1,1])
            cols_filter_second_main_task[0].markdown("""
                <h5 style='text-align: center; font-size: 1.7rem;padding:5px; font-weight: bold;border-bottom:2px solid blue;margin-bottom:5px;margin-top:20px'>Bảng liệt kê</h5>
                        
                        """, unsafe_allow_html=True)
            
            dich_vu_options = [""] + list(self.service_load_not_parent["ten_dv"].unique())
            nhan_vien_options = [""] + list(self.employee_array["ten_nv"].unique())

            # Tạo selectbox
            selected_dich_vu = cols_filter_second_main_task[1].selectbox("Dịch vụ", dich_vu_options)
            search_term_title_person = cols_filter_second_main_task[2].text_input("Tiêu đề",placeholder="Nhập tiêu đề", key="search_term_title_person")
            data_tasks_show = data_tasks_show[data_tasks_show["employee_id"] == st.session_state.employee_id]
            if selected_dich_vu:
                data_tasks_show = data_tasks_show[data_tasks_show["ten_dv"] == selected_dich_vu]
            if search_term_title_person:
                data_tasks_show = data_tasks_show[data_tasks_show["title"].str.contains(search_term_title_person, case=False)]
            st.dataframe(data_tasks_show,use_container_width=True,column_config={
                "title":"Tiêu đề",
                "ten_dv":"Dịch vụ",
                "ten_nv":"Nhân viên",
                "status":"Trạng thái",
                "time":"Thời gian",
                "revenue":"Doanh thu",
                "notes":"Ghi chú",
            },hide_index=True)

    def line_check_dashboard(self):
        container_first_main_line_level = st.container(key="container_first_main_line_level")
        with container_first_main_line_level:
            cols_first_main = st.columns([4,1.5,1.5,1.5,2])
            human_presentation_relative = module_config.measure_test_time_load_api("../src/for_style/human_3_present.png")
            human_presentation_relative = "data:image/png;base64," + human_presentation_relative if not human_presentation_relative.startswith(module_config.CDN_START_STR) else human_presentation_relative
            with cols_first_main[4]:
                    selected_year = st.selectbox("❄️", self.year_select, index=list(self.year_select).index(self.year_select.max()),key="selected_year_line_level")
                    selected_month = st.selectbox("❄️", self.month_key_show,index=self.month_now_index, key="selected_month_line_level")
                    selected_month = self.month_select[selected_month]
                    
                    selected_loaidoanhthu = st.selectbox("❄️", ["Phát triển mới","Hiện hữu"],placeholder="Loại doanh thu",key="loaidoanhthu_slb_linlevel")
            with cols_first_main[0]:
                ctn_first_main_title = st.container(key="ctn_first_main_title")
                ctn_first_main_title.markdown(f"""
                    <div style="text-align: left;">
                        <div style="display: inline-flex; justify-content: space-between;gap: 10px;">
                        <img src="{human_presentation_relative}" style="width: 35%; height: auto;">
                        <h4 style="font-weight: bold;font-size:2rem;text-align:left;">❄️Bảng trình bày công việc</h4>
                        </div>
                        <p style="font-size: 1rem;font-weight:bold">Theo dõi tình hình công việc, dịch vụ và nhân viên</p>
                    </div>                    
                                        """,unsafe_allow_html=True)
            # data show metric
            Data_show_metric = data_task_all[(data_task_all["start_date"].dt.year == selected_year) & (data_task_all["start_date"].dt.month == selected_month)]
            with cols_first_main[1]:
                ctn_first_main_metric_01 = st.container(key="ctn_first_main_metric_01")
                ctn_first_main_metric_01.metric("Hoàn thành",
                                                Data_show_metric["status"].value_counts()["Đã hoàn thành"] if "Đã hoàn thành" in Data_show_metric["status"].value_counts() else 0
                                                )
                ctn_first_main_metric_01.caption("Tổng Số hoàn thành")
            with cols_first_main[2]:
                ctn_first_main_metric_02 = st.container(key="ctn_first_main_metric_02")
                ctn_first_main_metric_02.metric("Chưa hoàn thành",
                                                Data_show_metric["status"].value_counts()["Chưa hoàn thành"] if "Chưa hoàn thành" in Data_show_metric["status"].value_counts() else 0)
                ctn_first_main_metric_02.caption("Số chưa hoàn thành")
            with cols_first_main[3]:
                ctn_first_main_metric_03 = st.container(key="ctn_first_main_metric_03")
                ctn_first_main_metric_03.metric("Chờ",
                                                Data_show_metric["status"].value_counts()["Chờ"] if "Chờ" in Data_show_metric["status"].value_counts() else 0)
                ctn_first_main_metric_03.caption("Tổng Số chờ")

        container_second_main_line_level = st.container(key="container_second_main_line_level")
        with container_second_main_line_level: 
            container_title_chart_second = st.container(key="container_title_chart_second")
            cols_second_main_line_level = container_title_chart_second.columns([0.35,1,1.25])
            with cols_second_main_line_level[0]:
                
                radio_nhanvien_select = st.radio("Chọn nhân viên",[None] +  self.selected_em_key,
                                                 format_func=lambda x: self.em_select[x].split(" ")[-1] if x and x != None else "Tất cả", key="radio_nhanvien_select",on_change=TOOL_FOR_UI().update_ui_calendar)
            with cols_second_main_line_level[1]:
                st.markdown("""
                        <h5 style="text-align:center;font-size:1rem;font-weight: bolder;">Tỉ lệ hoàn thành doanh thu (%)</h5>
                                                    
                                                    """,unsafe_allow_html=True)
                pie_chart,df_detail,sum_plan_revenue, sum_make_revenue= module_todo.list_task_complete_chart(kehoach_after_load,nhanvien_after_load,dichvu_after_load,data_task_all,selected_year,selected_month,selected_loaidoanhthu,radio_nhanvien_select)
                employrr = st.altair_chart(pie_chart,key="Pie_chart_linlevel")
                ctn_metric_second_main_line_level = st.container(key="ctn_metric_second_main_line_level")
                cols_ctn_second_main_line_level = ctn_metric_second_main_line_level.columns([1,1])
                cols_ctn_second_main_line_level[0].metric("Tổng doanh thu kế hoạch",module_view.format_number(sum_plan_revenue))
                cols_ctn_second_main_line_level[1].metric("Tổng doanh thu thực hiện",module_view.format_number(sum_make_revenue))
            with cols_second_main_line_level[2]:
                st.markdown("""
                        <h5 style="text-align:center;font-size:1rem;font-weight: bolder;">Tỉ lệ hoàn thành theo dịch vụ (%)</h5>
                                                    """,unsafe_allow_html=True)
                df_service_show = module_todo.table_service_process_bar_task(df_detail,radio_nhanvien_select)
        container_thirst_main_line_level = st.container(key="container_thirst_main_line_level")
        with container_thirst_main_line_level:
            data_filter_for_thirst_table = data_task_all.copy()
            if radio_nhanvien_select is None:
                data_filter_for_thirst_table = data_filter_for_thirst_table[(data_filter_for_thirst_table["start_date"].dt.year == selected_year) 
                                                                        & (data_filter_for_thirst_table["start_date"].dt.month == selected_month)]
            else: 
                data_filter_for_thirst_table = data_filter_for_thirst_table[(data_filter_for_thirst_table["start_date"].dt.year == selected_year) &
                                                                        (data_filter_for_thirst_table["start_date"].dt.month == selected_month) &
                                                                        (data_filter_for_thirst_table["employee_id"] == radio_nhanvien_select)]
            data_filter_for_thirst_table.reset_index(drop=True)
            data_filter_for_thirst_table["id"] = data_filter_for_thirst_table.index + 1
            data_filter_for_thirst_table["id"] = data_filter_for_thirst_table["id"].astype(int)
            data_filter_for_thirst_table["name_service"] = data_filter_for_thirst_table["service_id"].map(dichvu_after_load.set_index("ma_dv_id66")["ten_dv"])
            data_filter_for_thirst_table["name_employee"] = data_filter_for_thirst_table["employee_id"].map(nhanvien_after_load.set_index("ma_nv")["ten_nv"])
            data_filter_for_thirst_table["start_date"] = data_filter_for_thirst_table["start_date"].astype(str)
            data_filter_for_thirst_table["end_date"] = data_filter_for_thirst_table["end_date"].astype(str)
            data_filter_for_thirst_table["revenue"] = data_filter_for_thirst_table["revenue"].astype(float).apply(lambda x: module_view.format_number(x))
            data_filter_for_thirst_table=data_filter_for_thirst_table[["id","title","name_service","name_employee","status","start_date","end_date","revenue","notes"]]
            data_filter_for_thirst_table["status"] = data_filter_for_thirst_table["status"].map({"Chưa hoàn thành": "❌ Chưa hoàn thành", "Đã hoàn thành": "✔️ Đã hoàn thành", "Chờ": "⏳ Chờ"})
            with elements("data_ctn_thirst_main_linelv"):
                selected = mui.DataGrid(
                rows=data_filter_for_thirst_table.to_dict(orient="records"),
                disableRowSelectionOnClick=True,
                columns=[
                    {"field": "title", "headerName": "Tiêu đề", "width": 100,"color":"red"},
                    {"field": "name_service", "headerName": "Dịch vụ", "width": 200},
                    {"field": "name_employee", "headerName": "Nhân viên", "width": 200},
                    {"field": "status", "headerName": "Trạng thái", "width": 150},
                    {"field": "start_date", "headerName": "Ngày bắt đầu", "width": 100},
                    {"field": "end_date", "headerName": "Ngày kết thúc", "width": 100},
                    {"field": "revenue", "headerName": "Doanh thu", "width": 100},
                ],
                pageSize=5,
                style={"height": 400, "width": "100%", "borderRadius": 15, "overflow": "hidden"},
                cellSelection=True,
                disableColumnFilter=False,
                sx={
                "& .MuiDataGrid-columnHeaders": {  # Lớp CSS cho phần header
                    "backgroundColor": "#00a6a6",     # Màu nền
                    "color": "white",              # Màu chữ            # Kích thước chữ
                    "fontWeight": "bold",          # Chữ in đậm
                },
            },
            )
            container_thirst_main_sub_line_level = container_thirst_main_line_level.container(key="container_thirst_main_sub_line_level")
            cols_thirst_main_line_level = container_thirst_main_sub_line_level.columns([1,1,1])
            cols_thirst_main_line_level[0].metric("Tổng số hoàn thành",data_filter_for_thirst_table["status"].value_counts()["✔️ Đã hoàn thành"] if "✔️ Đã hoàn thành" in data_filter_for_thirst_table["status"].value_counts() else 0)
            cols_thirst_main_line_level[1].metric("Tổng số chưa hoàn thành",data_filter_for_thirst_table["status"].value_counts()["❌ Chưa hoàn thành"] if "❌ Chưa hoàn thành" in data_filter_for_thirst_table["status"].value_counts() else 0)
            cols_thirst_main_line_level[2].metric("Tổng số chờ",data_filter_for_thirst_table["status"].value_counts()["⏳ Chờ"] if "⏳ Chờ" in data_filter_for_thirst_table["status"].value_counts() else 0)
        container_four_main_line_level = st.container(key="container_four_main_line_level")
        with container_four_main_line_level:
            cols_show_radio_four_main = st.columns([2,1,1])
            option_show_radio_four_main = cols_show_radio_four_main[1].selectbox("Chọn chế độ xem",["Dạng ngày","Dạng danh sách","Theo dịch vụ","Theo nhân viên"], key="option_show_radio_four_main",
                                                       on_change=TOOL_FOR_UI().update_ui_calendar)
            array_em_four = self.employee_array[["ma_nv", "ten_nv"]].drop_duplicates()
            array_ser_four = self.service_load_not_parent[["ma_dv_id66", "ten_dv"]].drop_duplicates()

            # Tạo dictionary ánh xạ mã -> tên
            employee_dict_fourfour = {row["ma_nv"]: row["ten_nv"] for _, row in array_em_four.iterrows()}
            service_dict_four = {row["ma_dv_id66"]: row["ten_dv"] for _, row in array_ser_four.iterrows()}

            # Thêm option rỗng vào danh sách (nếu cần)
            employee_keys = [""] + list(employee_dict_fourfour.keys())
            service_keys = [""] + list(service_dict_four.keys())

            selected_show_service_calendar_four_main = cols_show_radio_four_main[2].selectbox(
                "Chọn dịch vụ",
                options=service_keys,
                placeholder="Chọn dịch vụ",
                format_func=lambda x: service_dict_four[x] if x else "",  # Hiển thị tên hoặc để trống
                key="selected_show_service_calendar_four_main",
                on_change=TOOL_FOR_UI().update_ui_calendar,
            )
            cols_show_radio_four_main[0].subheader("Lịch công việc",divider=True)
            cols_calendar_four_body = st.columns([4,1])
                        
            with cols_calendar_four_body[0]:
                self.calendar_show_line_lv_dash(data_task_all,option_show_radio_four_main,radio_nhanvien_select,selected_show_service_calendar_four_main)
            with cols_calendar_four_body[1]:
                TOOL_FOR_UI().render_task_view("line_lv")
                

class MAIN_TODO():
    def __init__(self):
        self.fronend_class = TODOCHECK_UI_DESIGN()
    def sidebar_todocheck(self):
        with st.sidebar:
            module_config.show_expander_sidebar()
            selected = option_menu(
                    menu_title= None,  # required
                    options=["Dashboard", "Công việc của tôi"],  # required
                    icons=["clipboard-data", "calendar2-check"],  
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
    def hearder_todocheck(self, text):
        container_header_todocheck = st.container(key="container_header_todocheck")
        with container_header_todocheck:
            todocols = st.columns([13,2])
            with todocols[0]:
                container_cols_search = st.container(key="container_cols_search")
                cols_search = container_cols_search.columns([5,3]) 
                cols_search[0].header(text,divider=True)                  
                option_show_radio_dashboard = cols_search[1].selectbox(" ",["Dạng ngày","Dạng danh sách","Theo dịch vụ","Theo nhân viên"],
                                on_change=TOOL_FOR_UI().update_ui_calendar
                                , key="option_show_radio_calendar_first")
            with todocols[1]:
                container_second_task = st.container(key="container_second_task") 
                new_button_task = container_second_task.button("Thêm",icon=":material/add_task:",use_container_width=True, key="new_button_task")
                if new_button_task:
                    st.session_state.dialog_open_insert_tasks = True
                    module_todo.add_new_task_2(data_service_all)
        return option_show_radio_dashboard
    def main(self):
        selected = self.sidebar_todocheck()
        if selected == "Dashboard":
            if not data_task_all.empty:
                self.fronend_class.line_check_dashboard()  
            else:
                st.warning("##### Không có dữ liệu công việc!")
        elif selected == "Công việc của tôi":
            option_show_radio_dashboard = self.hearder_todocheck("Công việc của tôi")
            self.fronend_class.dashboard_todocheck(option_show_radio_dashboard)
            
thuchien_after_load, kehoach_after_load, nhanvien_after_load, dichvu_after_load,line_after_load = module_view.load_data() 
data_task_all = pd.DataFrame(module_todo.load_tasks())
data_service_all =module_insert.load_data_service()               
MAIN_TODO().main()
module_config.add_sidebar_footer()



