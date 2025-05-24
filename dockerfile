# Sử dụng image python slim
FROM python:3.11-slim

# Set environment variables để không tạo bytecode và đảm bảo log không bị buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Chỉ định thư mục làm việc trong container
WORKDIR /app

# Copy requirements.txt vào container
COPY requirements.txt .

# Cài đặt các package cần thiết cho việc biên dịch và cài đặt MySQL client
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libmariadb-dev \ 
    pkg-config \
    && rm -rf /var/lib/apt/lists/* 

# Cập nhật pip lên phiên bản mới nhất
RUN pip install --upgrade pip

# Cài đặt các thư viện trong requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào thư mục làm việc
COPY . .

# Chạy ứng dụng Django với server phát triển (chạy ở cổng 8000)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
