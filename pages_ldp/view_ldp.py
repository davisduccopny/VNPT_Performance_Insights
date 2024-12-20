import streamlit as st
import pandas as pd
import base64
from streamlit_option_menu import option_menu
import numpy as np
import io
from openpyxl.styles import Font, Border, Side
from openpyxl import Workbook
import openpyxl
import time
import PROJECTS.module_view as module_view
import PROJECTS.config as module_config
import streamlit.components.v1 as components

# PART LOGIN 
if not st.session_state.get("is_logged_in", False):
    with st.spinner("🔐 Đang chuyển hướng đến trang đăng nhập..."):
        time.sleep(2)
    st.session_state.is_logged_in = False
    st.session_state.role_access_admin = False
    st.session_state.line_access = None
    st.switch_page("main.py")
    st.stop() 
# PART SET CONFIG
with open('src/style_general.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
with open('src/style_ldp/style_view.css', encoding="utf-8")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

class VIEW_LDP():
    def __init__(self):
        pass
class MAIN_VIEW():
    def __init__(self):
        pass
    def sidebar_viewldp(self):
        with st.sidebar:
            selected = option_menu(
                    menu_title= None,  # required
                    options=["Dạng bảng theo tháng", "Dạng bảng tổng hợp"],  # required
                    icons=["calendar2-range-fill", "calendar3"],  
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
    def run_view(self):
        selected = self.sidebar_viewldp()
        if selected == "Dạng bảng theo tháng":
            st.title("Dạng bảng theo tháng")
        elif selected == "Dạng bảng tổng hợp":
            st.title("Dạng bảng tổng hợp")
            
thuchien_after_load, kehoach_after_load, nhanvien_after_load, dichvu_after_load,line_after_load = module_view.load_data() 
MAIN_VIEW().run_view()