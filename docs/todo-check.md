### YÊU CẦU DỰ ÁN
1. Triển khai ứng dụng quản lý công việc gồm các bộ phận sau:
    a. Các bộ phận
 - Gồm các dịch vụ
 - Các thành viên trong một tổ.
 - Các công việc thực hiện trong ngày/tuần/tháng.
    b. Các giao diện mong muốn:
 - Giao diện chính(khi mở trang): Hiển thị các công việc theo chế độ xem nhất định (xem theo ngày/tháng hoặc xem theo dịch vụ hoặc xem theo trạng thái công việc). Khi người dùng click vào công việc thì hiển thị một form giúp chỉnh sửa thông tin công việc đó.
 - Giao diện thêm công việc
 - Giao diện bảng: (có trường chọn thời gian)Hiển thị danh sách tất cả công việc bao gồm các cột (dịch vụ, nhân viên phụ trách, doanh thu gói, lũy kế, ghi chú). Phía dưới bảng sẽ ghi ra tổng doanh thu của tất cả các dịch vụ trong thời gian đã chọn

2. Quy trình
 - Người dùng truy cập vào ứng dụng
 - Lựa chọn chế độ xem (xem theo ngày tháng hoặc xem theo dịch vụ hoặc xem theo trạng thái công việc)
 - Tiếp theo người dùng có thể thêm một công việc mới trong đó:
    + Có trường lựa chọn dịch vụ
    + Có trường chọn status
    + Có input nhập doanh thu gói(của dịch vụ đó).
    + Có trường chọn ngày bắt đầu và ngày kết thúc.
    + Có trường nhập ghi chú.
- Sau khi thêm công việc, người dùng có thể xem lại công việc đó và chỉnh sửa thông tin công việc đó.
3. Lưu trữ dữ liệu : mysql
