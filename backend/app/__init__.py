from flask import Flask
from flask_cors import CORS
from .models import db
from .routes import register_blueprints


def create_app(config_name="default"):
    app = Flask(__name__)

    # 配置加载
    from config import config

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化扩展
    CORS(app)
    db.init_app(app)

    # 注册路由
    register_blueprints(app)

    return app
