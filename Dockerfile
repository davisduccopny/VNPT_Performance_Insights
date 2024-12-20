# Sử dụng Python image làm base
FROM python:3.11.5

# Đặt thư mục làm việc cho ứng dụng
WORKDIR /app

# Sao chép các file vào container
COPY . .

# Cài đặt các yêu cầu
RUN pip install --no-cache-dir -r requirements.txt

# Đặt cổng cho ứng dụng (Streamlit mặc định là 8501)
EXPOSE 8501

# Chạy Streamlit
CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
