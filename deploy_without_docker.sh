#!/bin/bash

# 确保脚本在出错时停止执行
set -e

# 检查环境文件是否存在
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    exit 1
fi

echo "Step 1: Creating directories..."
# 创建必要的目录
mkdir -p database uploads logs
chmod 777 database uploads logs

echo "Step 2: Installing backend dependencies..."
cd backend
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip install -r requirements.txt

echo "Step 3: Initializing database..."
python init_db.py

echo "Step 4: Starting backend service..."
# 使用 gunicorn 启动后端服务
nohup gunicorn --bind 0.0.0.0:5000 --workers 4 --threads 2 --timeout 120 "app:create_app()" > ../logs/backend.log 2>&1 &

echo "Step 5: Installing frontend dependencies..."
cd ../frontend
# 使用淘宝镜像源安装依赖
npm config set registry https://registry.npmmirror.com
npm install

echo "Step 6: Building frontend..."
npm run build

echo "Step 7: Setting up Nginx..."
# 安装 Nginx（根据系统选择合适的命令）
if [ -f /etc/debian_version ]; then
    sudo apt-get update
    sudo apt-get install -y nginx
elif [ -f /etc/redhat-release ]; then
    sudo yum install -y nginx
fi

# 配置 Nginx
sudo cp nginx.conf /etc/nginx/conf.d/essay-correction.conf
sudo nginx -t && sudo systemctl restart nginx

echo "Deployment completed!"
echo "Backend logs are available in logs/backend.log" 