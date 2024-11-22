#!/bin/sh

# 确保脚本在出错时停止执行
set -e

# 创建必要的目录
python setup.py

# 初始化数据库
python init_db.py

# 启动应用
exec gunicorn --bind 0.0.0.0:5000 --workers 4 --threads 2 --timeout 120 "app:create_app()"