import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import pooling, Error
from mysql.connector import OperationalError, InternalError
import base64
import datetime
from streamlit_option_menu import option_menu
from datetime import date
import os
import numpy as np
import io
import plotly.express as px
from openpyxl.styles import Font, Border, Side
from openpyxl import Workbook
import openpyxl
import time
import xlsxwriter
import sys
from openpyxl.styles import PatternFill
import streamlit.components.v1 as components
import bcrypt
import requests
import PROJECTS.module_login as module_login
import PROJECTS.module_view as module_view
import PROJECTS.config as module_config
from streamlit_elements import elements, dashboard
import altair as alt

# PART SET CONFIG
st.set_page_config(layout='wide',page_title="Xem dữ liệu", page_icon='src/vnpt.ico', initial_sidebar_state='expanded')
st.logo("src\VNPT PERFORMANCE INSIGHTS (2).png", icon_image="src/vnpt.ico")
with open('src/style.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True) 
with open('src/style_view.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# PART LOGIN 
if not st.session_state.get("is_logged_in", False):
    st.warning("Bạn cần đăng nhập để xem nội dung!")
    st.session_state.is_logged_in = False
    st.session_state.role_access_admin = False
    st.session_state.line_access = None
    st.switch_page("Home.py")
    st.stop() 

# PART DESIGN FRONTEND
class DESIGN_FRONTEND():
    def __init__(self):
        pass
    def ui_info(self):
        st.header("")
        st.markdown("## **Báo cáo theo dịch vụ và nhân viên**")
    def streamlit_menu_sidebar(self):
        # st.sidebar.write("Chế độ xem:")
        # with st.sidebar:
        selected = option_menu(
            menu_title= None,  # required
            options=["Board", "Table"],  # required
            icons=["clipboard2-data", "table"],  # optional
            menu_icon= None,  # optional
            default_index=0,  # optional
            orientation="horizontal",
            key="menu_option",
            styles={
        "container": {
            "padding": "0px 5px", 
            "max-width": "30%",
            "margin": "0px auto",  
            "border": "None",
            "border-radius": "20px",
            "background-color": "rgb(120 ,189, 243)",
            "font-weight": "600"
        },
        "icon": {
            "color": "#fff",  
            "font-size": "16px"
        },
        "nav-link": {
            "font-size": "16px", 
            "text-align": "left",  
            "--hover-color": "#54a7ef",
        },
        "nav-link-selected": {
            "border-radius": "15px",
            "background-color": "#7FC8F8005E7C", 
            "font-size": "16px",
            "font-family": "Tahoma, Geneva, sans-serif",
            
        }
    }
        )
        return selected
    def sidebar_option(self):
        selected = st.sidebar.radio("Dữ liệu theo dõi:",["👩‍💻 Nhân viên", "🌁 Dịch vụ"],horizontal=True)
        st_toggle_check = st.sidebar.empty()
        if selected == "👩‍💻 Nhân viên":
            if st_toggle_check.toggle("Chọn nhiều tháng", False, key="select_multiple_month"):
                selected_months = st.sidebar.multiselect("Chọn tháng", range(1, 13), default=[1], help="Chọn nhiều tháng để xem dữ liệu")
            else:
                selected_months = st.sidebar.multiselect("Chọn tháng", range(1, 13), default=[1], max_selections=1, help="Bạn chỉ được chọn 1 tháng")
        else:
            st_toggle_check.empty()
            selected_months = st.sidebar.multiselect("Chọn tháng", range(1, 13), default=[1], max_selections=1, help="Bạn chỉ được chọn 1 tháng")
        selected_loaidoanhthu = st.sidebar.selectbox("Chọn loại doanh thu", thuchien_after_load["loaidoanhthu"].unique())
        line_nv = st.session_state.line_access
        if (selected == "👩‍💻 Nhân viên"):
            nv_mapping = dict(zip(nhanvien_after_load["ma_nv"], nhanvien_after_load["ten_nv"]))
            selected_nv_name = st.sidebar.selectbox("Chọn nhân viên", nhanvien_after_load["ten_nv"].unique())
            selected_data_kind = nhanvien_after_load[nhanvien_after_load["ten_nv"] == selected_nv_name]["ma_nv"].values[0]
        else:
            selected_dv = st.sidebar.selectbox("Chọn dịch vụ", dichvu_after_load["ten_dv"].unique())
            dv_mapping = dict(zip(dichvu_after_load["ten_dv"], dichvu_after_load["ma_dv_id66"]))
            selected_data_kind = dv_mapping[selected_dv]
        selected_year = st.sidebar.selectbox("Chọn năm", kehoach_after_load["year_insert"].astype(int).unique())
        return selected,selected_months,selected_year,selected_loaidoanhthu,line_nv,selected_data_kind
    def employee_design_frontend(self, selected_months,line_nv, selected_year, selected_loaidoanhthu, selected_ma_nv):
        # Lọc dữ liệu
        filtered_thuchien = thuchien_after_load[
        (thuchien_after_load["IDnhanvien"] == selected_ma_nv) &
        (thuchien_after_load["thang"].isin(selected_months)) &
        (thuchien_after_load["year_insert"] == int(selected_year)) &
        (thuchien_after_load["loaidoanhthu"] == selected_loaidoanhthu) &
        (thuchien_after_load["line"] == line_nv)
    ]

        filtered_kehoach = kehoach_after_load[
        (kehoach_after_load["ma_nv"] == selected_ma_nv) &
        (kehoach_after_load["year_insert"] == int(selected_year)) &
        (kehoach_after_load["line"] == line_nv)
    ]
        
        # CONTAINER 1
        container_header_metric = st.container(key="container_header_service")
        with container_header_metric:
            metric1,metric2,metric3= module_view.container_header_metric(filtered_thuchien,filtered_kehoach,selected_months)
        # CONTAINER 2
        container_first_employee = st.container(border=False)
        with container_first_employee:
            cols_first_employee = st.columns([15,30,15])
            with cols_first_employee[0]:
                # Biểu đồ tròn
                module_view.container_first_piechart(thuchien_after_load,nhanvien_after_load,line_nv, selected_months, selected_year)
                
        with cols_first_employee[1]:
                # TreeMap
                module_view.container_first_treemap(filtered_thuchien)
        with cols_first_employee[2]:
                # Process Column
            module_view.container_first_process_column(dichvu_after_load,filtered_thuchien,filtered_kehoach, selected_months)
        # CONTAINER 3
        container_second_employee = st.container(border=False)
        with container_second_employee:
            cols_second_employee = st.columns([15,30,15])
            with cols_second_employee[0]:
                # Biểu đồ Donut
                module_view.container_second_donut_chart(metric1, metric2)
            with cols_second_employee[1]:
                # Biểu đồ cột
                module_view.container_second_barchart(thuchien_after_load,line_nv,selected_ma_nv,selected_loaidoanhthu,selected_year)
            with cols_second_employee[2]:
                # DESCRIPTION DASHBOARD
                st.markdown("""
                <h6 style="text-align:center;font-weight:bold;"> Mô tả dashboard 🤔 </h6>
                <p style="text-align:justify;"> Dashboard này giúp bạn theo dõi:</p>
                <ul style="text-align:left;">
                    <li>Doanh thu của nhân viên theo từng dịch vụ, từng tháng.</li>
                    <li>Tỷ lệ hoàn thành so với kế hoạch.</li>
                    <li>Biểu đồ cột thể hiện doanh thu qua các tháng</li>
                </ul>
                """, unsafe_allow_html=True)

    # CONTAINER 4
        container_third_employee = st.container(border=False)
        with container_third_employee:
            cols_third_employee = st.columns([46,15])
            with cols_third_employee[0]:
                # Biểu đồ cột
                module_view.container_third_barchart(filtered_thuchien)

            with cols_third_employee[1]:
                st.markdown("""
                <h6 style="text-align:center;font-weight:bold;"> Hơn nữa 🤔 </h6>
                <p style="text-align:justify;"> Dashboard này còn có các biểu đồ:</p>
                <ul style="text-align:left;">
                    <li>Biểu đồ tròn tỷ lệ doanh thu giữa các thành viên trong line</li>
                    <li>Biểu đồ treemap thể hiện tỷ lệ doanh thu của các dịch vụ của nhân viên đó.</li>
                    <li>Biểu đồ cột ghép - thể hiện doanh thu theo các tháng của các nhóm dịch vụ</li>
                </ul>
                """, unsafe_allow_html=True)
    def service_design_frontend(self, selected_months,line_nv, selected_year, selected_loaidoanhthu, selected_ma_dv):
        selected_ten_dv = dichvu_after_load[dichvu_after_load["ma_dv_id66"] == selected_ma_dv]["ten_dv"].values[0]
        filtered_thuchien_dv = thuchien_after_load[
        (thuchien_after_load["nhom_dv"] == selected_ten_dv) &
        (thuchien_after_load["thang"].isin(selected_months)) &
        (thuchien_after_load["year_insert"] == selected_year) &
        (thuchien_after_load["loaidoanhthu"] == selected_loaidoanhthu) &
        (thuchien_after_load["line"] == line_nv)
    ]

        filtered_kehoach_dv = kehoach_after_load[
            (kehoach_after_load["id_dv_606"] == selected_ma_dv) &
            (kehoach_after_load["year_insert"] == int(selected_year)) &
            (kehoach_after_load["line"] == line_nv)
        ]
        container_header_services = st.container(key="container_header_services")
        with container_header_services:
            module_view.container_services_header(filtered_thuchien_dv,filtered_kehoach_dv,selected_months,selected_ten_dv,selected_ma_dv,selected_loaidoanhthu,selected_year,thuchien_after_load,kehoach_after_load,line_nv)
        # CONTAINER 2
        container_first_services = st.container(key="container_first_services")
        with container_first_services:
            cols_first_services = st.columns([15, 30])
            with cols_first_services[0]:
                module_view.container_first_services_piechart(thuchien_after_load,line_nv,selected_months, selected_year)
            with cols_first_services[1]:
                module_view.container_first_services_barchart(thuchien_after_load,selected_ten_dv,selected_loaidoanhthu,selected_year,line_nv)
        # CONTAINER 3
        container_second_services = st.container(key="container_second_services")
        with container_second_services:
            cols_second_services = st.columns([46, 15])
            with cols_second_services[0]:
                module_view.container_second_table_services(thuchien_after_load,nhanvien_after_load,selected_months,selected_ten_dv,selected_loaidoanhthu,selected_year,line_nv)
            
            with cols_second_services[1]:
                image_dashboard = module_config.get_relative_file_path("../src/dashboard.png")
                st.markdown(f"""
                <h6 style="text-align:center;font-weight:bold;"> Dashboard mô tả dịch vụ</h6>
                <img src="data:image/png;base64,{image_dashboard}" style="display:block; margin-left:auto; margin-right:auto; width:30%;">
                <ul style="text-align:left;">
                    <li>Các metric </li>
                    <li>Biểu đồ tròn tỷ lệ dịch vụ với nhau trong tháng</li>
                    <li>Biểu đồ cột ghép - thể hiện doanh thu và tỷ lệ tăng trưởng</li>
                    <li>Bảng đóng góp của từng thành viên trong line đối với dịch vụ tháng đó.</li>
                </ul>
                """, unsafe_allow_html=True)
    
# PART MAIN APP
class MAIN_APP():
    def __init__(self):
        pass
        
    def main(self,selected):
        class_design_frontend = DESIGN_FRONTEND()
        if selected == "Board":
            selected_option,selected_months,selected_year,selected_loaidoanhthu,line_nv,selected_data_kind = class_design_frontend.sidebar_option()
            if selected_option == "👩‍💻 Nhân viên":
                class_design_frontend.employee_design_frontend(selected_months,line_nv, selected_year, selected_loaidoanhthu, selected_data_kind)
            else:
                class_design_frontend.service_design_frontend(selected_months,line_nv, selected_year, selected_loaidoanhthu, selected_data_kind)
        elif selected == "Table":
            st.dataframe(thuchien_after_load)
        
if __name__ == "__main__":
    thuchien_after_load, kehoach_after_load, nhanvien_after_load, dichvu_after_load = module_view.load_data()     
    design_frontend_class = DESIGN_FRONTEND()
    main_app_class = MAIN_APP()
    selected_menu_sidebar = design_frontend_class.streamlit_menu_sidebar()
    main_app_class.main(selected_menu_sidebar)
    container_menu = st.sidebar.container(key="container_menu_view")
   
# line = st.session_state.line_access



