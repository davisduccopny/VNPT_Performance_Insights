import streamlit as st
import numpy as np
import pandas as pd
import mysql.connector
from mysql.connector import pooling, Error
from mysql.connector import OperationalError, InternalError
import EM_MODULE.config as module_config
import plotly.express as px
import datetime
import time
import uuid
import altair as alt
from EM_MODULE.module_view import format_number

@st.cache_data
def load_tasks():
    conn = module_config.connect_to_mysql()
    try:
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            select_query = "SELECT * FROM tasks WHERE line = %s"
            cursor.execute(select_query, (st.session_state.line_access,))
            tasks = cursor.fetchall()
            return tasks
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
def insert_data_todocheck(title, service_id, employee_id, status, start_date, end_date, revenue, notes, color, created_at,loaidoanhthu):
    conn = module_config.connect_to_mysql()
    try:
        if conn.is_connected():
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO tasks (title, service_id, employee_id, status, start_date, end_date, revenue, notes, color, created_at,loaidoanhthu,line)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
            """
            record = (title, service_id, employee_id, status, start_date, end_date, revenue, notes, color, created_at,loaidoanhthu, st.session_state.line_access)
            cursor.execute(insert_query, record)
            conn.commit()
            return True
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
def get_last_task_id():
    conn = module_config.connect_to_mysql()
    try:
        if conn.is_connected():
            cursor = conn.cursor()
            select_query = "SELECT MAX(id) as last_id FROM tasks WHERE line = %s"
            cursor.execute(select_query, (st.session_state.line_access,))
            result = cursor.fetchone()
            return result[0] if result else None
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
def update_task_in_db(task_id, title, service_id, employee_id, status, start_date, end_date, revenue, notes, color, updated_at,loaidoanhthu):
    conn = module_config.connect_to_mysql()
    try:
        if conn.is_connected():
            cursor = conn.cursor()
            update_query = """
                UPDATE tasks
                SET title = %s, service_id = %s, employee_id = %s, status = %s, start_date = %s, end_date = %s, revenue = %s, notes = %s, color = %s, updated_at = %s,loaidoanhthu = %s
                WHERE id = %s
            """
            record = (title, service_id, employee_id, status, start_date, end_date, revenue, notes, color, updated_at,loaidoanhthu, task_id)
            cursor.execute(update_query, record)
            conn.commit()
            return True
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def delete_task_in_db(task_id):
    conn = module_config.connect_to_mysql()
    try:
        if conn.is_connected():
            cursor = conn.cursor()
            delete_query = "DELETE FROM tasks WHERE id = %s"
            cursor.execute(delete_query, (task_id,))
            conn.commit()
            return True
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close() 
 
            
@st.dialog("Thêm công việc mới!")
def add_new_task_2(data_service):
    data_service = data_service[data_service["danh_muc_tt"].notna()]
    data_service = data_service[~data_service["danh_muc_tt"].isin(["1", "1.1.01", "1.1.02", "1.1.03", "1.1.05", "1.1.06", "1.1.07"])]
    if "dialog_open_insert_tasks" not in st.session_state:
        st.session_state.dialog_open_insert_tasks = False
    if "confirmation_insert_task_dialog" not in st.session_state:
        st.session_state.confirmation_insert_task_dialog = None   
    if st.session_state.dialog_open_insert_tasks:
        container_dialog_add_task = st.container(key="container_dialog_add_task")
        with container_dialog_add_task:                
            cols_dialog_add_task = st.columns([1,1])
            with cols_dialog_add_task[0]:
                title_task_insert = st.text_input("Tiêu đề", key="title_task_insert")
                service_task_insert = st.selectbox("Dịch vụ",data_service["ten_dv"].unique(), key="service_task_insert")
                id_service_task_selected = data_service[data_service["ten_dv"] == service_task_insert]["ma_dv_id66"].values[0]
                start_date_task_insert = st.date_input("Ngày bắt đầu",key="start_date_task_insert")
        
            with cols_dialog_add_task[1]:
                status_task_insert = st.selectbox("Trạng thái",["Chưa hoàn thành","Đã hoàn thành","Chờ"], key="status_task_insert")
                revenue_task_insert = st.number_input("Doanh thu", key="revenue_task_insert")
                end_date_task_insert = st.date_input("Ngày kết thúc", key="end_date_task_insert")
                loaidoanhthu_insert_task = st.selectbox("Loại doanh thu",["Hiện hữu","Phát triển mới"], key="loaidoanhthu_insert_task")
            notes_task_insert = st.text_area("Ghi chú", key="notes_task_insert")
            if status_task_insert == "Chưa hoàn thành":
                color_picker_insert_task = "#FF6C6C"
            elif status_task_insert == "Đã hoàn thành":
                color_picker_insert_task = "rgb(111 238 128)"
            else:
                color_picker_insert_task = "rgb(241 245 87)"
            cols_second_task_confirm = st.columns([1,1])
            button_insert_tasks = cols_second_task_confirm[0].button(
                    "Thêm",
                    key="button_add_task_confirm",
                    icon=":material/add_diamond:",
                    type="secondary",use_container_width=True
                    )
            button_cancel_tasks = cols_second_task_confirm[1].button("Hủy", key="button_cancel_task",icon=":material/close:",type="secondary",use_container_width=True)
            if button_cancel_tasks:
                st.session_state.confirmation_insert_task_dialog = "No"
                st.session_state.dialog_open_insert_tasks = False
                st.rerun()
            if button_insert_tasks:
                    if title_task_insert and service_task_insert and start_date_task_insert and status_task_insert and revenue_task_insert and end_date_task_insert:
                        if insert_data_todocheck(title_task_insert,id_service_task_selected,st.session_state.employee_id,status_task_insert,start_date_task_insert,end_date_task_insert,revenue_task_insert,notes_task_insert,color_picker_insert_task,datetime.datetime.now(),loaidoanhthu_insert_task):
                            st.success("##### Thêm công việc thành công!")
                            time.sleep(1)
                            st.session_state.confirmation_insert_task_dialog = "Yes"
                            st.session_state.dialog_open_insert_tasks = False
                            load_tasks.clear()
                            st.session_state["events"] = str(uuid.uuid4())
                            st.rerun()
                            
                        else:
                            st.warning("##### Có lỗi xảy ra, vui lòng thử lại sau!")
                    else:
                        st.warning("##### Vui lòng nhập đầy đủ thông tin!")

@st.dialog("Chỉnh sửa công việc!")
def update_task(data_service,data_tasks,task_id_update,action_on_board_calendar):
    array_status_update = ["Chưa hoàn thành","Đã hoàn thành","Chờ"]
    array_loaidoanhthu_update = ["Hiện hữu","Phát triển mới"]
    array_service_update = data_service["ten_dv"].unique()
    selected_task = data_tasks[data_tasks["id"] == int(task_id_update)]
    service_id = selected_task["service_id"].values[0]
    service_id_index = array_service_update.index(service_id) if service_id in array_service_update else 0
    status_update = selected_task["status"].values[0]
    status_index = array_status_update.index(status_update) if status_update in array_status_update else 0
    loaidoanhthu_update = selected_task["loaidoanhthu"].values[0]
    loaidoanhthu_index = array_loaidoanhthu_update.index(loaidoanhthu_update) if loaidoanhthu_update in array_loaidoanhthu_update else 0

    data_service = data_service[data_service["danh_muc_tt"].notna()]
    data_service = data_service[~data_service["danh_muc_tt"].isin(["1", "1.1.01", "1.1.02", "1.1.03", "1.1.05", "1.1.06", "1.1.07"])]
    if "dialog_open_update_tasks" not in st.session_state:
        st.session_state.dialog_open_update_tasks = False
    if st.session_state.dialog_open_update_tasks:
        if action_on_board_calendar == "Sửa":
            container_dialog_update_task = st.container(key="container_dialog_update_task")
            with container_dialog_update_task:                
                cols_dialog_update_task = st.columns([1,1])
                with cols_dialog_update_task[0]:
                    title_task_update = st.text_input("Tiêu đề",selected_task["title"].values[0], key="title_task_update")
                    service_task_update = st.selectbox("Dịch vụ",data_service["ten_dv"].unique(),index=service_id_index,key="service_task_update")
                    id_service_task_selected = data_service[data_service["ten_dv"] == service_task_update]["ma_dv_id66"].values[0]
                    start_date_task_update = st.date_input("Ngày bắt đầu",pd.to_datetime(selected_task["start_date"].values[0]).date(),key="start_date_task_update")
            
                with cols_dialog_update_task[1]:
                    status_task_update = st.selectbox("Trạng thái",array_status_update,status_index, key="status_task_update")
                    revenue_task_update = st.number_input("Doanh thu",float(selected_task["revenue"].values[0]), key="revenue_task_update")
                    end_date_task_update = st.date_input("Ngày kết thúc",pd.to_datetime(selected_task["end_date"].values[0]).date(), key="end_date_task_update")
                loaidoanhthu_update_task = st.selectbox("Loại doanh thu",array_loaidoanhthu_update,loaidoanhthu_index, key="loaidoanhthu_update_task")
                notes_task_update = st.text_area("Ghi chú",selected_task["notes"].values[0], key="notes_task_update")
                if status_task_update == "Chưa hoàn thành":
                    color_picker_update_task = "#FF6C6C"
                elif status_task_update == "Đã hoàn thành":
                    color_picker_update_task = "rgb(111 238 128)"
                else:
                    color_picker_update_task = "rgb(241 245 87)"
                cols_second_task_confirm = st.columns([1,1])
                button_update_tasks = cols_second_task_confirm[0].button(
                        "Cập nhật",
                        key="button_update_task_confirm",
                        icon=":material/add_diamond:",
                        type="secondary",use_container_width=True
                        )
                button_cancel_tasks = cols_second_task_confirm[1].button("Hủy", key="button_cancel_task",icon=":material/close:",type="secondary",use_container_width=True)
                if button_cancel_tasks:
                    st.session_state.dialog_open_update_tasks = False
                    st.session_state["events"] = str(uuid.uuid4())
                    st.rerun()
                if button_update_tasks:
                        if title_task_update and service_task_update and start_date_task_update and status_task_update and revenue_task_update and end_date_task_update:
                            if update_task_in_db(int(task_id_update),title_task_update,id_service_task_selected,st.session_state.employee_id,status_task_update,start_date_task_update,end_date_task_update,revenue_task_update,notes_task_update,color_picker_update_task,datetime.datetime.now(),loaidoanhthu_update_task):
                                st.success("##### Cập nhật công việc thành công!")
                                time.sleep(1)
                                st.session_state.dialog_open_update_tasks = False
                                load_tasks.clear()
                                st.session_state["events"] = str(uuid.uuid4())
                                st.rerun()
                            else:
                                st.warning("##### Có lỗi xảy ra, vui lòng thử lại sau!")
                        else:
                            st.warning("##### Vui lòng nhập đầy đủ thông tin!")
        else:
            st.write("##### Bạn có chắc chắn muốn xóa công việc này không?")
            cols_delete_task = st.columns([1,1])
            button_delete_task = cols_delete_task[0].button(
                    "Xóa",
                    key="button_delete_task_confirm",
                    icon=":material/delete_forever:",
                    type="secondary",use_container_width=True
                    )
            button_cancel_delete_task = cols_delete_task[1].button("Hủy", key="button_cancel_delete_task",icon=":material/close:",type="secondary",use_container_width=True)
            if button_delete_task:
                status_del = delete_task_in_db(int(task_id_update))
                if status_del:
                    st.success("##### Xóa công việc thành công!")
                    time.sleep(1)
                    st.session_state.dialog_open_update_tasks = False
                    load_tasks.clear()
                    st.session_state["events"] = str(uuid.uuid4())
                    st.rerun()
                else:
                    st.warning("##### Có lỗi xảy ra, vui lòng thử lại sau!")
            if button_cancel_delete_task:
                st.session_state.dialog_open_update_tasks = False
                st.session_state["events"] = str(uuid.uuid4())
                st.rerun()
                
@st.dialog("Chi tiết công việc!")
def view_task_linelv(data_service,data_tasks,task_id_update):
    array_status_viewlinelv = ["Chưa hoàn thành","Đã hoàn thành","Chờ"]
    array_loaidoanhthu_viewlinelv = ["Hiện hữu","Phát triển mới"]
    array_service_update = data_service["ten_dv"].unique()
    selected_task = data_tasks[data_tasks["id"] == int(task_id_update)]
    service_id = selected_task["service_id"].values[0]
    service_id_index = array_service_update.index(service_id) if service_id in array_service_update else 0
    status_update = selected_task["status"].values[0]
    status_index = array_status_viewlinelv.index(status_update) if status_update in array_status_viewlinelv else 0
    loaidoanhthu_update = selected_task["loaidoanhthu"].values[0]
    loaidoanhthu_index = array_loaidoanhthu_viewlinelv.index(loaidoanhthu_update) if loaidoanhthu_update in array_loaidoanhthu_viewlinelv else 0

    data_service = data_service[data_service["danh_muc_tt"].notna()]
    data_service = data_service[~data_service["danh_muc_tt"].isin(["1", "1.1.01", "1.1.02", "1.1.03", "1.1.05", "1.1.06", "1.1.07"])]
    if "view_task_detail_linelv_dialog" not in st.session_state:
        st.session_state.view_task_detail_linelv_dialog = False
    if st.session_state.view_task_detail_linelv_dialog:
        container_view_task_linelv = st.container(key="container_view_task_linelv")
        with container_view_task_linelv:                
            cols_dialog_update_task = st.columns([1,1])
            with cols_dialog_update_task[0]:
                title_task_view_detail_linelv = st.text_input("Tiêu đề",selected_task["title"].values[0], key="title_task_view_detail_linelv")
                service_task_view_linelv = st.selectbox("Dịch vụ",data_service["ten_dv"].unique(),index=service_id_index,key="service_task_view_linelv")
                start_date_task_viewlinelv = st.date_input("Ngày bắt đầu",pd.to_datetime(selected_task["start_date"].values[0]).date(),key="start_date_task_viewlinelv")
        
            with cols_dialog_update_task[1]:
                status_task_viewlinelv = st.selectbox("Trạng thái",array_status_viewlinelv,status_index, key="status_task_viewlinelv")
                revenue_task_viewlinelv = st.number_input("Doanh thu",float(selected_task["revenue"].values[0]), key="revenue_task_viewlinelv")
                end_date_task_viewlinelv = st.date_input("Ngày kết thúc",pd.to_datetime(selected_task["end_date"].values[0]).date(), key="end_date_task_viewlinelv")
            loaidoanhthu_viewlinelv_task = st.selectbox("Loại doanh thu",array_loaidoanhthu_viewlinelv,loaidoanhthu_index, key="loaidoanhthu_viewlinelv_task")
            notes_task_viewlinelv = st.text_area("Ghi chú",selected_task["notes"].values[0], key="notes_task_viewlinelv")
            button_cancel_tasks = st.button("Hủy", key="button_cancel_task",icon=":material/close:",type="secondary",use_container_width=True)
            if button_cancel_tasks:
                st.session_state.view_task_detail_linelv_dialog = False
                st.session_state["events_show_linelv"] = str(uuid.uuid4())
                st.rerun()
# PART FOR LINE LEVEL DASHBOARD 
def make_donut_todo(input_response, input_text):
    if input_response < 100:
        chart_color = ['#FF6F61', '#2EC4B6']

  # Đỏ cho chưa đạt
    else:
        chart_color = ['#2a9d8f', '#155F7A']
        
    source = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100-input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100, 0]
    })
        
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),
                        legend=None),
    ).properties(height=180)
        
    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=18, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            # domain=['A', 'B'],
                            domain=[input_text, ''],
                            range=chart_color),  # 31333F
                        legend=None),
    ).properties(height=180)
    return plot_bg + plot + text
def list_task_complete_chart(kehoach_after_load,nhanvien_after_load,dichvu_after_load,data_task_all, year_selected, month_selected,loaidoanhthu_selected,select_em_id):
    kehoach_after_load = kehoach_after_load[(kehoach_after_load["line"]== st.session_state.line_access) &
                                            (kehoach_after_load["year_insert"]== year_selected) &
                                            (kehoach_after_load["loaidoanhthu"]== loaidoanhthu_selected)]
    
    data_task_all = data_task_all[data_task_all["revenue"] > 0]
    data_task_all = data_task_all[(data_task_all["start_date"].dt.year == year_selected) &
                                  (data_task_all["start_date"].dt.month == month_selected) &
                                  (data_task_all["loaidoanhthu"] == loaidoanhthu_selected)]
    kehoach_after_load = kehoach_after_load[["id_dv_606",f"t{month_selected}","ma_nv"]].rename(columns={f"t{month_selected}":"planned_revenue", "id_dv_606":"service","ma_nv":"employee"})
    data_task_all = data_task_all[["service_id","revenue","employee_id"]].rename(columns={"service_id":"service","revenue":"actual_revenue","employee_id":"employee"})            
    df = pd.merge(kehoach_after_load, data_task_all, on=['employee', 'service'], how='left')
    df['actual_revenue'] = df['actual_revenue'].fillna(0)
    df_detail = df.copy()
    df_detail = df_detail.groupby(['employee', 'service']).agg({
        'actual_revenue': 'sum',
        'planned_revenue': 'sum'
        }).reset_index()
    df_detail['completion_percentage'] = df_detail.apply(
        lambda row: row['actual_revenue'] if row['planned_revenue'] == 0 else (float(row['actual_revenue']) / float(row['planned_revenue'])) * 100,
        axis=1
    ).astype(float)
    df_detail['color'] = df_detail['completion_percentage'].apply(lambda x: '#9CEC5B' if x >= 100 else ('#F0F465' if x >= 60 else '#fc4c4c'))
    df_detail["name_service"] = df_detail["service"].map(dichvu_after_load.set_index("ma_dv_id66")["ten_dv"])
    if select_em_id != None:
        df_employee = df.groupby('employee').agg({
        'actual_revenue': 'sum',
        'planned_revenue': 'sum'
        }).reset_index()
        df_employee = df_employee[df_employee["employee"] == select_em_id]
        if df_employee.empty:
            completion_rate_no_employee_selection = 0
            sum_plan_revenue = 0
            sum_make_revenue = 0
        else:
            df_employee['completion_percentage'] = (df_employee['actual_revenue'].astype(float) / df_employee['planned_revenue'].astype(float)) * 100
            df_employee['completion_percentage'] = df_employee['completion_percentage'].astype(float).round(2)
            completion_rate_no_employee_selection = df_employee['completion_percentage'].values[0]
            sum_plan_revenue = df_employee['planned_revenue'].astype(float).round(2).values[0]
            sum_make_revenue = df_employee['actual_revenue'].astype(float).round(2).values[0]
    else:
        completion_rate_no_employee_selection = (df["actual_revenue"].astype(float).sum() / df["planned_revenue"].astype(float).sum()) * 100
        completion_rate_no_employee_selection = completion_rate_no_employee_selection.astype(float).round(2)
        sum_plan_revenue = df["planned_revenue"].astype(float).sum().round(2)
        sum_make_revenue = df["actual_revenue"].astype(float).sum().round(2)

    Donut_chart = make_donut_todo(completion_rate_no_employee_selection, "Hoàn thành so với kế hoạch (%)")
    return Donut_chart,df_detail, sum_plan_revenue, sum_make_revenue

def table_service_process_bar_task(df_service, selection_id):
    if selection_id != "" and selection_id is not None:
        df_service = df_service[df_service["employee"] == selection_id]
        if df_service.empty:
            st.write("##### Không có dữ liệu!")
        else:
            df_service["actual_revenue"] = df_service["actual_revenue"].apply(format_number)
            df_service["planned_revenue"] = df_service["planned_revenue"].apply(format_number)
            df_service = df_service[["name_service","actual_revenue","planned_revenue","completion_percentage"]].rename(columns={"name_service":"Dịch vụ","actual_revenue":"Thực tế","planned_revenue":"Kế hoạch","completion_percentage":"Tỉ lệ(%)"})
            df_service["Tỉ lệ(%)"] = df_service["Tỉ lệ(%)"].apply(lambda x: f"{x:.2f}")
            
            df_service["Tỉ lệ(%)"] = df_service["Tỉ lệ(%)"].astype(float)
            df_service = df_service.reset_index(drop=True)
            st.dataframe(df_service, column_config={
                "Thực tế": {"format": "{:,.0f}"},
                "Kế hoạch": {"format": "{:,.0f}"},
                "Tỉ lệ(%)": st.column_config.ProgressColumn(
                "Tỉ lệ(%)",
                min_value=0,
                max_value=100,
                format="%d%%",
                width="medium"
                )
            },hide_index=True, height=300)
    else:
        df_service = df_service[["name_service","actual_revenue","planned_revenue"]]
        df_service = df_service.groupby('name_service').agg({
            'actual_revenue': 'sum',
            'planned_revenue': 'sum'
        }).reset_index()
        df_service['completion_percentage'] = df_service.apply(
            lambda row: row['actual_revenue'] if row['planned_revenue'] == 0 else (float(row['actual_revenue']) / float(row['planned_revenue'])) * 100,
            axis=1
        ).astype(float)
        df_service["actual_revenue"] = df_service["actual_revenue"].apply(format_number)
        df_service["planned_revenue"] = df_service["planned_revenue"].apply(format_number)
        df_service = df_service.rename(columns={"name_service":"Dịch vụ","actual_revenue":"Thực tế","planned_revenue":"Kế hoạch","completion_percentage":"Tỉ lệ(%)"})
        df_service["Tỉ lệ(%)"] = df_service["Tỉ lệ(%)"].apply(lambda x: f"{x:.2f}")
        df_service = df_service.reset_index(drop=True)
        st.dataframe(df_service, column_config={
            "Thực tế": {"format": "{:,.0f}"},
            "Kế hoạch": {"format": "{:,.0f}"},
            "Tỉ lệ(%)": st.column_config.ProgressColumn(
            "Tỉ lệ(%)",
            min_value=0,
            max_value=100,
            format="%d%%",
             width="medium"
            )
        },hide_index=True, height=300)
        
        