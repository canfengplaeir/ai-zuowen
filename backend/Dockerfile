# 使用 Python 3.11 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=manage.py \
    FLASK_ENV=production \
    TZ=Asia/Shanghai \
    PIP_NO_CACHE_DIR=1

# 配置apt镜像源为阿里云镜像
RUN echo \
    deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib \
    deb https://mirrors.aliyun.com/debian-security/ bullseye-security main \
    deb https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib \
    deb https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib \
    > /etc/apt/sources.list

# 只复制必要的文件来安装依赖
COPY requirements.txt .

# 安装系统依赖和Python依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        netcat-traditional \
        curl \
    && rm -rf /var/lib/apt/lists/* \
    # 使用阿里云的 PyPI 镜像
    && pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y gcc python3-dev \
    && apt-get autoremove -y

# 复制项目文件
COPY . .

# 创建必要的目录并设置权限
RUN mkdir -p /app/database /app/uploads /app/logs \
    && chmod +x /app/entrypoint.sh \
    && chown -R nobody:nogroup /app/database /app/uploads /app/logs

# 切换到非 root 用户
USER nobody

# 暴露端口
EXPOSE 5000

# 设置启动命令
ENTRYPOINT ["/app/entrypoint.sh"] 