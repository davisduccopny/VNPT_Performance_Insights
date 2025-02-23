import streamlit as st
import pandas as pd
import os
import numpy as np
import EM_MODULE.config as module_config
import altair as alt
import plotly.express as px

def query_to_dataframe(query, conn):
    cursor = conn.cursor(dictionary=True)  
    cursor.execute(query)
    data = cursor.fetchall()  
    cursor.close()
    return pd.DataFrame(data)

@st.cache_data
def load_data():
    conn = module_config.connect_to_mysql()
    try:
        thuchien = query_to_dataframe(f"SELECT * FROM thuchien WHERE type_process = 'LINE' AND IDnhanvien != 'LDPVNPT';", conn)
        kehoach = query_to_dataframe(f"SELECT * FROM kehoach WHERE type_process = 'LINE';", conn)
        nhanvien = query_to_dataframe("SELECT * FROM nhanvien", conn)
        dichvu = query_to_dataframe("SELECT * FROM dichvu", conn)
        line = query_to_dataframe("SELECT * FROM line_manage WHERE ma_line != 'LDPVNPT';", conn)
        for month in range(1, 13):
            kehoach[f"t{month}"] = kehoach[f"t{month}"] * 1000000
        return thuchien, kehoach, nhanvien, dichvu, line
    finally:
        conn.close()

def format_number(num):
    for unit in ['', 'K', 'Tr', 'Tỉ', 'K Tỉ']:
        if abs(num) < 1000:  
            return f"{num:.3f} {unit}"
        num /= 1000  
    return f"{num:.3f} P"
# PART EMPLOYEE DASHBOARD
def container_header_metric(filtered_thuchien,filtered_kehoach,selected_months):
    metric1 = filtered_thuchien["doanhthu"].sum()
    metric2 = filtered_kehoach[[f"t{month}" for month in selected_months]].sum().sum()
    metric3 = filtered_thuchien["nhom_dv"].nunique()

    cols_metric_employee = st.columns(3)
    cols_metric_employee[0].metric("Thực hiện", format_number(metric1))
    cols_metric_employee[1].metric("Kế hoạch", format_number(metric2))
    cols_metric_employee[2].metric("Dịch vụ thực hiện", metric3)
    return metric1, metric2, metric3

def container_first_piechart(thuchien_after_load,nhanvien_after_load,line_nv, selected_months, selected_year):
    st.markdown("""
    <h6 style="text-align:center;font-weight:bold;"> So với trong line </h6>
    """, unsafe_allow_html=True)
    line_nv_data = thuchien_after_load[(thuchien_after_load["line"] == line_nv) & 
                            (thuchien_after_load["thang"].isin(selected_months)) & 
                            (thuchien_after_load["year_insert"] == selected_year)]
    line_nv_data = line_nv_data.merge(nhanvien_after_load[['ma_nv', 'ten_nv']], left_on='IDnhanvien', right_on='ma_nv', how='left')
    pie_fig = px.pie(
        line_nv_data, 
        names="ten_nv", 
        values="doanhthu", 
        labels={"ten_nv": "Tên nhân viên"},
        hole=0.3,
    )
    pie_fig.update_traces(
        # margin=dict(t=0, b=0, l=0, r=0),
        hoverinfo="label+percent+value",  # Hiển thị nhãn, phần trăm, giá trị
        hovertemplate="<b>%{label}</b><br>Doanh thu: %{value}<br>Chiếm: %{percent}",  # Tuỳ chỉnh
        # marker=dict(line=dict(color="white", width=2)),
    )
    pie_fig.update_traces(
                    hoverlabel=dict(
                    bgcolor="lightblue",  # Màu nền khi hover
                    font_size=14,         # Kích thước chữ
                    font_color="black"    # Màu chữ
                )
    )
    

    # Tùy chỉnh vị trí và kích thước
    pie_fig.update_layout(
        legend={
            "y": -0.005, 
            "x": 0.5,
            "xanchor": "center",
            "orientation": "h",  # Đặt nhãn nằm ngang
        },
        margin=dict(l=0, r=0, t=0  , b=0),  # Tùy chỉnh lề
        height=300,  # Chiều cao biểu đồ
        width=500   # Chiều rộng biểu đồ
    )

    
    # Hiển thị biểu đồ trong Streamlit
    st.plotly_chart(pie_fig, use_container_width=True, theme="streamlit", key="pie_fig_employee")
    
def container_first_treemap(filtered_thuchien):
    st.markdown("""
                <h6 style="text-align:center;font-weight:bold;"> Thành phần doanh thu theo dịch vụ </h6>
                """, unsafe_allow_html=True)
    treemap_fig = px.treemap(filtered_thuchien, path=["ten_dv"],values="doanhthu")
    treemap_fig.update_traces(
        hoverinfo="label+value+percent parent+percent entry",
        hovertemplate="<b>%{label}</b><br>Doanh thu: %{value}<br>Chiếm: %{percentParent:.2f}%<br>Chiếm: %{percentEntry:.2f}%",
    )
    treemap_fig.update_traces(
                    hoverlabel=dict(
                    bgcolor="lightblue",  # Màu nền khi hover
                    font_size=14,         # Kích thước chữ
                    font_color="black"    # Màu chữ
                )
    )
    treemap_fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),  # Tùy chỉnh lề
        height=300,  
        width=500   
    )
    treemap_fig.data[0].texttemplate = "%{label}<br>%{value}"
    st.plotly_chart(treemap_fig, key="treemap_fig_employee", use_container_width=True)
    
def container_first_process_column(dichvu_after_load,filtered_thuchien,filtered_kehoach,selected_months):
    st.markdown("""
                    <h6 style="text-align:center;font-weight:bold;margin-bottom:8%;"> Tỷ lệ hoàn thành dịch vụ </h6>
                    """, unsafe_allow_html=True)
    process_data_dv = filtered_thuchien.groupby("nhom_dv").agg({
        "doanhthu": "sum"
    }).reset_index()
    process_data_dv["Kế hoạch"] = process_data_dv["nhom_dv"].apply(
        lambda dv: filtered_kehoach[filtered_kehoach["id_dv_606"] == dv][[f"t{month}" for month in selected_months]].sum().sum()
    )
    for dv in filtered_kehoach["id_dv_606"].unique():
        if dv not in process_data_dv["nhom_dv"].values:
            kehoach_sum = filtered_kehoach[filtered_kehoach["id_dv_606"] == dv][[f"t{month}" for month in selected_months]].sum().sum()
            if kehoach_sum != 0:
                new_row = pd.DataFrame([{
                    "nhom_dv": dv,
                    "doanhthu": 0,
                    "Kế hoạch": kehoach_sum,
                    "% Hoàn thành": "0"
                }])
                process_data_dv = pd.concat([process_data_dv, new_row], ignore_index=True)
    process_data_dv["% Hoàn thành"] = process_data_dv.apply(
        lambda row: 100 if row["Kế hoạch"] == 0 else (row["doanhthu"] / row["Kế hoạch"]) * 100, axis=1
    )
    process_data_dv["% Hoàn thành"] = process_data_dv["% Hoàn thành"].apply(lambda x: f"{x:.0f}")
    process_data_dv.loc[:,"ten_dv"] = process_data_dv["nhom_dv"].map(dichvu_after_load.set_index("ma_dv_id66")["ten_dv"])
    st.data_editor(process_data_dv[["ten_dv","% Hoàn thành"]], use_container_width=True, 
                    column_config={
                        "ten_dv": "Dịch vụ",
                        "% Hoàn thành": st.column_config.ProgressColumn(
                            "Tiến độ",
                            min_value=0,
                            max_value=100,
                            format="%d%%",
                            width="small",
                        )
                    },
                    hide_index=True,
                    disabled=True,
                    height=300
                    
                    )
    
def make_donut(input_response, input_text):

    chart_color = ['#29b5e8', '#155F7A']
        
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
    ).properties(width=200, height=200)
        
    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            # domain=['A', 'B'],
                            domain=[input_text, ''],
                            range=chart_color),  # 31333F
                        legend=None),
    ).properties(width=200, height=200)
    return plot_bg + plot + text

def container_second_donut_chart(metric1, metric2):
    st.markdown("""
                <h6 style="text-align:center;font-weight:bold;"> Tỉ lệ hoàn thành </h6>
                """, unsafe_allow_html=True)
    completion_rate = int((metric1 / metric2) * 100) if metric2 != 0 else 0
    donut_chart = make_donut(completion_rate, "Hoàn thành so với kế hoạch")
    st.altair_chart(donut_chart, use_container_width=True)
    
def container_second_barchart(thuchien_after_load,line_nv,selected_ma_nv,selected_loaidoanhthu,selected_year):
    st.markdown("""
                <h6 style="text-align:center;font-weight:bold;"> Tổng doanh thu qua các tháng </h6>
                """, unsafe_allow_html=True)
    
    filtered_thuchien_loaidoanhthu = thuchien_after_load[(thuchien_after_load["loaidoanhthu"] == selected_loaidoanhthu)&
                                                            (thuchien_after_load["line"] == line_nv)&
                                                            (thuchien_after_load["IDnhanvien"] == selected_ma_nv) &
                                                            (thuchien_after_load["year_insert"] == selected_year)]
    monthly_total_revenue = filtered_thuchien_loaidoanhthu.groupby("thang")["doanhthu"].sum().reset_index()
    monthly_total_revenue["thang"] = monthly_total_revenue["thang"].astype(int)
    
    total_revenue_fig = px.bar(monthly_total_revenue, x="thang", y="doanhthu",
                                labels={"thang": "Tháng", "doanhthu": "Tổng doanh thu"})
    total_revenue_fig.update_xaxes(tickmode='linear', dtick=1)
    total_revenue_fig.update_traces(
                    hoverlabel=dict(
                    bgcolor="lightblue",  # Màu nền khi hover
                    font_size=14,         # Kích thước chữ
                    font_color="black"    # Màu chữ
                )
    )
    total_revenue_fig.update_layout(
        legend=dict(
            y=-0.2, 
            x=0.5,
            xanchor="center",
            orientation="h",
            font=dict(color="black"),
        ),
        margin=dict(l=10, r=10, t=20, b=20),
        height=300,
        width=500
    )
    monthly_total_revenue["pct_change"] = monthly_total_revenue["doanhthu"].pct_change().fillna(0) * 100
    trend_y = monthly_total_revenue["pct_change"]
    total_revenue_fig.add_scatter(
        x=monthly_total_revenue["thang"],
        y=trend_y,
        mode="lines+markers+text",
        name="Tỷ lệ tăng trưởng",
        line=dict(color="red", width=3),
        marker=dict(size=6),
        text=monthly_total_revenue["pct_change"].apply(lambda x: f"{x:.2f}%"),
        textposition="top center",
        textfont=dict(size=12, color="#fff"),
        
    )
    total_revenue_fig.update_layout(
        xaxis=dict(
            title=dict(
                font=dict(
                    size=14,
                    color="rgb(0, 94, 124)",
                    weight="bold"
                )
            )
        ),
        yaxis=dict(
            title=dict(
                font=dict(
                    size=14,
                    color="rgb(0, 94, 124)",
                    weight="bold"
                )
            )
        )
    )
    st.plotly_chart(total_revenue_fig, key="total_revenue_fig_employee", use_container_width=True)

def container_third_barchart(filtered_thuchien,dichvu_after_load):
    st.markdown("""
                <h6 style="text-align:center;font-weight:bold;"> Biến động doanh thu theo tháng của các nhóm dịch vụ </h6>
                """, unsafe_allow_html=True)
    monthly_revenue = filtered_thuchien.groupby(["thang", "nhom_dv"])["doanhthu"].sum().reset_index()
    monthly_revenue["nhom_dv"] = monthly_revenue["nhom_dv"].map(dichvu_after_load.set_index("ma_dv_id66")["ten_dv"])
    bar_chart_fig = px.bar(monthly_revenue, x="thang", y="doanhthu", color="nhom_dv", barmode='group',
                            labels={"thang": "Tháng", "doanhthu": "Doanh thu", "nhom_dv": "Nhóm dịch vụ"})
    bar_chart_fig.update_layout(
        
        legend=dict(
            y=-0.3, 
            x=0.5,
            xanchor="center",
            orientation="h",
            font=dict(color="black"),  
        ),
        margin=dict(l=10, r=10, t=20, b=20),  

        width=500   
    )
    bar_chart_fig.update_traces(
                    hoverlabel=dict(
                    bgcolor="lightblue",  
                    font_size=14,        
                    font_color="black"    
                )
    )
    bar_chart_fig.update_layout(
        xaxis=dict(
            title=dict(
                font=dict(
                    size=14,            
                    color="rgb(0, 94, 124)",
                        weight="bold"  
                )
            )
        ),
        yaxis=dict(
            title=dict(
                font=dict(
                    size=14,
                    color="rgb(0, 94, 124)",
                        weight="bold"
                )
            )
        )
    )

    st.plotly_chart(bar_chart_fig, key="bar_chart_fig_employee", use_container_width=True)
# END EMPLOYEE DASHBOARD

# PART SERVICE DASHBOARD
def container_services_header(filtered_thuchien_dv,filtered_kehoach_dv,selected_months,selected_ten_dv,selected_ma_dv,selected_loaidoanhthu,selected_year,thuchien_after_load,kehoach_after_load,line_nv):
    cols_header_services = st.columns(3)
    # Metrics
    metric1_dv = filtered_thuchien_dv["doanhthu"].sum()
    metric2_dv = filtered_kehoach_dv[[f"t{month}" for month in selected_months]].sum().sum()
    if metric1_dv == 0 or metric2_dv == 0:
        percentage_dv_header = 0
    else:
        percentage_dv_header = (metric1_dv / metric2_dv) * 100
    # Tính toán so với tháng trước
    previous_months = [month - 1 for month in selected_months if month > 1]
    if previous_months:
        previous_filtered_thuchien_dv = thuchien_after_load[
            (thuchien_after_load["nhom_dv"] == selected_ma_dv) &
            (thuchien_after_load["thang"].isin(previous_months)) &
            (thuchien_after_load["year_insert"] == selected_year) &
            (thuchien_after_load["loaidoanhthu"] == selected_loaidoanhthu) &
            (thuchien_after_load["line"] == line_nv)
        ]
        previous_metric1_dv = previous_filtered_thuchien_dv["doanhthu"].sum()
        delta_metric1_dv = metric1_dv - previous_metric1_dv

        previous_filtered_kehoach_dv = kehoach_after_load[
            (kehoach_after_load["id_dv_606"] == selected_ma_dv) &
            (kehoach_after_load["year_insert"] == int(selected_year)) &
            (kehoach_after_load["line"] == line_nv)
        ]
        previous_filtered_kehoach_dv["thang"] = kehoach_after_load[f"t{previous_months[0]}"]
        previous_metric2_dv = previous_filtered_kehoach_dv[[f"t{month}" for month in previous_months]].sum().sum()
        delta_metric2_dv = metric2_dv - previous_metric2_dv
        delta_percentage_dv_header = (delta_metric1_dv / delta_metric2_dv) * 100 if delta_metric2_dv != 0 else 0
    else:
        delta_metric1_dv = 0
        delta_metric2_dv = 0
    
    # end so với tháng trước
    cols_header_services[0].metric("Doanh thu thực hiện", format_number(metric1_dv), delta=f"{format_number(delta_metric1_dv)} so với tháng {previous_months[0]}" if previous_months else None)
    cols_header_services[1].metric("Số kế hoạch", format_number(metric2_dv), delta=f"{format_number(delta_metric2_dv)} so với tháng {previous_months[0]}" if previous_months else None)
    cols_header_services[2].metric("Tỉ lệ hoàn thành", f"{percentage_dv_header:.2f} %", delta=f"{delta_percentage_dv_header:.2f} % so với tháng {previous_months[0]}" if previous_months else None)

def container_first_services_piechart(thuchien_after_load,dichvu_after_load,line_nv,selected_months,selected_year):
    st.markdown("""
        <h6 style="text-align:center;font-weight:bold;"> Tỷ lệ doanh thu các dịch vụ </h6>
        """, unsafe_allow_html=True)
    line_dv_data = thuchien_after_load[
        (thuchien_after_load["line"] == line_nv) & 
        (thuchien_after_load["thang"].isin(selected_months)) & 
        (thuchien_after_load["year_insert"] == selected_year)
    ]
    line_dv_data["ten_dv"] = line_dv_data["nhom_dv"].map(dichvu_after_load.set_index("ma_dv_id66")["ten_dv"])
    
    pie_fig_dv = px.pie(
        line_dv_data, 
        names="ten_dv", 
        values="doanhthu", 
        labels={"ten_dv": "Tên dịch vụ"},
        hole=0.3,
    )
    pie_fig_dv.update_traces(
        hoverinfo="label+percent+value",
        hovertemplate="<b>%{label}</b><br>Doanh thu: %{value}<br>Chiếm: %{percent}",
    )
    pie_fig_dv.update_traces(textposition='outside',
                    hoverlabel=dict(
                    bgcolor="lightblue",  # Màu nền khi hover
                    font_size=16,         # Kích thước chữ
                    font_color="black"    # Màu chữ
                )
    )
    pie_fig_dv.update_layout(
        legend={
            "y": -0.005, 
            "x": 0.5,
            "xanchor": "center",
            "orientation": "h",
        },
        margin=dict(l=0, r=0, t=0, b=0),
        height=300,
        width=500
    )
    st.plotly_chart(pie_fig_dv, use_container_width=True, theme="streamlit", key="pie_fig_dv")

def container_first_services_barchart(thuchien_after_load,selected_ma_dv,selected_loaidoanhthu,selected_year,line_nv):
    st.markdown("""
            <h6 style="text-align:center;font-weight:bold;"> Biểu đồ cột doanh thu theo tháng </h6>
            """, unsafe_allow_html=True)
    monthly_revenue_dv = thuchien_after_load[
        (thuchien_after_load["line"] == line_nv) &
        (thuchien_after_load["nhom_dv"] == selected_ma_dv) &
        (thuchien_after_load["year_insert"] == selected_year) &
        (thuchien_after_load["loaidoanhthu"] == selected_loaidoanhthu)
    ].groupby("thang")["doanhthu"].sum().reset_index()
    monthly_revenue_dv["thang"] = monthly_revenue_dv["thang"].astype(int)
    # monthly_revenue_dv = filtered_thuchien_dv.groupby("thang")["doanhthu"].sum().reset_index()
    # monthly_revenue_dv["thang"] = monthly_revenue_dv["thang"].astype(int)
    
    bar_chart_dv_fig = px.bar(monthly_revenue_dv, x="thang", y="doanhthu",
                labels={"thang": "Tháng", "doanhthu": "Doanh thu"})
    bar_chart_dv_fig.update_xaxes(tickmode='linear', dtick=1)
    bar_chart_dv_fig.update_traces(textposition='outside',
                                    hoverlabel=dict(
                                    bgcolor="lightblue",  # Màu nền khi hover
                                    font_size=16,         # Kích thước chữ
                                    font_color="black"    # Màu chữ
                                )
                                    ) 
    monthly_revenue_dv["pct_change"] = monthly_revenue_dv["doanhthu"].pct_change().fillna(0) * 100
    trend_y = monthly_revenue_dv["pct_change"]

    bar_chart_dv_fig.add_scatter(
        x=monthly_revenue_dv["thang"],
        y=trend_y,
        mode="lines+markers+text",
        name="Tỉ lệ tăng trưởng",
        line=dict(color="red", width=3),
        marker=dict(size=6),
        text=monthly_revenue_dv["pct_change"].apply(lambda x: f"{x:.2f}%"),
        textposition="top center",
        textfont=dict(size=12, color="#fff"),
    )
    bar_chart_dv_fig.update_layout(
        legend=dict(
        y=-0.2, 
        x=0.5,
        xanchor="center",
        orientation="h",
        font=dict(color="black"),
        ),
        margin=dict(l=10, r=10, t=20, b=20),
        height=300,
        width=500
    )
    bar_chart_dv_fig.update_layout(
        xaxis=dict(
            title=dict(
                font=dict(
                    size=14,                # Kích thước chữ
                    color="rgb(0, 94, 124)",
                        weight="bold"  
                )
            )
        ),
        yaxis=dict(
            title=dict(
                font=dict(
                    size=14,
                    color="rgb(0, 94, 124)",
                        weight="bold"
                )
            )
        )
    )
    st.plotly_chart(bar_chart_dv_fig, key="bar_chart_dv_fig", use_container_width=True)
    
def container_second_table_services(thuchien_after_load,nhanvien_after_load,selected_months,selected_ma_dv,selected_loaidoanhthu,selected_year,line_nv):
    st.markdown("""
                <h6 style="text-align:center;font-weight:bold;"> Doanh thu của từng nhân viên trong line </h6>
                """, unsafe_allow_html=True)
    
    # Lọc dữ liệu theo line và tháng đã chọn

    line_nv_data = thuchien_after_load[
        (thuchien_after_load["line"] == line_nv) & 
        (thuchien_after_load["thang"].isin(selected_months)) & 
        (thuchien_after_load["year_insert"] == selected_year) &
        (thuchien_after_load["loaidoanhthu"] == selected_loaidoanhthu) &
        (thuchien_after_load["nhom_dv"] == selected_ma_dv)
    ]
    
    # Tính toán doanh thu của từng nhân viên
    nv_revenue = line_nv_data.groupby("IDnhanvien")["doanhthu"].sum().reset_index()
    nv_revenue = nv_revenue.merge(nhanvien_after_load[['ma_nv', 'ten_nv']], left_on='IDnhanvien', right_on='ma_nv', how='left')
    line_total_revenue = line_nv_data["doanhthu"].sum()
    nv_revenue["ty_le_so_voi_line"] = nv_revenue["doanhthu"] / line_total_revenue * 100 if line_total_revenue != 0 else 0
    # Tính toán so với tháng trước
    previous_months = [month - 1 for month in selected_months if month > 1]
    if previous_months:
        previous_line_nv_data = thuchien_after_load[
            (thuchien_after_load["line"] == line_nv) & 
            (thuchien_after_load["thang"].isin(previous_months)) & 
            (thuchien_after_load["year_insert"] == selected_year) &
            (thuchien_after_load["loaidoanhthu"] == selected_loaidoanhthu) &
            (thuchien_after_load["nhom_dv"] == selected_ma_dv)
        ]
        previous_nv_revenue = previous_line_nv_data.groupby("IDnhanvien")["doanhthu"].sum().reset_index()
        previous_nv_revenue = previous_nv_revenue.rename(columns={"doanhthu": "doanhthu_thang_truoc"})
        nv_revenue = nv_revenue.merge(previous_nv_revenue, on="IDnhanvien", how="left")
        nv_revenue["so_voi_thang_truoc"] = nv_revenue["doanhthu"] - nv_revenue["doanhthu_thang_truoc"]
    else:
        nv_revenue["so_voi_thang_truoc"] = 0
    
    # Tính toán so với tháng 1
    month_1_data = thuchien_after_load[
        (thuchien_after_load["line"] == line_nv) & 
        (thuchien_after_load["thang"] == 1) & 
        (thuchien_after_load["year_insert"] == selected_year) &
        (thuchien_after_load["loaidoanhthu"] == selected_loaidoanhthu) &
        (thuchien_after_load["nhom_dv"] == selected_ma_dv)
    ]
    month_1_revenue = month_1_data.groupby("IDnhanvien")["doanhthu"].sum().reset_index()
    month_1_revenue = month_1_revenue.rename(columns={"doanhthu": "doanhthu_thang_1"})
    nv_revenue = nv_revenue.merge(month_1_revenue, on="IDnhanvien", how="left")
    nv_revenue["so_voi_thang_1"] = nv_revenue["doanhthu"] - nv_revenue["doanhthu_thang_1"]
    
    # Hiển thị bảng
    
    def highlight_cells_with_arrow(value):
        if value > 0:
            return f'<span style="color: green;">&#9650; {value:.2f}</span>'  # Mũi tên lên
        elif value < 0:
            return f'<span style="color: red;">&#9660; {value:.2f}</span>'   # Mũi tên xuống
        return f'<span>{value:.2f}</span>'
    nv_revenue = nv_revenue[["ten_nv", "doanhthu", "ty_le_so_voi_line", "so_voi_thang_truoc", "so_voi_thang_1"]]
    nv_revenue["so_voi_thang_truoc"] = nv_revenue["so_voi_thang_truoc"].apply(highlight_cells_with_arrow)
    nv_revenue["so_voi_thang_1"] = nv_revenue["so_voi_thang_1"].apply(highlight_cells_with_arrow)
    nv_revenue = nv_revenue.rename(columns={
        "ten_nv": "Tên nhân viên",
        "doanhthu": "Doanh thu",
        "ty_le_so_voi_line": "Tỷ lệ so với line",
        "so_voi_thang_truoc": "So với tháng trước",
        "so_voi_thang_1": "So với tháng 1"
    })

    # Hiển thị bảng trong Streamlit
    st.write(nv_revenue.to_html(escape=False, index=False,float_format="%.2f",border=1,justify="center", table_id="view_stream_service_table"), unsafe_allow_html=True)
    
    # PART FOR TABLE

# PART TABLE VIEW FOR EMPLOYEE
    # FORM 1
def filter_data_thuchien_by_employee(thuchien_after_load,ma_nv,month, year,line_nv,loaidoanhthu):
    if month is not None:
        thuchien_after_filter = thuchien_after_load[(thuchien_after_load["IDnhanvien"] == ma_nv) & 
                                                    (thuchien_after_load["line"] == line_nv) &
                                                    (thuchien_after_load["thang"] == month) &
                                                    (thuchien_after_load["year_insert"] == year) &
                                                    (thuchien_after_load["loaidoanhthu"] == loaidoanhthu)]
        thuchien_after_filter = thuchien_after_filter[["nhom_dv", "doanhthu"]]
        thuchien_after_filter["nhom_dv"] = thuchien_after_filter["nhom_dv"].str.strip()
    else:
        thuchien_after_filter = thuchien_after_load[(thuchien_after_load["IDnhanvien"] == ma_nv) & 
                                                    (thuchien_after_load["line"] == line_nv) &
                                                    (thuchien_after_load["year_insert"] == year) &
                                                    (thuchien_after_load["loaidoanhthu"] == loaidoanhthu)]
        thuchien_after_filter = thuchien_after_filter[["nhom_dv", "doanhthu", "thang","year_insert"]]
        thuchien_after_filter["nhom_dv"] = thuchien_after_filter["nhom_dv"].str.strip()
    return thuchien_after_filter
def filter_kehoach_by_employee(kehoach_after_load, dichvu_after_load,selected_ma_nv,line_nv, selected_month,selected_year,selected_loaidoanhthu):
    if selected_month is not None:
        filtered_kehoach = kehoach_after_load[
            (kehoach_after_load["ma_nv"] == selected_ma_nv) &
            (kehoach_after_load["year_insert"] == int(selected_year)) &
            (kehoach_after_load["line"] == line_nv) &
            (kehoach_after_load["loaidoanhthu"] == selected_loaidoanhthu)
        ].copy()
        filtered_kehoach.loc[:, "ten_dv"] = filtered_kehoach["id_dv_606"].map(dict(zip(dichvu_after_load["ma_dv_id66"], dichvu_after_load["ten_dv"])))
        filtered_kehoach = filtered_kehoach[["ten_dv",f"t{selected_month}"]]
    else:
        filtered_kehoach = kehoach_after_load[
            (kehoach_after_load["ma_nv"] == selected_ma_nv) &
            (kehoach_after_load["year_insert"] == int(selected_year)) &
            (kehoach_after_load["line"] == line_nv) &
            (kehoach_after_load["loaidoanhthu"] == selected_loaidoanhthu)
        ].copy()
        filtered_kehoach.loc[:, "ten_dv"] = filtered_kehoach["id_dv_606"].map(dict(zip(dichvu_after_load["ma_dv_id66"], dichvu_after_load["ten_dv"])))
        filtered_kehoach = filtered_kehoach[["ten_dv", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "t11", "t12"]]
        filtered_kehoach.rename(columns={"year_insert": "Năm"}, inplace=True)
    return filtered_kehoach
def build_hierarchy(df):
    if not {'ma_dv_id66', 'ten_dv', 'danh_muc_tt'}.issubset(df.columns):
        raise ValueError("DataFrame phải có các cột 'ma_dv_id66', 'ten_dv', và 'danh_muc_tt'")
    
    df['full_path'] = df['ten_dv']

    def build_full_path(row, df):
        if pd.isna(row['danh_muc_tt']):
            return row['ten_dv']
        else:
            parent_row = df[df['ma_dv_id66'] == row['danh_muc_tt']]
            if not parent_row.empty:
                parent_full_path = parent_row['full_path'].values[0]
                return f"{parent_full_path}.{row['ten_dv']}"
            return row['ten_dv']

    df['full_path'] = df.apply(lambda row: build_full_path(row, df), axis=1)

    df_all = df.sort_values(by=['ma_dv_id66', 'full_path'])
    
    df_filtered = df[df['ma_dv_id66'].str.count('\.') <= 2]
    
    return df_all[['ma_dv_id66', 'ten_dv', 'full_path']], df_filtered[['ma_dv_id66', 'ten_dv', 'full_path']]

def sorted_service_from_db(df_all_2):
    ma_dv_1 = df_all_2['ma_dv_id66'].tolist()
    ten_dv_1 = df_all_2['ten_dv'].tolist()
    return ma_dv_1, ten_dv_1


def create_dataframe_thuchien_tt(thang, ma_dv, ten_dv):
    ke_hoach_col = f"KẾ HOẠCH T{thang:02d}"
    thuc_hien_col = f"THỰC HIỆN T{thang:02d}"
    if thang == 1:
        thuc_hien_col = "THỰC HIỆN T1"
    columns = ["STT", "Dịch vụ", ke_hoach_col, thuc_hien_col, "% THỰC HIỆN", "KỲ TRƯỚC", "% VỚI KỲ TRƯỚC", "+/- VỚI KỲ TRƯỚC", "THỰC HIỆN T01", "% THỰC HIỆN T01", "+ /- VỚI T01"]

    # Dữ liệu
    data = {
        "STT": [*ma_dv],
        "Dịch vụ": [*ten_dv],
    }

    for col in columns[2:]:
        data[col] = [None] * len(data["STT"])

    # Tạo DataFrame
    kq_thuchien = pd.DataFrame(data, columns=columns)
    return kq_thuchien, ke_hoach_col, thuc_hien_col
def map_kehoach_to_thuchien_tt(kehoach_after_filter,df_new_create_form_1,ke_hoach_col, thang):
        for index, row in kehoach_after_filter.iterrows():
            service = row["ten_dv"]

            # Tìm vị trí của dịch vụ trong df_new_create_form_1
            matching_rows = df_new_create_form_1[df_new_create_form_1["Dịch vụ"] == service]

            # Nếu có ít nhất một hàng khớp, ánh xạ dữ liệu
            if not matching_rows.empty:
                matching_index = matching_rows.index[0]
                df_new_create_form_1.loc[matching_index, ke_hoach_col] = row[f"t{thang}"] / 1000000
            else:
                print(f"Dịch vụ '{service}' không được tìm thấy trong DataFrame 'df_new_create_form_1'.")
        return df_new_create_form_1
def map_thuchien_tt_for_form(column_data, kq_thuchien_tt, kq_thuchien):
    for index, row in kq_thuchien_tt.iterrows():
        service = row['nhom_dv']

        # Tìm vị trí của dịch vụ trong kq_thuchien
        matching_rows = kq_thuchien[kq_thuchien["STT"] == service]

        # Nếu có ít nhất một hàng khớp, ánh xạ dữ liệu
        if not matching_rows.empty:
            matching_index = matching_rows.index[0]
            # Cập nhật giá trị tương ứng trong cột
            column_name = column_data.name
            kq_thuchien.at[matching_index, column_name] = row.iloc[1] / 1000000
        else:
            print(f"Dịch vụ '{service}' không được tìm thấy trong DataFrame 'kq_thuchien'.")
    
    return kq_thuchien
def update_summary_rows(df):
    df['STT'] = df['STT'].astype(str)

    columns_to_sum = df.columns[2:]

    def get_child_rows(df, parent_stt):
        return df[df['STT'].str.startswith(parent_stt + '.')]

    for index, row in df.iterrows():
        if pd.isna(row[columns_to_sum]).all() or (row[columns_to_sum] == 0).all():

            child_rows = get_child_rows(df, row['STT'])

            if not child_rows.empty:
                df.loc[index, columns_to_sum] = child_rows[columns_to_sum].sum()

    for index, row in df.iterrows():
        if row['STT'] == '0':
            row_1 = df[df['STT'] == '1'].iloc[:, 2:].sum()
            row_2 = df[df['STT'] == '2'].iloc[:, 2:].sum()

            df.loc[index, columns_to_sum] = row_1 + row_2

    return df
def update_form_1_table(kq_dataframe, thuc_hien_col, ke_hoach_col):
    
    kq_dataframe = kq_dataframe.fillna(0).infer_objects(copy=False)
    kq_dataframe['% THỰC HIỆN'] = np.where(kq_dataframe[ke_hoach_col] != 0,
                                        kq_dataframe[thuc_hien_col] / kq_dataframe[ke_hoach_col] * 100,
                                        0)


    kq_dataframe['% VỚI KỲ TRƯỚC'] = np.where(kq_dataframe['KỲ TRƯỚC'] != 0,
                                            kq_dataframe[thuc_hien_col] / kq_dataframe['KỲ TRƯỚC'] * 100,
                                            0)
    kq_dataframe['+/- VỚI KỲ TRƯỚC'] = kq_dataframe[thuc_hien_col] - kq_dataframe['KỲ TRƯỚC']

    kq_dataframe['% THỰC HIỆN T01'] = np.where(kq_dataframe['THỰC HIỆN T01'] != 0,
                                            kq_dataframe[thuc_hien_col] / kq_dataframe['THỰC HIỆN T01'] * 100,
                                            0)

    kq_dataframe['+ /- VỚI T01'] = kq_dataframe[thuc_hien_col] - kq_dataframe['THỰC HIỆN T01']


    return kq_dataframe
    # END FORM 1
    # FORM 2
def create_dataframe_form_2(ma_dv, ten_dv):
    columns = ["STT", "Dịch vụ"] + [f"Tháng {i:02d}" for i in range(1, 13)]

    data = {
        "STT": [*ma_dv],
        "Dịch vụ": [*ten_dv],
    }

    # Tạo DataFrame
    kq_dataframe = pd.DataFrame(data, columns=columns)

    return kq_dataframe
def map_thuchien_to_form_2(kq_thuchien, kq_dataframe):
    for index, row in kq_thuchien.iterrows():
        service = row['nhom_dv']
        month = row['thang']
        revenue = row['doanhthu']

        matching_rows = kq_dataframe[kq_dataframe["STT"] == service]

        if not matching_rows.empty:
            matching_index = matching_rows.index[0]
            kq_dataframe.at[matching_index, f"Tháng {int(month):02d}"] = revenue/1000000
        else:
            print(f"Dịch vụ '{service}' không được tìm thấy trong DataFrame 'kq_dataframe'.")
    
    return kq_dataframe
    # END FORM 2
    # FORM 3
def map_kehoach_to_form_3_employee(kq_kehoach, kq_dataframe):
        for index, row in kq_kehoach.iterrows():
            service = row["ten_dv"]

 
            matching_rows = kq_dataframe[kq_dataframe["Dịch vụ"] == service]

            if not matching_rows.empty:
                matching_index = matching_rows.index[0]
                kq_dataframe.iloc[matching_index, 2:] = row[1:].values / 1000000
            else:
                print(f"Dịch vụ '{service}' không được tìm thấy trong DataFrame 'kq_dataframe'.")

        return kq_dataframe

# PART FOR TABLE VIEW FOR SERVICE
    # FORM 1
def filter_kehoach_by_service(kehoach_after_load,nhanvien_after_load,line_nv, selected_service,selected_month,year_insert,loaidoanhthu):
    if selected_month is not None:
        filtered_kehoach = kehoach_after_load[
            (kehoach_after_load["id_dv_606"] == selected_service) &
            (kehoach_after_load["year_insert"] == year_insert) &
            (kehoach_after_load["line"] == line_nv) &
            (kehoach_after_load["loaidoanhthu"] == loaidoanhthu)
        ].copy()
        filtered_kehoach.loc[:, "ten_nv"] = filtered_kehoach["ma_nv"].map(dict(zip(nhanvien_after_load["ma_nv"], nhanvien_after_load["ten_nv"])))
        filtered_kehoach = filtered_kehoach[["ma_nv","ten_nv",f"t{selected_month}"]]
    else:
        filtered_kehoach = kehoach_after_load[
            (kehoach_after_load["id_dv_606"] == selected_service) &
            (kehoach_after_load["year_insert"] == year_insert) &
            (kehoach_after_load["line"] == line_nv) &
            (kehoach_after_load["loaidoanhthu"] == loaidoanhthu)
        ].copy()
        filtered_kehoach.loc[:, "ten_nv"] = filtered_kehoach["ma_nv"].map(dict(zip(nhanvien_after_load["ma_nv"], nhanvien_after_load["ten_nv"])))
        filtered_kehoach = filtered_kehoach[["ma_nv","ten_nv", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "t11", "t12"]]
        filtered_kehoach.rename(columns={"year_insert": "Năm"}, inplace=True)
    return filtered_kehoach
def filter_thuchien_by_service(thuchien_after_load,ma_dv,month, year,line_nv,loaidoanhthu):
    if month is not None:
        thuchien_after_filter = thuchien_after_load[(thuchien_after_load["nhom_dv"] == ma_dv) & 
                                                    (thuchien_after_load["line"] == line_nv) &
                                                    (thuchien_after_load["thang"] == month) &
                                                    (thuchien_after_load["year_insert"] == year) &
                                                    (thuchien_after_load["loaidoanhthu"] == loaidoanhthu)]
        thuchien_after_filter = thuchien_after_filter[["IDnhanvien", "doanhthu"]]
        thuchien_after_filter["IDnhanvien"] = thuchien_after_filter["IDnhanvien"].str.strip()
    else:
        thuchien_after_filter = thuchien_after_load[(thuchien_after_load["nhom_dv"] == ma_dv) & 
                                                    (thuchien_after_load["line"] == line_nv) &
                                                    (thuchien_after_load["year_insert"] == year) &
                                                    (thuchien_after_load["loaidoanhthu"] == loaidoanhthu)]
        thuchien_after_filter = thuchien_after_filter[["IDnhanvien", "doanhthu", "thang","year_insert"]]
        thuchien_after_filter["IDnhanvien"] = thuchien_after_filter["IDnhanvien"].str.strip()
    return thuchien_after_filter
def create_dataframe_service_form_2(nhanvien_after_load):
    columns = ["STT", "Nhân viên"] + [f"Tháng {i:02d}" for i in range(1, 13)]

    data = {
        "STT": ["A", *nhanvien_after_load["ma_nv"].tolist()],
        "Nhân viên": ["Tổng cộng"] + nhanvien_after_load["ten_nv"].tolist(),
    }

    for col in columns[2:]:
        data[col] = [None] * len(data["STT"])

    # Tạo DataFrame
    kq_dataframe = pd.DataFrame(data, columns=columns)

    return kq_dataframe
def create_thuchien_service_dataframe_form_1(thang,nhanvien_after_load):
    kehoach_col = f"KẾ HOẠCH T{thang:02d}"
    thuchien_col = f"THỰC HIỆN T{thang:02d}"
    if thang == 1:
        thuchien_col = "THỰC HIỆN T1"
    columns = ["MA-NV", "Nhân viên", kehoach_col, thuchien_col, "% THỰC HIỆN", "KỲ TRƯỚC", "% VỚI KỲ TRƯỚC", "+/- VỚI KỲ TRƯỚC", "THỰC HIỆN T01", "% THỰC HIỆN T01", "+ /- VỚI T01"]
    
    data = {
        "MA-NV": ["A", *nhanvien_after_load["ma_nv"].tolist()],
        "Nhân viên": ["Tổng cộng"] + nhanvien_after_load["ten_nv"].tolist(),
    }
    for col in columns[2:]:
        data[col] = [None] * len(data["MA-NV"])
    kq_thuchien = pd.DataFrame(data, columns=columns)
    return kq_thuchien, kehoach_col, thuchien_col
def map_kehoach_to_thuchien_service(kehoach_after_filter,df_new_create_form_1,ke_hoach_col, thang):
        for index, row in kehoach_after_filter.iterrows():
            employee = row["ma_nv"]

            # Tìm vị trí của dịch vụ trong df_new_create_form_1
            matching_rows = df_new_create_form_1[df_new_create_form_1["MA-NV"] == employee]

            # Nếu có ít nhất một hàng khớp, ánh xạ dữ liệu
            if not matching_rows.empty:
                matching_index = matching_rows.index[0]
                df_new_create_form_1.loc[matching_index, ke_hoach_col] = row[f"t{thang}"] / 1000000
            else:
                print(f"Nhan vien '{employee}' không được tìm thấy trong DataFrame 'df_new_create_form_1'.")
        return df_new_create_form_1
def map_thuchien_service_for_form(column_data, kq_thuchien_tt, kq_thuchien):
    for index, row in kq_thuchien_tt.iterrows():
        employee = row['IDnhanvien']

        # Tìm vị trí của dịch vụ trong kq_thuchien
        matching_rows = kq_thuchien[kq_thuchien["MA-NV"] == employee]

        # Nếu có ít nhất một hàng khớp, ánh xạ dữ liệu
        if not matching_rows.empty:
            matching_index = matching_rows.index[0]
            # Cập nhật giá trị tương ứng trong cột
            column_name = column_data.name
            kq_thuchien.at[matching_index, column_name] = row.iloc[1] / 1000000
        else:
            print(f"Nhan vien '{employee}' không được tìm thấy trong DataFrame 'kq_thuchien'.")
    
    return kq_thuchien
def update_summary_rows_service(df):
    numeric_cols = df.columns[2:]  

    sums = df.loc[1:, numeric_cols].sum()

    df.loc[0, numeric_cols] = sums

    return df
    # END FORM 1
    # FORM 2
def create_data_service_form_2(nhanvien_after_load):
    columns = ["MA-NV", "Nhân viên"] + [f"Tháng {i:02d}" for i in range(1, 13)]

    data = {
        "MA-NV": ["A", *nhanvien_after_load["ma_nv"].tolist()],
        "Nhân viên": ["Tổng cộng"] + nhanvien_after_load["ten_nv"].tolist(),
    }

    for col in columns[2:]:
        data[col] = [None] * len(data["MA-NV"])

    # Tạo DataFrame
    kq_dataframe = pd.DataFrame(data, columns=columns)

    return kq_dataframe
def map_thuchien_service_to_form_2(kq_thuchien, kq_dataframe):
    for index, row in kq_thuchien.iterrows():
        service = row['IDnhanvien']
        month = row['thang']
        revenue = row['doanhthu']

        matching_rows = kq_dataframe[kq_dataframe["MA-NV"] == service]

        if not matching_rows.empty:
            matching_index = matching_rows.index[0]
            kq_dataframe.at[matching_index, f"Tháng {int(month):02d}"] = revenue/1000000
        else:
            print(f"MA-NV '{service}' không được tìm thấy trong DataFrame 'kq_dataframe'.")
    
    return kq_dataframe
    # END FORM 2
    # FORM 3
def map_kehoach_to_form_3(kq_kehoach, kq_dataframe):
    for index, row in kq_kehoach.iterrows():
        employee = row["ma_nv"]

        matching_rows = kq_dataframe[kq_dataframe["MA-NV"] == employee]

        if not matching_rows.empty:
            matching_index = matching_rows.index[0]
            kq_dataframe.iloc[matching_index, 2:] = row[2:].values / 1000000
        else:
            print(f"Nhan vien '{employee}' không được tìm thấy trong DataFrame 'kq_dataframe'.")

    return kq_dataframe