# 检查环境文件是否存在
if [ ! -f backend/.env ]; then
    echo "Error: backend/.env file not found!"
    exit 1
fi

echo "Step 1: Creating directories..."
# 创建必要的目录
mkdir -p backend/database backend/uploads backend/logs

echo "Step 2: Setting permissions..."
# 设置目录权限
chmod 777 backend/database backend/uploads backend/logs 