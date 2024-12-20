import streamlit as st
import pandas as pd
st.set_page_config(page_title="Page 1", page_icon="📄",layout="wide")
import seaborn as sns
import matplotlib.pyplot as plt
tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])
with tab1:

    st.title("Phân tích dữ liệu với tùy chỉnh biểu đồ và bảng")

    # Đọc dữ liệu từ file Excel đã tải lên
    file_path = "data/input_kehoach.xlsx"

    try:
        # Đọc dữ liệu
        df = pd.read_excel(file_path)

        # Lọc ra giá trị duy nhất cho selectbox
        unique_ma_nv = df['ma_nv'].dropna().unique()
        unique_id_dv_606 = df['id_dv_606'].dropna().unique()

        # Xử lý cột tháng
        month_columns = [col for col in df.columns if col.lower().startswith('t')]

        if not month_columns:
            st.error("Không tìm thấy các cột tháng (bắt đầu bằng 't').")
        else:
            # Tạo cột với tỷ lệ 1:5 cho các selectbox và nội dung
            col1, col2 = st.columns([2,4], gap = "medium")

            # Phần tùy chọn lọc dữ liệu (selectbox)
            with col1:
                st.subheader("Tùy chọn lọc dữ liệu")
                selected_ma_nv = st.selectbox("Chọn giá trị ma_nv:", unique_ma_nv)
                selected_id_dv_606 = st.selectbox("Chọn giá trị id_dv_606:", unique_id_dv_606)

            # Lọc dữ liệu theo lựa chọn
            filtered_data = df[(df['ma_nv'] == selected_ma_nv) & (df['id_dv_606'] == selected_id_dv_606)]

            # Nếu dữ liệu không tồn tại
            if filtered_data.empty:
                col2.warning("Không có dữ liệu cho lựa chọn này.")
            else:
                # Chuyển dữ liệu từ dạng rộng sang dạng dài
                monthly_data = filtered_data[month_columns].T
                monthly_data.columns = [f"{selected_ma_nv} - {selected_id_dv_606}"]
                monthly_data.index = range(1, len(monthly_data) + 1)  # Đổi tên index thành số tháng

                # Hiển thị bảng dữ liệu và biểu đồ trong cột bên phải
                with col2:
                    st.subheader(f"Kết quả phân tích cho '{selected_ma_nv}' và '{selected_id_dv_606}'")

                    # Hiển thị bảng dữ liệu
                    st.write("### Dữ liệu theo tháng")
                    st.dataframe(filtered_data)

                    # Vẽ biểu đồ
                    st.write("### Biểu đồ tăng trưởng theo tháng")
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(
                        monthly_data.index,
                        monthly_data.iloc[:, 0],
                        marker='o',
                        label=f"{selected_ma_nv} - {selected_id_dv_606}"
                    )
                    ax.set_title(f"Tăng trưởng '{selected_ma_nv}' và '{selected_id_dv_606}' theo tháng", fontsize=16)
                    ax.set_xlabel("Tháng", fontsize=12)
                    ax.set_ylabel("Giá trị", fontsize=12)
                    ax.legend()
                    ax.grid(True)

                    st.pyplot(fig)

    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")

with tab2:
    st.title("Phân tích dữ liệu với tùy chỉnh biểu đồ và bảng")

    # Đọc dữ liệu từ file Excel đã tải lên
    file_path = "data/input_kehoach.xlsx"

    try:
        # Đọc dữ liệu
        df = pd.read_excel(file_path)

        # Lọc ra giá trị duy nhất cho checkbox
        unique_ma_nv = df['ma_nv'].dropna().unique()
        unique_id_dv_606 = df['id_dv_606'].dropna().unique()

        # Xử lý cột tháng
        month_columns = [col for col in df.columns if col.lower().startswith('t')]

        if not month_columns:
            st.error("Không tìm thấy các cột tháng (bắt đầu bằng 't').")
        else:
            # Tạo layout với tỷ lệ 1:5
            col1, col2 = st.columns([2, 5], gap="medium")

            # Phần tùy chọn lọc dữ liệu (checkbox trong expander)
            with col1:
                st.subheader("Tùy chọn lọc dữ liệu")

                # Expander cho ma_nv (Đưa lên trên, luôn check tất cả giá trị)
                with st.expander("Chọn `ma_nv`", expanded=True):
                    selected_ma_nv = [
                        ma_nv for ma_nv in unique_ma_nv if st.checkbox(f"ma_nv: {ma_nv}", value=True)
                    ]
                    if not selected_ma_nv:  # Nếu không có gì được chọn, chọn tất cả
                        selected_ma_nv = list(unique_ma_nv)

                # Expander cho id_dv_606 (expanded=False, chọn mặc định giá trị đầu tiên)
                with st.expander("Chọn `id_dv_606`", expanded=False):
                    selected_id_dv_606 = []
                    for id_dv in unique_id_dv_606:
                        is_checked = st.checkbox(f"id_dv_606: {id_dv}", value=(id_dv == unique_id_dv_606[0]))
                        if is_checked:
                            selected_id_dv_606.append(id_dv)
                    if not selected_id_dv_606:  # Nếu không có gì được chọn, chọn giá trị đầu tiên
                        selected_id_dv_606 = [unique_id_dv_606[0]]

            # Lọc dữ liệu theo lựa chọn checkbox
            filtered_data = df[
                (df['ma_nv'].isin(selected_ma_nv)) & (df['id_dv_606'].isin(selected_id_dv_606))
            ]

            # Tính tổng giá trị cho từng nhân viên (ma_nv) qua các tháng
            if selected_ma_nv:  # Kiểm tra nếu có `ma_nv` được chọn
                monthly_totals_by_ma_nv = df[df['ma_nv'].isin(selected_ma_nv)].groupby('ma_nv')[month_columns].sum()
                monthly_totals_by_ma_nv['Tổng 12 tháng'] = monthly_totals_by_ma_nv.sum(axis=1)
            else:
                monthly_totals_by_ma_nv = pd.DataFrame()  # Nếu không có `ma_nv` được chọn, không hiển thị bảng

            # Tính tổng giá trị cho từng dịch vụ (id_dv_606) qua các tháng
            if selected_id_dv_606:  # Kiểm tra nếu có `id_dv_606` được chọn
                monthly_totals_by_id_dv_606 = df[df['id_dv_606'].isin(selected_id_dv_606)].groupby('id_dv_606')[month_columns].sum()
                monthly_totals_by_id_dv_606['Tổng 12 tháng'] = monthly_totals_by_id_dv_606.sum(axis=1)
            else:
                monthly_totals_by_id_dv_606 = pd.DataFrame()  # Nếu không có `id_dv_606` được chọn, không hiển thị bảng

            # Tổng giá trị 12 tháng toàn bộ nhân viên
            total_value_12_months_ma_nv = monthly_totals_by_ma_nv['Tổng 12 tháng'].sum()

            # Tổng giá trị 12 tháng toàn bộ dịch vụ
            total_value_12_months_id_dv_606 = monthly_totals_by_id_dv_606['Tổng 12 tháng'].sum()

            # Tính tỷ lệ của từng nhân viên
            monthly_totals_by_ma_nv['Tỷ lệ (%)'] = (monthly_totals_by_ma_nv['Tổng 12 tháng'] / total_value_12_months_ma_nv) * 100

            # Tính tỷ lệ của từng dịch vụ
            monthly_totals_by_id_dv_606['Tỷ lệ (%)'] = (monthly_totals_by_id_dv_606['Tổng 12 tháng'] / total_value_12_months_id_dv_606) * 100

            # Hiển thị bảng tổng số giá trị theo tháng cho `ma_nv` trong container thuộc col2
            with col2:
                st.subheader("Tổng số giá trị theo tháng của các `ma_nv`")
                col2_1, col2_2 = st.columns([1,1])
                with col2_1:

                    # Hiển thị bảng tổng số giá trị theo từng tháng của các `ma_nv`
                    if not monthly_totals_by_ma_nv.empty:
                        st.write("### Bảng tổng số giá trị theo từng tháng của các `ma_nv` đã chọn")
                        st.dataframe(
                            monthly_totals_by_ma_nv.style.set_properties(**{
                                'font-size': '12px',  # Thu nhỏ font-size trong bảng
                            })
                        )
                    else:
                        st.warning("Không có dữ liệu tổng số giá trị cho các `ma_nv` đã chọn.")

                    
                with col2_2:
                    # Biểu đồ donut tỷ lệ các nhân viên trong tổng giá trị 12 tháng
                    if not monthly_totals_by_ma_nv.empty:
                        st.write("### Biểu đồ Donut tỷ lệ các nhân viên trong tổng giá trị 12 tháng")
                        fig, ax = plt.subplots(figsize=(10, 10))  # Điều chỉnh kích thước ở đây
                        ax.pie(
                            monthly_totals_by_ma_nv['Tỷ lệ (%)'],
                            labels=monthly_totals_by_ma_nv.index,
                            autopct='%1.1f%%',
                            startangle=90,
                            colors=plt.cm.Paired.colors,
                            wedgeprops={'width': 0.3}  # Tạo khoảng trống ở giữa
                        )
                        ax.set_title("Tỷ lệ các nhân viên trong tổng giá trị 12 tháng", fontsize=16)
                        ax.axis('equal')  # Đảm bảo hình tròn

                        st.pyplot(fig)

            with col2:
                # Hiển thị bảng tổng số giá trị theo tháng cho `id_dv_606` trong container thuộc col2
                st.subheader("Tổng số giá trị theo tháng của các `id_dv_606`")
                col2_3, col2_4 = st.columns([1,1])
                with col2_3:
                    # Hiển thị bảng tổng số giá trị theo từng tháng của các `id_dv_606`
                    if not monthly_totals_by_id_dv_606.empty:
                        st.write("### Bảng tổng số giá trị theo từng tháng của các `id_dv_606` đã chọn")
                        st.dataframe(
                            monthly_totals_by_id_dv_606.style.set_properties(**{
                                'font-size': '12px',  # Thu nhỏ font-size trong bảng
                            })
                        )
                    else:
                        st.warning("Không có dữ liệu tổng số giá trị cho các `id_dv_606` đã chọn.")
                    
                with col2_4:
                    # Biểu đồ donut tỷ lệ các dịch vụ trong tổng giá trị 12 tháng
                    if not monthly_totals_by_id_dv_606.empty:
                        st.write("### Biểu đồ Donut tỷ lệ các dịch vụ trong tổng giá trị 12 tháng")
                        fig, ax = plt.subplots(figsize=(10, 10))  # Điều chỉnh kích thước ở đây
                        ax.pie(
                            monthly_totals_by_id_dv_606['Tỷ lệ (%)'],
                            labels=monthly_totals_by_id_dv_606.index,
                            autopct='%1.1f%%',
                            startangle=90,
                            colors=plt.cm.Paired.colors,
                            wedgeprops={'width': 0.3}  # Tạo khoảng trống ở giữa
                        )
                        ax.set_title("Tỷ lệ các dịch vụ trong tổng giá trị 12 tháng", fontsize=16)
                        ax.axis('equal')  # Đảm bảo hình tròn

                        st.pyplot(fig)


            # Nếu dữ liệu không tồn tại
            if filtered_data.empty:
                col2.warning("Không có dữ liệu cho lựa chọn này.")
            else:
                # Chuyển dữ liệu từ dạng rộng sang dạng dài
                monthly_data = filtered_data[month_columns].T
                monthly_data.columns = [
                    f"{ma_nv} - {id_dv}" for ma_nv, id_dv in zip(
                        filtered_data['ma_nv'], filtered_data['id_dv_606']
                    )
                ]
                monthly_data.index = range(1, len(monthly_data) + 1)  # Đổi tên index thành số tháng

                # Hiển thị bảng dữ liệu và biểu đồ trong cột bên phải
                with col2:
                    st.subheader("Kết quả phân tích")

                    # Hiển thị bảng dữ liệu
                    st.write("### Dữ liệu theo tháng")
                    st.dataframe(
                        filtered_data.style.set_properties(**{
                            'font-size': '12px',  # Thu nhỏ font-size trong bảng
                        })
                    )
    
                    # Vẽ biểu đồ
                    st.write("### Biểu đồ tăng trưởng theo tháng")
                    fig, ax = plt.subplots(figsize=(12, 6))
                    for column in monthly_data.columns:
                        ax.plot(
                            monthly_data.index,
                            monthly_data[column],
                            marker='o',
                            label=column
                        )
                    ax.set_title("Tăng trưởng theo tháng", fontsize=16)
                    ax.set_xlabel("Tháng", fontsize=12)
                    ax.set_ylabel("Giá trị", fontsize=12)
                    ax.legend(fontsize=10, loc='upper left')  # Giảm kích thước font của legend
                    ax.grid(True)

                    st.pyplot(fig)
                    

    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")


import base64

# Đường dẫn đến tệp hình ảnh cục bộ
image_path = "examples/background_2211.jpg"

# Chuyển đổi hình ảnh thành base64 để Streamlit sử dụng
def get_base64_from_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Lấy base64 từ ảnh
image_base64 = get_base64_from_image(image_path)

# CSS để thêm hình nền từ ảnh cục bộ
page_bg_css = f"""
<style>
body {{
    background-image: url("data:image/jpeg;base64,{image_base64}");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    background-repeat: no-repeat;
    opacity: 0.85; /* Độ mờ */
}}

main {{
    background-color: rgba(255, 255, 255, 0.8); /* Làm mờ nội dung chính */
    border-radius: 10px; /* Bo góc */
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Hiệu ứng đổ bóng */
}}
col2_1 {{
    border: 20px solid white;
    border-radius: 10px;
    background-color: #f0f0f0;
}}
</style>
"""
# Tab 3: Owl - Nhiều màu sắc hơn
with tab3:
    st.title("Phân tích dữ liệu với phong cách nhiều màu sắc")

    # Đường dẫn file
    file_path = "data/input_kehoach.xlsx"

    try:
        # Đọc dữ liệu
        df = pd.read_excel(file_path)

        # Xử lý dữ liệu
        unique_ma_nv = df['ma_nv'].dropna().unique()
        unique_id_dv_606 = df['id_dv_606'].dropna().unique()
        month_columns = [col for col in df.columns if col.lower().startswith('t')]

        if not month_columns:
            st.error("Không tìm thấy các cột tháng (bắt đầu bằng 't').")
        else:
            col1, col2 = st.columns([2, 5], gap="medium")

            # Lựa chọn lọc dữ liệu
            with col1:
                st.subheader("Tùy chọn lọc dữ liệu")
                selected_ma_nv = st.multiselect("Chọn ma_nv:", unique_ma_nv, default=unique_ma_nv[:2])
                selected_id_dv_606 = st.multiselect("Chọn id_dv_606:", unique_id_dv_606, default=unique_id_dv_606[:2])

            filtered_data = df[
                (df['ma_nv'].isin(selected_ma_nv)) & (df['id_dv_606'].isin(selected_id_dv_606))
            ]

            if filtered_data.empty:
                col2.warning("Không có dữ liệu phù hợp với lựa chọn.")
            else:
                # Tổng hợp dữ liệu theo tháng
                grouped_data = filtered_data.groupby(['ma_nv'])[month_columns].sum()
                grouped_data['Tổng 12 tháng'] = grouped_data.sum(axis=1)

                with col2:
                    st.subheader("Phân tích dữ liệu và biểu đồ")

                    # Hiển thị bảng với màu sắc
                    st.write("### Bảng tổng hợp dữ liệu")
                    styled_table = grouped_data.style.background_gradient(
                        cmap="coolwarm", axis=0
                    ).set_properties(**{"font-size": "12px"})
                    st.dataframe(styled_table)

                    # Biểu đồ cột (Bar chart)
                    st.write("### Biểu đồ cột")
                    fig, ax = plt.subplots(figsize=(10, 6))
                    grouped_data[month_columns].plot(kind='bar', ax=ax, color=sns.color_palette("husl", len(month_columns)))
                    ax.set_title("Tổng giá trị theo tháng", fontsize=16)
                    ax.set_xlabel("ma_nv", fontsize=12)
                    ax.set_ylabel("Giá trị", fontsize=12)
                    ax.legend(title="Tháng")
                    st.pyplot(fig)

                    # Biểu đồ heatmap
                    st.write("### Biểu đồ Heatmap")
                    fig, ax = plt.subplots(figsize=(12, 6))
                    sns.heatmap(
                        grouped_data[month_columns],
                        annot=True,
                        fmt=".0f",
                        cmap="coolwarm",
                        cbar=True,
                        ax=ax,
                    )
                    ax.set_title("Tổng giá trị theo từng tháng", fontsize=16)
                    ax.set_xlabel("Tháng", fontsize=12)
                    ax.set_ylabel("ma_nv", fontsize=12)
                    st.pyplot(fig)

    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")

