<!-- CÁC PAINPOINT CẦN GIẢI QUYẾT ĐỐI VỚI APP -->
1. Các trưởng line thường có xuất phát điểm thấp về công nghệ 
    - Cần phải tối ưu quá trình nhập ( với các trường dữ liệu rõ ràng)
2. Các điểm mà ứng dụng chú ý :
    - Người nhập kế hoạch là các trưởng line hoặc người được phân quyền từ manage trở lên 
    - Ứng dụng đưa ra được việc đánh giá người dùng thông qua việc nhập trực tiếp số liệu
        + Những người không đủ kpi thì hiển thị thông báo hoặc làm nổi bật.
        + Đưa ra so sánh dữ liệu được kế toán nhập và dữ liệu nhân viên nhập, nếu có sự chênh lệch thì thông báo.
    - Giới hạn thời gian nhập vào một thời gian cụ thể trong tuần hoặc tháng.
    - Tăng cường khả năng thao tác trên dashboard, đặc biệt là bộ lọc.
3. Hướng giải quyết:
    - Sửa lại cấu trúc nhập:
        + Nhập bằng file excel
        + Nhập bằng form
    - Phát triển chức năng update dữ liệu trực tiếp bằng việc load dữ liệu vào form rồi hiển thị lên ui.
    - Xây dashboard đối với level Line ==> Xem kpi của trưởng line nhập và số nhập của nhân viên.
    - Xây dashboard đối với level manage ==> số thực hiện của nhân viên nhập và số load từ csdl vnpt.
    - Phát triển recorder to text để nhân viên nhập giải trình.
    - Hiệu ứng và thông báo ở trang chủ, gửi thông báo đến email hoặc điện thoại với kpi.

4. Cấu trúc:
    - Trang chủ
    - Trang công việc cho nhân viên:
        + Trang xem tổng quan trong line.
        + Trang cá nhân (để nhập số liệu và xem cá nhân).
        + Trang thông báo và giải trình (Không truy cập được)
    - Trang công việc cho trưởng line:
        + Trang xem tổng quan trong line.
        + Trang cá nhân (để nhập số liệu và xem cá nhân).
        + Trang thông báo và giải trình (truy cập được) - so sánh với số liệu của kế toán
    - Trang xem chi tiết
    - Trang quản lý (Nhập và xóa)
    - Trang cá nhân
    - Trang mở rộng:
        + Quản lý nhân sự.
        + Documentation.