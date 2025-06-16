FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建静态文件目录
RUN mkdir -p static

# 暴露端口
EXPOSE 8008

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008"] 