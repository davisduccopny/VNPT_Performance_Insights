<h1 style="text-align:center;">VNPT Performance Insights</h1>

### 1. Yêu cầu cho công cụ:
- Convert data từ dạng excel để import vào csdl, sau đó tạo ra dạng báo cáo dữ liệu tự động.
- Cung cấp hỗ trợ ứng dụng cho việc ra quyết định và quản lý dữ liệu
- Dựa vào dữ liệu nhân viên để tạo ra các biểu đồ
- Từng nhân viên sẽ được đánh giá dựa trên dịch vụ, line, và doanh thu theo thời gian.
- Có hai cấp độ website:
    + Một cho nhân viên cấp thấp sử dụng theo từng line (tổ).
    + Hai cho lớp quản lý tầm trung.
### 2. Kết quả đạt được:
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
- Tạo tài khoản người dùng, quản lý người dùng, phân quyền người dùng theo Line và vai trò.
- Tự động hóa xử lý dữ liệu, biến đổi và thêm vào csdl.
- Tạo báo cáo Excel và báo cáo dạng dashboard (có thể tải về dạng excel).
- Quản lý dữ liệu doanh thu theo line và theo tháng.
- Quản lý dịch vụ (linh hoạt trong hoạt động của công ty).
- Quản lý giải trình và cung cấp giao diện dashboard để check hiệu quả công việc.
- Quản lý công việc, thêm task theo dịch vụ và ngày tháng.
- Hệ thống biểu mẫu và tài liệu hướng dẫn.
- Cài đặt người dùng.

## Giao diện
<table>
  <tr>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_login.png" width="250" alt="page_login"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_gioithieu.png" width="250" alt="page_gioithieu"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_quanlicongviec.png" width="250" alt="page_dashboard_quanlicongviec"></td>
  </tr>
  <tr>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_congvieccuatoi.png" width="250" alt="page_congvieccuatoi"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_xem_nhanvien.png" width="250" alt="page_dashboard_xem_nhanvien"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_xem_dichvu.png" width="250" alt="page_dashboard_xem_dichvu"></td>
  </tr>
  <tr>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_table_xem_nhanvien.png" width="250" alt="page_table_xem_nhanvien"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_table_xem_dichvu.png" width="250" alt="page_table_xem_dichvu"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_themdulieu_kehoach.png" width="250" alt="page_themdulieu_kehoach"></td>
  </tr>
  <tr>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_themdulieu_thuchien.png" width="250" alt="page_themdulieu_thuchien"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_xoadulieu.png" width="250" alt="page_xoadulieu"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_xoadulieu_thuchien.png" width="250" alt="page_xoadulieu_thuchien"></td>
  </tr>
  <tr>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_quanlidichvu.png" width="250" alt="page_quanlidichvu"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_bieumau.png" width="250" alt="page_bieumau"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_giaitrinh.png" width="250" alt="page_dashboard_giaitrinh"></td>
  </tr>
  <tr>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_quanligiaitrinh.png" width="250" alt="page_quanligiaitrinh"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_quanlinguoidung.png" width="250" alt="page_quanlinguoidung"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_tailieuhuongdan.png" width="250" alt="page_tailieuhuongdan"></td>
  </tr>
  <tr>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_nguoidung.png" width="250" alt="page_dashboard_nguoidung"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_doimatkhau.png" width="250" alt="page_doimatkhau"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_hienthi.png" width="250" alt="page_hienthi"></td>
  </tr>
  <tr>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_hanhdongnguoidung.png" width="250" alt="page_hanhdongnguoidung"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_dashboard_capdonvi.png" width="250" alt="page_dashboard_capdonvi"></td>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_table_capdonvi_theothang.png" width="250" alt="page_table_capdonvi_theothang"></td>
  </tr>
  <tr>
    <td><img src="https://davisduccopny.github.io/Image_Repo/vnpt-performance-insights/readme/page_table_capdonvi_tonghop.png" width="250" alt="page_table_capdonvi_tonghop"></td>
  </tr>
</table>



## Các mục dashboard chính
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


## Các mục bảng báo cáo (xuất excel)
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
 
