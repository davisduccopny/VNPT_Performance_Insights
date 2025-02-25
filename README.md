<h1 align="center">VNPT Performance Insights</h1>
<div  align="center"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/src/VNPT_PERFORMANCE_INSIGHTS__2_-removebg-preview.png" width="250" alt="VNPT Performance Insights"></div>

<br>
<p>Dự án xây dựng công cụ VNPT-PIS giúp tự động hóa quy trình tạo báo cáo từ dữ liệu thô, đồng thời xây dựng dashboard trực quan. Ứng dụng xây dựng trong thời gian thực tập tại Tập đoàn Bưu chính - Viễn thông Việt Nam (VNPT).</p>
<h2 align="left">📌 1. Yêu cầu cho công cụ</h2>

🎯 Tự động xử lý dữ liệu, chuẩn hóa, loại bỏ lỗi và hợp nhất từ nhiều nguồn.<br>
🎯 Xây dựng Dashboard hiển thị KPIs, lọc dữ liệu động.<br>
🎯 Tạo báo cáo Excel tự động nếu cần.<br>
🎯 Đánh giá được nhân viên dựa trên dịch vụ, line, và doanh thu theo thời gian.<br>
🎯 Có hai cấp độ website: 1️⃣ Một cho nhân viên cấp thấp sử dụng theo từng line (tổ). 2️⃣ Hai cho lớp quản lý tầm trung.<br>
🎯 Bảo mật & phân quyền hợp lý, hhạn chế chỉnh sửa, mã hóa dữ liệu, xác thực đăng nhập.<br>

<h2 align="left">👨‍💻 2. Công Nghệ chính Sử Dụng</h2>

*🟢 Python 3.11.5* <br>
*🟢 Framework Streamlit* <br>
*🟢 MySQL 8.0.27* <br>

<h2 align="left">🔄 3. Tự Động Hóa</h2>

- Tạo báo cáo excel, cho phép tải về với nhiều form tùy chỉnh.
- Tự động hóa xử lý dữ liệu, chuẩn hóa, loại bỏ lỗi.
- Tự động tạo dashboard trực quan.

<h2 align="left">📁 4. Cấu trúc thư mục </h2>

```
📦 VNPT_PERFORMANCE_INSIGHTS
├── 📄 .dockerignore
├── 📄 .gitattributes
├── 📄 .gitignore
├── 📁 .streamlit
│   ├── 📄 config.toml
│   ├── 📄 pages.toml
│   ├── 📄 pages_ldp.toml
├── 📄 Dockerfile
├── 📁 EM_MODULE
│   ├── 📄 __init__.py
│   ├── 📄 config.py
│   ├── 📄 module_delete.py
│   ├── 📄 module_expand.py
│   ├── 📄 module_explaination.py
│   ├── 📄 module_insert.py
│   ├── 📄 module_login.py
│   ├── 📄 module_todo.py
│   ├── 📄 module_users.py
│   ├── 📄 module_view.py
├── 📁 LDP_MODULE
│   ├── 📄 __init__.py
│   ├── 📄 ldp_board.py
│   ├── 📄 ldp_delete.py
│   ├── 📄 ldp_insert.py
│   ├── 📄 ldp_view.py
├── 📄 Procfile
├── 📄 README.md
├── 📄 backup_mysql.py
├── 📁 data
│   ├── 📁 form_data
│   │   ├── 📄 form_kehoach_theonam.xlsx
│   │   ├── 📄 form_kehoach_theothang.xlsx
│   │   ├── 📄 form_thuchien_theonam.xlsx
│   │   ├── 📄 form_thuchien_theothang.xlsx
├── 📁 documentation
│   ├── 📄 __init__.py
│   ├── 📁 insert_data
│   ├── 📄 module_documentation.py
│   ├── 📁 view_app
├── 📄 main.py
├── 📁 pages_ldp
│   ├── 📄 board.py
│   ├── 📄 delete_ldp.py
│   ├── 📄 insert_ldp.py
│   ├── 📄 view_ldp.py
├── 📁 pages_view
│   ├── 📄 delete.py
│   ├── 📄 expand.py
│   ├── 📄 explaination.py
│   ├── 📄 home.py
│   ├── 📄 insert.py
│   ├── 📄 todo_check.py
│   ├── 📄 users.py
│   ├── 📄 view.py
├── 📄 pyproject.toml
├── 📁 references
│   ├── 📄 file_mau_app_vnpt.py
├── 📁 reports
│   ├── 📄 Tài liệu hướng dẫn sử dụng PIS.docx
│   ├── 📄 main_report.ipynb
├── 📄 requirements.txt
├── 📁 src
│   ├── 📁 for_style
│   ├── 📁 image_ex
│   ├── 📁 style_ldp

```
<h2 align="left">📌 5. Kết quả đạt được:</h2>

#### 2.1 Về mặt giao diện:
- Giao diện chung:
    + Đăng nhập.
    + Giới thiệu.
    + Cài đặt người dùng.
    + Hướng dẫn sử dụng.
    + Thêm dữ liệu và xóa dữ liệu kế hoạch.
    + Quản lý dịch vụ.
    + Biểu mẫu.
- Giao diện cho cấp độ nhân viên
    + Quản lý công việc
        + Dashboard thể hiện tasks(theo line).
        + Trang công việc của tôi (Thêm sửa xóa task).
    + Xem dữ liệu:
        + Dạng bảng (Theo nhân viên hoặc theo dịch vụ).
        + Dạng dashboard (Theo nhân viên hoặc theo dịch vụ).
    + Quản lý dữ liệu:
        + Thêm dữ liệu kế hoạch
    + Giải trình (So sánh thực hiện với kế hoạch).
    + Quản lý tài khoản (Giám đốc Line).
    + Giao diện thống kê người dùng
- Giao diện cho cấp độ quản lý:
    + Dashboard doanh thu theo đơn vị.
    + Xem dữ liệu dạng bảng:
        + Theo tháng
        + Tổng hợp (theo năm).
    + Quản lý dữ liệu:
        + Thêm dữ liệu kế hoạch cho các line.
        + Thêm dữ liệu thực hiện được lấy từ csdl.
    + Xóa dữ liệu kế hoạch và thực hiện của các line.
#### 2.2 Về mặt tính năng:
✅ Tạo tài khoản người dùng, quản lý người dùng, phân quyền người dùng theo Line và vai trò.<br>
✅ Tự động hóa xử lý dữ liệu, biến đổi và thêm vào csdl.<br>
✅ Tạo báo cáo Excel và báo cáo dạng dashboard (có thể tải về dạng excel).<br>
✅ Quản lý dữ liệu doanh thu theo line và theo tháng.<br>
✅ Quản lý dịch vụ (linh hoạt trong hoạt động của công ty).<br>
✅ Quản lý giải trình và cung cấp giao diện dashboard để check hiệu quả công việc.<br>
✅ Quản lý công việc, thêm task theo dịch vụ và ngày tháng.<br>
✅ Hệ thống biểu mẫu và tài liệu hướng dẫn.<br>
✅ Cài đặt người dùng.<br>

<h2 align="left">📄 6. Giao diện 🖥📱</h2>
<table>
  <tr>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_login.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_login.png" width="250" alt="page_login"><div>Login</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_gioithieu.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_gioithieu.png" width="250" alt="page_gioithieu"><div>Giới thiệu</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_quanlicongviec.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_quanlicongviec.png" width="250" alt="page_dashboard_quanlicongviec"><div>Quản lý công việc</div></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_congvieccuatoi.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_congvieccuatoi.png" width="250" alt="page_congvieccuatoi"><div>Công việc của tôi</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_xem_nhanvien.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_xem_nhanvien.png" width="250" alt="page_dashboard_xem_nhanvien"><div>Dashboard nhân viên</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_xem_dichvu.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_xem_dichvu.png" width="250" alt="page_dashboard_xem_dichvu"><div>Dashboard dịch vụ</div></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_table_xem_nhanvien.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_table_xem_nhanvien.png" width="250" alt="page_table_xem_nhanvien"><div>Dạng bảng nhân viên</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_table_xem_dichvu.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_table_xem_dichvu.png" width="250" alt="page_table_xem_dichvu"><div>Dạng bảng dịch vụ</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_themdulieu_kehoach.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_themdulieu_kehoach.png" width="250" alt="page_themdulieu_kehoach"><div>Thêm kế hoạch</div></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_themdulieu_thuchien.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_themdulieu_thuchien.png" width="250" alt="page_themdulieu_thuchien"><div>Thêm thực hiện</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_xoadulieu.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_xoadulieu.png" width="250" alt="page_xoadulieu"><div>Xóa kế hoạch</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_xoadulieu_thuchien.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_xoadulieu_thuchien.png" width="250" alt="page_xoadulieu_thuchien"><div>Xóa thực hiện</div></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_quanlidichvu.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_quanlidichvu.png" width="250" alt="page_quanlidichvu"><div>Quản lý dịch vụ</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_bieumau.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_bieumau.png" width="250" alt="page_bieumau"><div>Biểu mẫu</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_giaitrinh.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_giaitrinh.png" width="250" alt="page_dashboard_giaitrinh"><div>Dashboard giải trình</div></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_quanligiaitrinh.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_quanligiaitrinh.png" width="250" alt="page_quanligiaitrinh"><div>Quản lý giải trình</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_quanlinguoidung.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_quanlinguoidung.png" width="250" alt="page_quanlinguoidung"><div>Quản lý người dùng</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_tailieuhuongdan.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_tailieuhuongdan.png" width="250" alt="page_tailieuhuongdan"><div>Tài liệu hướng dẫn</div></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_nguoidung.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_nguoidung.png" width="250" alt="page_dashboard_nguoidung"><div>Dashboard người dùng</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_doimatkhau.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_doimatkhau.png" width="250" alt="page_doimatkhau"><div>Đổi mật khẩu</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_hienthi.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_hienthi.png" width="250" alt="page_hienthi"><div>Cài đặt hiển thị</div></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_hanhdongnguoidung.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_hanhdongnguoidung.png" width="250" alt="page_hanhdongnguoidung"><div>Hành động người dùng</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_capdonvi.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_capdonvi.png" width="250" alt="page_dashboard_capdonvi"><div>Dashboard cấp đơn vị</div></a></td>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_table_capdonvi_theothang.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_table_capdonvi_theothang.png" width="250" alt="page_table_capdonvi_theothang"><div>Dạng bảng theo tháng (cấp đơn vị)</div></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_table_capdonvi_tonghop.png" target="_blank"><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_table_capdonvi_tonghop.png" width="250" alt="page_table_capdonvi_tonghop"><div>Dạng bảng tổng hợp (cấp đơn vị)</div></a></td>
  </tr>
</table>

<h2 align="left">🎬 7. Sử dụng </h2>
<p align="center">
  <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ" target="_blank">
    <img src="https://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg" alt="Video Hướng Dẫn" width="400">
  </a>
</p>

<h2 align="left">📊 7. Các mục dashboard chính </h2>

### 1. Theo nhân viên (sẽ có các option chọn nhân viên, chọn tháng, line (tổ) lấy theo nhân viên,  chọn năm, chọn loại doanh thu, Chọn tháng (multiple select mặc định là tháng 1))
- Metric 1 : Tổng doanh thu thực hiện tháng (cộng dồn theo multiple select)
- Metric 2 : Tổng số kế hoạch tháng hiện tại (cộng dồn theo multiple select)
- Metric 3: Số lượng dịch vụ có doanh thu (cộng dồn theo multiple select)
- Biểu đồ treemap: Hiển thị thành phần doanh thu của các dịch vụ đã thực hiện (cộng dồn theo multiple select)
- Process colunm: thể hiện tiến độ hoàn thành của thực hiện với kế hoạch theo từng dịch vụ (cộng dồn theo multiple select)
- Biểu đồ tròn : Thể hiện tổng doanh thu(doanhthu) của nhân viên này với các nhân viên khác trong cùng 1 line (tổ) (cộng dồn theo multiple select)
- Biểu đồ donut: thể hiện tỉ lệ hoàn thành tổng thể (thực hiện so với kế hoạch)(cộng dồn theo multiple select)
- Biểu đồ cột chồng : thể hiện số thực hiện của nhân viên đó theo tất cả các dịch vụ đến tháng hiện tại.
- Biểu đồ đường : số thực hiện của tất cả dịch vụ đén tháng hiện tại.
### 2. Theo dịch vụ (sẽ có các option chọn dịch vụ, chọn tháng, chọn năm, chọn loại doanh thu, Chọn tháng (multiple select mặc định là tháng 1))
- Metric 1 : Tổng doanh thu thực hiện (tổng của dịch vụ đó trong tổ(line)) (cộng dồn theo multiple select)
- Metric 2 : Tổng số kế hoạch  (tổng của dịch vụ đó trong tổ(line)) (cộng dồn theo multiple select)
- Biểu đồ đường : thể hiện số thực hiện của dịch vụ đó đến tháng hiện tại
- Biểu đồ cột chồng : Thể hiện sự đóng góp của nhân viên trong dịch vụ đó( cộng dồn theo multiple select)
- Biểu đồ donut: thể hiện tỉ lệ hoàn thành (thực hiện so với kế hoạch) của dịch vụ đó (cộng dồn theo multiple select)
    
### 3. Dashboard thể hiện tình hình công việc, so sánh tỉ lệ hoàn thành và so sánh giữa các nhân viên(sẽ có các option lựa chọn năm, tháng, loại doanh thu, chọn nhân viên. Đối với lịch công việc có các chế độ xem theo tuần, tháng, danh sách và option chọn theo dịch vụ)
- Metric: Tổng số công việc hoàn thành, chưa hoàn thành và đang chờ.
- Metric: Tổng doanh thu kế hoạch, tổng doanh thu thực hiện.
- Donut chart: Tỉ lệ hoàn thành (%)
- Bảng tỉ lệ hoàn thành theo dịch vụ.
- Bảng danh sách công việc.
- Lịch công việc với các chế độ.
### 4. Dashboard giải trình bao gồm việc so sánh số liệu thực thu và số liệu nhập (Option chọn năm, chọn tháng, chọn loại doanh thu, chọn nhân viên):
- Barchart: So sánh số liệu kế toán và thực nhập.
- Piechart: Tỉ lệ thực nhập tổng thể.
- Bảng thể hiện so sánh thực nhập và kế toán theo nhân viên.
- Metric: Số dịch vụ chênh lệch, Số dịch vụ chưa hoàn thành, tổng số chênh lệch, Tổng số chưa hoàn thành.
### 5. Dashboard cấp quản lý thể hiện doanh thu theo đơn vị (Cross filter theo line và tháng):
- LineChart: Doanh thu theo tháng trong năm.
- PieChart: Tỉ lệ doanh thu của các line trong đơn vị.
- Bảng tỉ lệ hoàn thành theo dịch vụ.
- Metric: Doanh thu năm hiện hữu, phát triển mới. Tỉ lệ doanh thu hiện hữu, phát triển mới.


<h2 align="left">📋 8. Các mục bảng báo cáo (xuất excel) </h2> 

### 1. Theo Line:
- Gồm 2 loại báo cáo là theo nhân viên và theo dịch vụ:
    - Bảng kết quả phân tích so sánh với kỳ trước, thực hiện tháng trước,tỉ lệ thực hiện,... 
    - Bảng số thực hiện các tháng.
    - Bảng số kế hoạch các tháng.
### 2. Theo đơn vị:
- Báo cáo theo tháng:
    + Bảng kết quả phân tích so sánh với kỳ trước, thực hiện tháng trước,tỉ lệ thực hiện,... 
    + Bảng số thực hiện các tháng.
    + Bảng số kế hoạch các tháng.
- Báo cáo tổng hợp:
    - Tỉ lệ kế hoạch và thực hiện có lũy kế.
    - Thực hiện lũy kế.
    - Kế hoạch lũy kế.

 
<h2 align="left"> 🚀 9. Danh Sách Những Tính Năng Cần Phát Triển Tiếp Theo</h2>
📌 Tính Năng Đang Chờ Phát Triển

- 🔜 Tính năng 1: Cải thiện hiệu suất xử lý dữ liệu
  - Tối ưu hóa thuật toán xử lý dữ liệu để giảm thời gian chạy.
  - Xây dựng cơ chế caching nhằm tăng tốc độ phản hồi của API.
  - Kiểm tra và so sánh hiệu suất giữa các phương pháp xử lý.
- 🔜 Tính năng 2: Tích hợp xác thực OAuth 2.0
  - Hỗ trợ đăng nhập bằng Google, Facebook, GitHub.
  - Lưu trữ thông tin token một cách an toàn.
  - Cấu hình JWT để bảo vệ API.
- 🔜 Tính năng 3: Hệ thống thông báo real-time
  - Sử dụng WebSocket hoặc Firebase Cloud Messaging để gửi thông báo.
  - Hỗ trợ thông báo trên trình duyệt và ứng dụng di động.
  - Tạo trung tâm thông báo giúp người dùng dễ dàng quản lý.

<h2 align="left"> 💡 10. Đề Xuất Tính Năng Mới </h2>

Nếu bạn có ý tưởng hoặc đề xuất tính năng mới, vui lòng mở một Issue tại đây và mô tả chi tiết. 🤝  

Chúng tôi rất mong nhận được sự đóng góp từ bạn! 🚀  

📩 **Liên hệ**:  
- 📧 Email: [2156210125@hcmussh.edu.vn](mailto:2156210125@hcmussh.edu.vn)  
- 🔗 LinkedIn: [linkedin.com/in/hoang-xuan-quoc-0a3448293](https://www.linkedin.com/in/hoang-xuan-quoc-0a3448293)  
- 👤 Người thực hiện: **Hoàng Xuân Quốc**
- 📍🗺️ Ho Chi Minh - Viet Nam
