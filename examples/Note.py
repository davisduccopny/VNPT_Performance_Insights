import streamlit as st
import pandas as pd

st.title("Hiển thị file Excel với nhiều tab")

# Tải file Excel lên
uploaded_file = st.file_uploader("Tải lên file Excel", type=["xlsx", "xls"])

if uploaded_file:
    # Đọc file Excel
    excel_file = pd.ExcelFile(uploaded_file)
    sheet_names = excel_file.sheet_names  # Lấy danh sách tên sheet
    
    # Chọn sheet để hiển thị
    selected_sheet = st.selectbox("Chọn tab (sheet) để hiển thị:", sheet_names)
    
    # Đọc dữ liệu của sheet được chọn
    sheet_data = excel_file.parse(selected_sheet)
    
    # Hiển thị dữ liệu
    st.write(selected_sheet)
    
    
    st.dataframe(sheet_data)
