FROM python:3.10-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt
COPY requirements.txt .

# 安装Python依赖
RUN pip install -r requirements.txt

# 复制源代码
COPY . .

# 运行程序
CMD ["python", "emotion_detector.py"]