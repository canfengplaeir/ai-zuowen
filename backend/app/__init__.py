from flask import Flask
from flask_cors import CORS
from .models import db
from .routes import bp as main_bp
from .routes.auth import bp as auth_bp
from .routes.essay import bp as essay_bp


def create_app(config_name="default"):
    app = Flask(__name__)

    # 配置加载
    from config import config

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化扩展
    CORS(app)
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(main_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(essay_bp, url_prefix="/api/essay")

    return app
