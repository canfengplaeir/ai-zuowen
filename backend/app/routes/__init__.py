from flask import Blueprint
from importlib import import_module
from pathlib import Path


def register_blueprints(app):
    """自动注册所有路由模块"""
    # 创建主蓝图
    api = Blueprint("api", __name__)

    # 获取当前目录下的所有路由模块
    routes_dir = Path(__file__).parent
    route_modules = [
        f.stem
        for f in routes_dir.glob("*.py")
        if f.is_file() and f.stem not in ["__init__"]
    ]

    # 注册每个路由模块
    for module_name in route_modules:
        module = import_module(f".{module_name}", package=__package__)
        if hasattr(module, "bp"):
            api.register_blueprint(module.bp, url_prefix=f"/{module_name}")

    # 注册主蓝图
    app.register_blueprint(api, url_prefix="/api")
