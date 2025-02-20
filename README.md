# VNPT_Performance_Insights
 member:
 hihahiaha
 33333

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

This project provided application support for decision making and management data

## Idea cho app VNPT Performance Insights
    1. Yêu cầu và kết quả đạt được
    - Yêu cầu: 
        + Cung cấp hỗ trợ ứng dụng cho việc ra quyết định và quản lý dữ liệu
        + Cung cấp các báo cáo và biểu đồ để hỗ trợ quản lý
        + Dựa vào dữ liệu nhân viên để tạo ra các biểu đồ
        + Từng nhân viên sẽ được đánh giá dựa trên dịch vụ, line, và doanh thu theo thời gian.
    - Kết quả đạt được:
        + Giao diện đăng nhập
        + Giao diện tạo báo cáo
        + Giao diện thêm dữ liệu
        + Giao diện xóa báo cáo
        + Giao diện quản lý users (cho admin)
        + Giao diện mở rộng (admin)
        + Giao diện chỉnh sửa thông tin (logo, title, contact, ...)
    2. Chi tiết giao diện
    - Giao diện đăng nhập
        + Form đăng nhập (username, password,check robot)
        + Button đăng nhập 
    - Giao diện tạo báo cáo theo dịch vụ
        + Form tạo báo cáo
            + Chọn dịch vụ
            + Chọn line
            + Chọn nhân viên
            + Chọn thời gian(tháng, năm)
            + button xem 
        + Button tạo báo cáo
    - Giao diện báo cáo theo nhân viên (2 loại biểu đồ, 1 là biểu đồ tròn tất cả dịch vụ trong doanh thu, 2 là tổng doanh thu so với line)
        + Form báo cáo
            + Chọn nhân viên
            + Chọn loại thời gian (theo tháng, theo năm)
            + Chọn thời gian(tháng, năm)
            + button xem
    - Giao diện thêm dữ liệu
        + Form thêm dữ liệu
        + Button thêm dữ liệu
    - Giao diện xóa báo cáo
        + Form xóa báo cáo
        + Button xóa báo cáo
    - Giao diện quản lý users
        + Form quản lý users
        + Button quản lý users
    - Giao diện chỉnh sửa thông tin
        + Form chỉnh sửa thông tin
        + Button chỉnh sửa thông tin
## Các mục dashboard chính
    1. Theo nhân viên (sẽ có các option chọn nhân viên, chọn tháng, line (tổ) lấy theo nhân viên,  chọn năm, chọn loại doanh thu, Chọn tháng (multiple select mặc định là tháng 1))
    - Metric 1 : Tổng doanh thu thực hiện tháng (cộng dồn theo multiple select)
    - Metric 2 : Tổng số kế hoạch tháng hiện tại (cộng dồn theo multiple select)
    - Metric 3: Số lượng dịch vụ có doanh thu (cộng dồn theo multiple select)
    - Biểu đồ treemap: Hiển thị thành phần doanh thu của các dịch vụ đã thực hiện (cộng dồn theo multiple select)
    - Process colunm: thể hiện tiến độ hoàn thành của thực hiện với kế hoạch theo từng dịch vụ (cộng dồn theo multiple select)
    - Biểu đồ tròn : Thể hiện tổng doanh thu(doanhthu) của nhân viên này với các nhân viên khác trong cùng 1 line (tổ) (cộng dồn theo multiple select)
    - Biểu đồ donut: thể hiện tỉ lệ hoàn thành tổng thể (thực hiện so với kế hoạch)(cộng dồn theo multiple select)
    - Biểu đồ cột chồng : thể hiện số thực hiện của nhân viên đó theo tất cả các dịch vụ đến tháng hiện tại.
    - Biểu đồ đường : số thực hiện của tất cả dịch vụ đén tháng hiện tại.
    2. Theo dịch vụ (sẽ có các option chọn dịch vụ, chọn tháng, chọn năm, chọn loại doanh thu, Chọn tháng (multiple select mặc định là tháng 1))
    - Metric 1 : Tổng doanh thu thực hiện (tổng của dịch vụ đó trong tổ(line)) (cộng dồn theo multiple select)
    - Metric 2 : Tổng số kế hoạch  (tổng của dịch vụ đó trong tổ(line)) (cộng dồn theo multiple select)
    - Biểu đồ đường : thể hiện số thực hiện của dịch vụ đó đến tháng hiện tại
    - Biểu đồ cột chồng : Thể hiện sự đóng góp của nhân viên trong dịch vụ đó( cộng dồn theo multiple select)
    - Biểu đồ donut: thể hiện tỉ lệ hoàn thành (thực hiện so với kế hoạch) của dịch vụ đó (cộng dồn theo multiple select)
    
## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         vnpt_performance_insights and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── vnpt_performance_insights   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes vnpt_performance_insights a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

