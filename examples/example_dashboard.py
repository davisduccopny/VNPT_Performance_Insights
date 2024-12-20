import streamlit as st
import pandas as pd

# Dữ liệu giả lập
data = {
    "employee": ["Alice", "Bob", "Charlie", "Diana", "Alice", "Bob", "Charlie", "Diana"],
    "service": ["Service A", "Service A", "Service B", "Service C", "Service B", "Service C", "Service A", "Service C"],
    "completion_percentage": [85, 75, 95, 60, 80, 70, 90, 65]
}

df = pd.DataFrame(data)

# Tính tỷ lệ hoàn thành trung bình của các dịch vụ
service_data = df.groupby('service').agg({'completion_percentage': 'mean'}).reset_index()

# Giao diện Streamlit
st.title("Dashboard: Nhân viên và Dịch vụ")

# Cột trái: Danh sách nhân viên và progress bar
st.sidebar.header("Danh sách nhân viên")
employee_list = df['employee'].unique().tolist()

# Sử dụng checkbox để chọn nhân viên
selected_employees = st.sidebar.multiselect("Chọn nhân viên", employee_list)

# Lọc dữ liệu theo các nhân viên đã chọn
if selected_employees:
    filtered_employee_data = df[df['employee'].isin(selected_employees)]
else:
    filtered_employee_data = pd.DataFrame(columns=df.columns)  # Nếu không chọn ai, hiển thị bảng trống

# Hiển thị bảng nhân viên với tiến độ hoàn thành
if not filtered_employee_data.empty:
    avg_completion = filtered_employee_data['completion_percentage'].mean()
    st.sidebar.subheader(f"Tổng tiến độ hoàn thành: {avg_completion:.2f}%")
    st.sidebar.progress(avg_completion / 100)  # Hiển thị progress bar cho tiến độ trung bình của các nhân viên đã chọn

# Hiển thị bảng danh sách nhân viên và tiến độ
st.subheader("Danh sách nhân viên và tiến độ hoàn thành")
employee_table = df.groupby("employee")["completion_percentage"].mean().reset_index()

# Định dạng bảng sử dụng df.style.format
styled_employee_table = employee_table.style.format({
    'completion_percentage': '{:.2f}%',  # Định dạng hiển thị phần trăm
})

# Hiển thị bảng nhân viên
st.dataframe(styled_employee_table)

# Cột phải: Danh sách dịch vụ và tỷ lệ hoàn thành trung bình của tất cả nhân viên
st.subheader("Danh sách các dịch vụ và tỷ lệ hoàn thành trung bình")
if selected_employees:
    filtered_service_data = df[df['employee'].isin(selected_employees)].groupby('service').agg({'completion_percentage': 'mean'}).reset_index()
else:
    filtered_service_data = service_data

# Định dạng bảng dịch vụ sử dụng df.style.format
styled_service_table = filtered_service_data.style.format({
    'completion_percentage': '{:.2f}%',  # Định dạng hiển thị phần trăm
})

# Hiển thị bảng dịch vụ
st.dataframe(styled_service_table)
