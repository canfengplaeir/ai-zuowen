# 使用 Python 3.11 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=manage.py \
    TZ=Asia/Shanghai \
    PIP_NO_CACHE_DIR=1

# ... 其余配置保持不变 ... 