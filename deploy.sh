#!/bin/bash

# 确保脚本在出错时停止执行
set -e

# 添加命令行参数支持
SKIP_BUILD=false
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --skip-build) SKIP_BUILD=true ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# 检查环境文件是否存在
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    exit 1
fi

echo "Step 1: Creating directories..."
# 创建必要的目录
mkdir -p database uploads logs

echo "Step 2: Setting permissions..."
# 设置目录权限
chmod 777 database uploads logs

echo "Step 3: Pulling Docker images (this may take a while)..."
# 预先拉取基础镜像
docker pull python:3.11-slim
docker pull node:18-alpine
docker pull nginx:stable-alpine

if [ "$SKIP_BUILD" = true ]; then
    echo "Skipping build phase..."
    docker-compose up -d
else
    echo "Building and starting containers..."
    docker-compose build --parallel
    docker-compose up -d
fi

echo "Step 5: Waiting for services to start..."
# 等待服务启动
sleep 10

echo "Step 6: Checking service status..."
# 检查服务状态
docker-compose ps

echo "Deployment completed successfully!" 