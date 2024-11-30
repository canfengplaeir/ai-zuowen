#!/bin/bash

# 获取环境变量
FLASK_ENV=${FLASK_ENV:-development}

# 根据环境选择启动方式
if [ "$FLASK_ENV" = "production" ]; then
    echo "使用 Gunicorn 启动生产环境..."
    exec gunicorn -c gunicorn.conf.py run:app
else
    echo "使用 Flask 开发服务器启动开发环境..."
    exec python run.py
fi 