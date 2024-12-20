import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠")
st.snow()

st.title("VNPT INSIGHT")
st.write("Chào mừng bạn đến với ứng dụng để chú Toàn đánh giá nhân viên!")
st.divider()


col1, col2, col3 = st.columns(3)

# Container trong mỗi cột
with col1:
    with st.container():
        st.markdown(
            """
            <div style="
                border: 2px solid #9AE8B7;
                padding: 0px;
                border-radius: 10px;
                text-align: center;
            ">
                <h1 style="color: #9AE8B7;">20</h1>
                <h4>Nhân viên</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("Cụ thể"):
            st.write("Ngô Thiên Vương")
            st.write("Trương Trí Vĩ")
            st.write("Hoàng Xuân Quốc")
            st.write("...")

with col2:
    with st.container():
        st.markdown(
            """
            <div style="
                border: 2px solid #4E9A8D;
                border-radius: 10px;
                text-align: center;
            ">
                <h1 style="color: #4E9A8D;">03</h1>
                <h4>Phòng ban</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("Cụ thể"):
            st.write("SME1")
            st.write("SME2")
            st.write("SME3")
            st.write("...")

with col3:
    with st.container():
        st.markdown(
            """
            <div style="
                border: 2px solid #1A545D;
                border-radius: 10px;
                text-align: center;
            ">
                <h1 style="color: #1A545D;">26</h1>
                <h4>Dịch vụ</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("Cụ thể"):
            st.markdown(
            """
            <div style ="
                border: 1px solid #1A545D;
                border-radius: 10px;
                text-align: center;
            ">
            </div>
            """,
            unsafe_allow_html=True,
            ) 
            st.write("Chữ ký số")
            st.write("Học bạ số")
            st.write("Thư viện số")
            st.write("...")


