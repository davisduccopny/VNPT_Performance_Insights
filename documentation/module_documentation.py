import streamlit as st
import os
import base64

def get_full_filepaths(file_array):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return [os.path.join(base_path, file) for file in file_array]
def encode_images(filepaths):
    encoded_images = []
    for full_file_path in filepaths:
        with open(full_file_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            encoded_images.append(encoded_image)
    return encoded_images


array_documentation_for_view = [
    "view_app/image.png",
    "view_app/image-1.png",
    "view_app/image-2.png",
    "view_app/image-3.png",
    "view_app/image-4.png",
    "view_app/image-5.png",
    "view_app/image-6.png",
    "view_app/image-7.png",
    "view_app/image-8.png",
    "view_app/image-9.png",
    "view_app/image-10.png",
    "view_app/image-11.png",
    "view_app/image-12.png",
    "view_app/image-13.png",
    "view_app/image-14.png",
    "insert_data/image.png",
    "insert_data/image-1.png",
    "insert_data/image-2.png",
    "insert_data/image-3.png",
    "insert_data/image-4.png",
    "insert_data/image-5.png",
    "insert_data/image-6.png",
    "insert_data/image-7.png",
    "insert_data/image-8.png",
    "insert_data/image-9.png",
    "insert_data/image-10.png",
    "insert_data/image-11.png"
]

full_filepaths_array_documentation_for_view  = encode_images(get_full_filepaths(array_documentation_for_view))
def dashboard_documentation():
    st.markdown(f"""

        <h4>a. Mục đích, ý nghĩa</h4>
        <p>
            Được thiết kế để trực quan hóa các dữ liệu theo dạng bảng, hiển thị dữ liệu theo thời gian thực nhằm hỗ trợ 
            người dùng nắm bắt thực trạng và đưa ra quyết định tốt hơn trong công việc.
        </p>

        <h4>b. Hướng dẫn chi tiết:</h4>

        <h5>Theo dõi dữ liệu của nhân viên:</h5>
        <ol>
            <li>
                Bấm vào “Xem dữ liệu” → Chọn “Nhân viên” và dữ liệu muốn xem theo nhu cầu công việc.
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[0]}" alt="alt text" style="width: 30%;">
                </div>
            </li>
            <li>
                Click lựa chọn dữ liệu cần theo dõi → Hiển thị bảng dashboard trên màn hình chính.
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[1]}" alt="alt text" style="width: 30%;">
                </div>
            </li>
            <li>
                Hiển thị các biểu đồ:
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[2]}" alt="Biểu đồ tree map" style="width: 30%;"><br>
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[3]}" alt="Biểu đồ tròn" style="width: 30%;"><br>
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[4]}" alt="Biểu đồ cột kết hợp đường" style="width: 30%;"><br>
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[5]}" alt="Biểu đồ cột biến động" style="width: 30%;">
                </div>
            </li>
        </ol>

        <h5>Theo dõi dữ liệu của dịch vụ:</h5>
        <ol>
            <li>
                Chọn “Dịch vụ” và dữ liệu muốn xem theo nhu cầu công việc.
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[6]}" alt="Bảng chọn dữ liệu dịch vụ" style="width: 30%;">
                </div>
            </li>
            <li>
                Click chọn dữ liệu cần theo dõi → Hiển thị dashboard trên màn hình.
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[7]}" alt="Dashboard dịch vụ" style="width: 30%;">
                </div>
            </li>
            <li>
                Hiển thị các biểu đồ:
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[8]}" alt="Biểu đồ tròn doanh thu" style="width: 30%;"><br>
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[9]}" alt="Biểu đồ cột doanh thu" style="width: 30%;"><br>
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[10]}" alt="Bảng doanh thu nhân viên" style="width: 30%;">
                </div>
            </li>
        </ol>

        <hr>
                
                
    """, unsafe_allow_html=True)
def table_documentation():
    st.markdown(f"""
        <h4>a. Mục đích, ý nghĩa</h4>
        <p>
            - Hỗ trợ người quản lý theo dõi mức độ hoàn thành công việc của nhân viên trong tổ so với kế hoạch được giao 
            theo từng tháng và loại hình dịch vụ.<br>
            - Hỗ trợ theo dõi số lượng cụ thể của một dịch vụ đã được thực hiện trong tháng và nhân viên đã thực hiện.
        </p>

        <h4>b. Cách thực hiện</h4>

        <h5>Xem bảng nhân viên:</h5>
        <ol>
            <li>
                Chọn “Xem dữ liệu” → Chọn “Table” → Chọn “Nhân viên” → Chọn “Xem”.
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[11]}" alt="Bảng dữ liệu nhân viên" style="width: 30%;">
                </div>
            </li>
            <li>
                Để thay đổi bảng dữ liệu của nhân viên khác, có thể thay đổi các yếu tố trong phần “Dữ liệu theo dõi” 
                ở góc trái màn hình.
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[12]}" alt="Bảng chọn dữ liệu" style="width: 30%;">
                </div>
            </li>
        </ol>

        <h5>Xem bảng dịch vụ:</h5>
        <ol>
            <li>
                Chọn “Xem dữ liệu” → Chọn “Table” → Chọn “Dịch vụ” → Chọn “Xem”.
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[13]}" alt="Bảng dữ liệu dịch vụ" style="width: 30%;">
                </div>
            </li>
            <li>
                Để xem dữ liệu của các dịch vụ khác, có thể thay đổi các yếu tố trong phần “Dữ liệu theo dõi” 
                ở góc trái màn hình.
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[14]}" alt="Bảng chọn dữ liệu" style="width: 30%;">
                </div>
            </li>
        </ol>
                """,unsafe_allow_html=True)
def insert_data_documentation():
    st.markdown(f"""
                <h4 style="text-align: left;">a. Mục đích, ý nghĩa</h4>
                <ul>
                    <li>Được thiết kế nhằm hỗ trợ quản lý và trực quan hóa các dữ liệu cần theo dõi, tổng hợp.</li>
                </ul>

                <h4 style="text-align: left;">b. Cách thực hiện</h4>
                <ul>
                    <li>Thêm dữ liệu kế hoạch:
                    <ol>
                        <li>Bước 1: Chọn “Thêm dữ liệu” → Chọn “Năm” → Chọn “Loại doanh thu” → Chọn “File Excel”.</li>
                        <li>Bước 2: Chọn “Up database”.</li>
                    </ol>
                    <div style="text-align: center; margin: 20px 0;">
                        <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[15]}" alt="Bảng chọn dữ liệu kế hoạch" style="max-width: 30%; height: auto; border: 1px solid #ccc;"/>
                    </div>
                    </li>
                    <li>Thêm dữ liệu thực hiện:
                    <ol>
                        <li>Bước 1: Chọn “Thêm dữ liệu” → Chọn “Năm dự án” → Chọn “Tháng thực hiện” → Chọn “Doanh thu dự án” → Chọn “File Excel”.</li>
                        <li>Bước 2: Chọn “Up database”.</li>
                    </ol>
                    <div style="text-align: center; margin: 20px 0;">
                        <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[16]}" alt="Thêm dữ liệu thực hiện" style="max-width: 30%; height: auto; border: 1px solid #ccc;"/>
                    </div>
                    </li>
                </ul>

                """, unsafe_allow_html=True)
def managerment_service_documentation():
    st.markdown(f"""
                <h2 style="text-align: left;">Quản lý dịch vụ</h2>
                <h4 style="text-align: left;">a. Mục đích, ý nghĩa</h4>
                <ul>
                    <li>Được thiết kế để hỗ trợ công tác theo dõi số lượng và tiến độ thực hiện dịch vụ, có thể thêm và chỉnh sửa nếu như có thêm dịch vụ mới và xóa những dịch vụ không cần thiết.</li>
                </ul>

                <h4 style="text-align: left;">b. Cách thực hiện</h4>
                <ul>
                    <li>Dùng để xem:
                    <ol>
                        <li>Bước 1: Chọn “Thêm dữ liệu” → Chọn “Quản lý dịch vụ”.</li>
                        <li>Bước 2: Chọn “Chế độ” → “Xem” → Chọn “Cập nhật”.</li>
                    </ol>
                    <div style="text-align: center; margin: 20px 0;">
                        <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[17]}" alt="Chế độ xem" style="max-width: 50%; height: auto; border: 1px solid #ccc;"/>
                    </div>
                    </li>
                    <li>Dùng để thêm dữ liệu:
                    <ol>
                        <li>Bước 1: Chọn “Thêm dữ liệu” → Chọn “Quản lý dịch vụ”.</li>
                        <li>Bước 2: Chọn “Chế độ” → Chọn “Thêm” → Chọn “Cập nhật”.</li>
                    </ol>
                    <div style="text-align: center; margin: 20px 0;">
                        <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[18]}" alt="Chế độ thêm" style="max-width: 50%; height: auto; border: 1px solid #ccc;"/>
                    </div>
                    </li>
                    <li>Dùng để chỉnh sửa dữ liệu:
                    <ol>
                        <li>Bước 1: Chọn “Thêm dữ liệu” → Chọn “Quản lý dịch vụ”.</li>
                        <li>Bước 2: Chọn “Chế độ” → Chọn “Chỉnh sửa” → Chọn “Cập nhật”.</li>
                    </ol>
                    <div style="text-align: center; margin: 20px 0;">
                        <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[19]}" alt="Chế độ chỉnh sửa" style="max-width: 50%; height: auto; border: 1px solid #ccc;"/>
                    </div>
                    </li>
                    <li>Dùng để xóa dữ liệu:
                    <ol>
                        <li>Bước 1: Chọn “Thêm dữ liệu” → Chọn “Quản lý dịch vụ”.</li>
                        <li>Bước 2: Chọn “Chế độ” → Chọn “Xóa” → Chọn “Cập nhật”.</li>
                    </ol>
                    <div style="text-align: center; margin: 20px 0;">
                        <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[20]}" alt="Chế độ xóa" style="max-width: 50%; height: auto; border: 1px solid #ccc;"/>
                    </div>
                    </li>
                </ul>
                """, unsafe_allow_html=True)
def user_documentation():
    st.markdown(f"""
        <h4 style="text-align: left;">a. Mục đích, ý nghĩa</h4>
        <ul>
            <li>Được thiết kế nhằm hỗ trợ quản lý thông tin cá nhân của người dùng, vai trò, cũng như thống kê hiệu suất làm việc trong hệ thống. Từ đó có thể dễ dàng theo dõi, phân tích và đánh giá.</li>
        </ul>

        <h4 style="text-align: left;">b. Cách thực hiện</h4>
        <ul>
            <li>Truy cập để xem thông tin:
            <ol>
                <li>Chọn “Home” → Chọn “Người dùng” → Chọn “Chung”.</li>
            </ol>
            <div style="text-align: center; margin: 20px 0;">
                <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[21]}" alt="Người dùng" style="max-width: 50%; height: auto; border: 1px solid #ccc;"/>
            </div>
            </li>
            <li>Truy cập để sửa mật khẩu:
            <ol>
                <li>Chọn “Home” → Chọn “Người dùng” → Chọn “Mật khẩu”.</li>
            </ol>
            <div style="text-align: center; margin: 20px 0;">
                <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[22]}" alt="Chỉnh sửa mật khẩu" style="max-width: 50%; height: auto; border: 1px solid #ccc;"/>
            </div>
            </li>
            <li>Truy cập để sửa thông tin:
            <ol>
                <li>Chọn “Home” → Chọn “Người dùng” → Chọn “Hiển thị” → Chọn “Save”.</li>
            </ol>
            <div style="text-align: center; margin: 20px 0;">
                <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[23]}" alt="Chỉnh sửa thông tin" style="max-width: 50%; height: auto; border: 1px solid #ccc;"/>
            </div>
            </li>
            <li>Truy cập để xóa tài khoản:
            <ol>
                <li>Chọn “Home” → Chọn “Người dùng” → Chọn “Khác”.</li>
            </ol>
            <div style="text-align: center; margin: 20px 0;">
                <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[24]}" alt="Xóa tài khoản" style="max-width: 50%; height: auto; border: 1px solid #ccc;"/>
            </div>
            </li>
        </ul>
                """, unsafe_allow_html=True)
def expand_and_management_user():
    st.markdown("""

                <h4 style="text-align: left;">a. Mục đích và ý nghĩa</h4>
                <ul>
                    <li>Được thiết kế để quản lý số lượng tài khoản đăng nhập và phân quyền cho từng tài khoản theo chức năng ở trong line.</li>
                </ul>
                
                <h4 style="text-align: left;">b. Cách thức thực hiện</h4>
                <ul>
                    <li>Để thêm một tài khoản:
                    <ol>
                        <li>Chọn “Mở rộng” → Chọn “Users” → Chọn “Đồng ý” / “Bỏ qua”.</li>
                    </ol>
                    </li>
                    <li>Để tải tài liệu:
                    <ol>
                        <li>Chọn “Mở rộng” → Chọn “Xuất Excel”.</li>
                    </ol>
                    </li>
                </ul>
                
                """, unsafe_allow_html=True)
def delete_data_documentation():
    st.markdown(f"""
                <h4 style="text-align: left;">a. Mục đích, ý nghĩa</h4>
                <ul>
                    <li>Được thiết kế nhằm hỗ trợ người dùng có thể xóa các tài liệu đã nhập sai vào cơ sở dữ liệu trong hệ thống.</li>
                </ul>
                
                <h4 style="text-align: left;">b. Cách thực hiện</h4>
                <ul>
                    <li>Xóa dữ liệu kế hoạch:
                    <ol>
                        <li>Chọn “Xóa dữ liệu” → Chọn “Kế hoạch” → Chọn “Năm” → Chọn “Xóa khỏi csdl”.</li>
                    </ol>
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[25]}" alt="Xóa dữ liệu kế hoạch" style="max-width:50%; height: auto; border: 1px solid #ccc;"/>
                    </li>
                    <li>Để xóa dữ liệu thực hiện:
                    <ol>
                        <li>Chọn “Xóa dữ liệu” → Chọn “Thực hiện” → Chọn “Năm” → Chọn “Loại doanh thu” → Chọn “Tháng” → Chọn “Xóa khỏi csdl”.</li>
                    </ol>
                    <img src="data:image/png;base64,{full_filepaths_array_documentation_for_view[26]}" alt="Xóa dữ liệu thực hiện" style="max-width:50%; height: auto; border: 1px solid #ccc;"/>
                    </li>
                </ul>
                
                """,unsafe_allow_html=True)