import streamlit as st
import pandas as pd
import PROJECTS.config as module_config
import plotly.express as px
import altair as alt
import speech_recognition as sr
import tempfile
import datetime

def convert_audio_to_file(audio_file):
    if audio_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(audio_file.read())
            temp_file_path = temp_file.name
        return temp_file_path
    else:
        return None

def audio_to_text(session_state,output_session):
    """Convert audio to text using SpeechRecognition."""

    file_path = st.session_state[f"{session_state}"]
    recognizer = sr.Recognizer()
    file_path = convert_audio_to_file(file_path)
    if file_path is not None:
        try:
            with sr.AudioFile(file_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language="vi-VN")
                st.session_state[f"{output_session}"] = text if text is not None else " "
        except sr.UnknownValueError:
            return "Không thể nhận diện âm thanh."
        except sr.RequestError as e:
            return f"Lỗi kết nối: {e}"
        
def get_explain_by_user_from_database():
    line = st.session_state.line_access
    employee = st.session_state.employee_id
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    try:
        conn = module_config.connect_to_mysql()
        cursor = conn.cursor()
        cursor.execute(f"SELECT content FROM explaination WHERE line = '{line}' AND employee = '{employee}' AND month = '{month}' AND year = '{year}'")
        data = cursor.fetchall()
        if len(data) > 0:
            data = pd.DataFrame(data,columns=["content"])
            return data["content"][0]
        else:
            return None
    except Exception as e:
        return None
    finally:
        cursor.close()
        conn.close()
def query_explain_by_user_from_database():
    line = st.session_state.line_access
    employee = st.session_state.employee_id
    try:
        conn = module_config.connect_to_mysql()
        cursor = conn.cursor()
        if st.session_state.type_process != 'LDPVNPT':
            cursor.execute(f"SELECT id,line,employee,content,month,year,created_at FROM explaination WHERE line = '{line}' AND employee = '{employee}'")
        else:
            cursor.execute(f"SELECT id,line,employee,content,month,year,created_at FROM explaination ORDER BY line ASC")
        data = cursor.fetchall()
        if len(data) > 0:
            data = pd.DataFrame(data,columns=["id","line","employee","content","month","year","created_at"])
            return data
        else:
            return None
    except Exception as e:
        return None
    finally:
        cursor.close()
        conn.close()        
def insert_explain_to_database(content):
    if content == "":
        st.toast("##### Vui lòng nhập nội dung giải trình",icon=":material/error:")
    else:
        check_duplicate = query_explain_by_user_from_database()
        if check_duplicate is not None:
            st.toast("##### Bạn đã thêm giải trình cho tháng này",icon=":material/error:")
        else:
            line = st.session_state.line_access
            employee = st.session_state.employee_id
            month = datetime.datetime.now().month
            year = datetime.datetime.now().year
            created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Kiểm tra điều kiện thêm giải trình
            current_day = datetime.datetime.now().day
            last_day_of_month = (datetime.datetime.now().replace(day=28) + datetime.timedelta(days=4)).day
            if current_day < last_day_of_month - 4:
                st.toast("##### Bạn không thể thêm giải trình sau ngày 4 của tháng",icon=":material/error:")
            else:
                try:
                    conn = module_config.connect_to_mysql()
                    cursor = conn.cursor()
                    cursor.execute(f"INSERT INTO explaination (line,employee,content,month,year,created_at) VALUES ('{line}','{employee}','{content}','{month}','{year}','{created_at}')")
                    conn.commit()
                    st.toast("##### Thêm giải trình thành công",icon=":material/check_circle:")
                except Exception as e:
                    st.toast("##### Thêm giải trình thất bại",icon=":material/error:")
                finally:
                    cursor.close()
                    conn.close()
        
def edit_explain_to_database(content):
    if content == "":
        st.toast("##### Vui lòng nhập nội dung giải trình",icon=":material/error:")
    else:
        line = st.session_state.line_access
        employee = st.session_state.employee_id
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        
        current_day = datetime.datetime.now().day
        last_day_of_month = (datetime.datetime.now().replace(day=28) + datetime.timedelta(days=4)).day
        if current_day < last_day_of_month - 4:
            st.toast("##### Bạn không thể sửa giải trình sau ngày 4 của tháng",icon=":material/error:")
        else:
            try:
                conn = module_config.connect_to_mysql()
                cursor = conn.cursor()
                cursor.execute(f"UPDATE explaination SET content = '{content}' WHERE line = '{line}' AND employee = '{employee}' AND month = '{month}' AND year = '{year}'")
                conn.commit()
                st.toast("##### Sửa giải trình thành công",icon=":material/check_circle:")
            except Exception as e:
                st.toast("##### Sửa giải trình thất bại",icon=":material/error:")
            finally:
                cursor.close()
                conn.close()
def delete_explain_from_database(id_explain):
    line = st.session_state.line_access
    employee = st.session_state.employee_id
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    
    current_day = datetime.datetime.now().day
    last_day_of_month = (datetime.datetime.now().replace(day=28) + datetime.timedelta(days=4)).day
    if current_day < last_day_of_month - 4:
        return False
    else:
        try:
            conn = module_config.connect_to_mysql()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM explaination WHERE id = {id_explain} AND line = '{line}' AND employee = '{employee}' AND month = '{month}' AND year = '{year}'")
            conn.commit()
            return True
        except Exception as e:
            return False
        finally:
            cursor.close()
            conn.close()
    




def data_layer_set(data_task_all,thuchien_after_load,kehoach_after_load,nhanvien_after_load,year_selected,month_selected,loaidoanhthu_selected,nhanvien_selected):
    data_task_show = data_task_all[(data_task_all["line"]==st.session_state.line_access) &
                                  (data_task_all["start_date"].dt.year==year_selected) &
                                  (data_task_all["start_date"].dt.month==month_selected) &
                                  (data_task_all["loaidoanhthu"]==loaidoanhthu_selected)]
    thuchien_show = thuchien_after_load[(thuchien_after_load["year_insert"]==year_selected) &
                                        (thuchien_after_load["thang"]==month_selected)]
    kehoach_show = kehoach_after_load[(kehoach_after_load["year_insert"]==year_selected) &
                                        (kehoach_after_load[f"t{month_selected}"]==month_selected)]
    nhanvien_show = nhanvien_after_load[nhanvien_after_load["line_nv"]==st.session_state.line_access]
    if nhanvien_selected != "": 
        data_task_show = data_task_show[data_task_show["employee_id"]==nhanvien_selected]
        thuchien_show = thuchien_show[thuchien_show["IDnhanvien"]==nhanvien_selected]
        kehoach_show = kehoach_show[kehoach_show["ma_nv"]==nhanvien_selected]
        nhanvien_show = nhanvien_show[nhanvien_show["ma_nv"]==nhanvien_selected]
    data_task_show["name_employee"] = data_task_show["employee_id"].map(nhanvien_show.set_index("ma_nv")["ten_nv"])
    return data_task_show,thuchien_show,kehoach_show,nhanvien_show

def Column_chart_fisrt_ctn(data_task_show,thuchien_show):
    if not data_task_show.empty and not thuchien_show.empty:
        thuchien_load = thuchien_show[["IDnhanvien", "doanhthu", "nhom_dv"]].rename(
            columns={"IDnhanvien": "employee", "doanhthu": "revenue", "nhom_dv": "service"}
        )
        thuchien_load_sum = thuchien_load.groupby(["employee"]).sum().reset_index()

        data_task_show = data_task_show[["employee_id", "service_id", "revenue","name_employee"]].rename(
            columns={"employee_id": "employee", "service_id": "service"}
        )
        data_task_show_sum = data_task_show.groupby(["employee","name_employee"]).sum().reset_index()

        merge_data = pd.merge(thuchien_load_sum, data_task_show_sum, how="outer", on=["employee"])
        merge_data = merge_data.fillna(0)
        merge_data['revenue_x'] = merge_data['revenue_x'].astype(float)
        merge_data['revenue_y'] = merge_data['revenue_y'].astype(float)

        selection = alt.selection_point(fields=['employee'], empty="none")
        
        if not merge_data.empty:
            merge_data = merge_data.rename(
                columns={"revenue_x": "Kế toán", "revenue_y": "Thực nhập"}
            )
            
            merge_data["Kế toán"] = merge_data["Kế toán"] / 1000000
            merge_data["Thực nhập"] = merge_data["Thực nhập"] / 1000000
            merge_data["name_employee"] = merge_data["name_employee"].apply(lambda x: x.split(" ")[-1])
            melted_data = merge_data.melt(
                id_vars=["employee", "name_employee"],
                value_vars=["Kế toán", "Thực nhập"],
                var_name="Loại doanh thu",
                value_name="Doanh thu"
            )
            
            chart = alt.Chart(melted_data).mark_bar().encode(
                x=alt.X("name_employee:N", title="Nhân viên", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Doanh thu:Q", title="Doanh thu"),
                color=alt.Color("Loại doanh thu:N", legend=alt.Legend(title="Loại doanh thu")),
                xOffset="Loại doanh thu:N",
                tooltip=["name_employee", "Loại doanh thu", "Doanh thu"]
            ).properties(
                title="So sánh Kế toán và thực nhập (triệu đồng)",
                height=250
            ).add_params(selection)
            
            return chart,merge_data
    else:
        return None,None
        
def Donut_chart_explain(data_filter,selection_emId):
    if data_filter is not None:
        if selection_emId["selection"]["param_1"]:
            data_filter = data_filter[data_filter["employee"] == selection_emId["selection"]["param_1"][0]["employee"]]
            
            
        total_thuc_nhap = data_filter["Thực nhập"].sum()
        total_ke_toan = data_filter["Kế toán"].sum()
        
        ratio_thuc_nhap = float(total_thuc_nhap) / float(total_ke_toan) if total_ke_toan != 0 else 0

        data_ratio = pd.DataFrame({
            "Loại": ["Thực nhập", "Phần còn lại"],
            "Tỷ lệ": [ratio_thuc_nhap, 1 - ratio_thuc_nhap]
        })
        donut_chart = alt.Chart(data_ratio).mark_arc(innerRadius=25).encode(
            theta=alt.Theta(field="Tỷ lệ", type="quantitative", title="Tỷ lệ"),
            color=alt.Color(field="Loại", type="nominal", title="Loại doanh thu"),
            tooltip=["Loại", "Tỷ lệ"]
        ).properties(
            title="Tỷ lệ Thực nhập so với Kế toán",
            height=250
        )

        text_labels = alt.Chart(data_ratio).mark_text(size=12, color="white").encode(
            text=alt.Text("Tỷ lệ:Q", format=".1%"),  
            theta=alt.Theta("Tỷ lệ:Q", stack=True),
            radius=alt.value(60),  
            color=alt.value("white")  
        )

        final_chart = donut_chart + text_labels
        return final_chart
    else:
        return None
def Table_service_filter(data_task_show,nhanvien_after_load,dichvu_after_load,thuchien_show,selection):
    if not data_task_show.empty:
        thuchien_load = thuchien_show[["IDnhanvien", "doanhthu", "nhom_dv"]].rename(
                columns={"IDnhanvien": "employee", "doanhthu": "revenue_th", "nhom_dv": "service"}
            )
        
        data_task_show = data_task_show[["employee_id", "service_id", "revenue"]].rename(
                columns={"employee_id": "employee", "service_id": "service"}
            )
        if selection["selection"]["param_1"] != {}:
            data_task_show = data_task_show[data_task_show["employee"]==selection["selection"]["param_1"][0]["employee"]]
            thuchien_load = thuchien_load[thuchien_load["employee"]==selection["selection"]["param_1"][0]["employee"]]
        
        compare_data = pd.merge(thuchien_load, data_task_show, how="outer", on=["employee", "service"])
        compare_data = compare_data.fillna(0)
        compare_data = compare_data.groupby(["employee", "service"]).agg(
            {
                'revenue_th': 'sum',
                'revenue': 'sum'
            }
        )
        
        compare_data['revenue_th'] = compare_data['revenue_th'].astype(float)
        compare_data['revenue'] = compare_data['revenue'].astype(float)
        compare_data["rate"] = compare_data["revenue_th"] / compare_data["revenue"]
        compare_data["subtract"] = compare_data["revenue_th"] - compare_data["revenue"]
        compare_data = compare_data.reset_index()
        
        compare_data["employee"] = compare_data["employee"].map(nhanvien_after_load.set_index("ma_nv")["ten_nv"])
        compare_data["employee"] = compare_data["employee"].apply(lambda x: x.split(" ")[-1])
        compare_data["service"] = compare_data["service"].map(dichvu_after_load.set_index("ma_dv_id66")["ten_dv"])
        
        return compare_data