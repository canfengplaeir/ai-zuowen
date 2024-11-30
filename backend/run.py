import multiprocessing
import os
import sys
import platform
import logging
from typing import Dict, Any
from app import create_app
from init_app import init_application
from app.utils.env_manager import env_manager


def run_with_waitress(app: Any, host: str, port: int) -> None:
    """使用 Waitress 运行生产环境 (Windows)"""
    try:
        from waitress import serve

        # 配置日志
        logger = logging.getLogger("waitress")
        logger.setLevel(logging.INFO)

        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 设置日志格式
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        print(f"使用 Waitress 启动生产环境... http://{host}:{port}")
        serve(
            app,
            host=host,
            port=port,
            threads=multiprocessing.cpu_count() * 2,
            channel_timeout=120,
            cleanup_interval=30,
            max_request_body_size=1024 * 1024 * 16,  # 16MB
        )
    except ImportError:
        print("错误: Windows生产环境需要安装 waitress。请运行: pip install waitress")
        sys.exit(1)


def run_with_gunicorn(app: Any, host: str, port: int) -> None:
    """使用 Gunicorn 运行生产环境 (Linux/Unix)"""
    try:
        from gunicorn.app.base import BaseApplication

        class GunicornApp(BaseApplication):
            def __init__(self, app: Any, options: Dict[str, Any]):
                self.options = options
                self.application = app
                super().__init__()

            def load_config(self) -> None:
                for key, value in self.options.items():
                    if key in self.cfg.settings and value is not None:
                        self.cfg.set(key.lower(), value)

            def load(self) -> Any:
                return self.application

        options = {
            "bind": f"{host}:{port}",
            "workers": multiprocessing.cpu_count() * 2 + 1,
            "worker_class": "sync",
            "timeout": 120,
        }

        print(f"使用 Gunicorn 启动生产环境... http://{host}:{port}")
        GunicornApp(app, options).run()

    except ImportError:
        print("错误: Linux/Unix生产环境需要安装 gunicorn。请运行: pip install gunicorn")
        sys.exit(1)


# 获取环境配置
FLASK_ENV = env_manager.flask_env
HOST = str(env_manager.get("HOST", "0.0.0.0"))
PORT = int(env_manager.get("PORT", "5000") or "5000")

# 初始化应用
if not init_application():
    print("应用初始化失败，程序退出。")
    sys.exit(1)

# 创建应用
app = create_app(FLASK_ENV)

if __name__ == "__main__":
    if env_manager.is_production:
        if platform.system() == "Windows":
            run_with_waitress(app, HOST, PORT)
        else:
            run_with_gunicorn(app, HOST, PORT)
    else:
        print(f"使用 Flask 开发服务器启动开发环境... http://{HOST}:{PORT}")
        app.run(host=HOST, port=PORT, debug=True)
