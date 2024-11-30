import multiprocessing
import os

# 获取CPU核心数
workers = multiprocessing.cpu_count() * 2 + 1

# 绑定地址
bind = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '5000')}"

# 工作模式
worker_class = "sync"

# 最大请求数
max_requests = 1000
max_requests_jitter = 50

# 超时时间
timeout = 120

# 日志配置
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = os.getenv("LOG_LEVEL", "warning").lower()

# 进程名称
proc_name = "essay_correction_app"

# 守护进程
daemon = False

# 优雅重启
graceful_timeout = 30
