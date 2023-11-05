FROM python:alpine
# 设置工作目录
WORKDIR /app
# 复制并安装依赖项
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# 复制程序代码
COPY main.py .
# 设置环境变量和程序入口
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
