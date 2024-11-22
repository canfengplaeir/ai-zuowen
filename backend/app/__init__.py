from flask import Flask
from flask_cors import CORS
from .routes import api
from .models import db
from config import Config
import os
from dotenv import load_dotenv

# 确保环境变量加载
load_dotenv()


def create_app():
    app = Flask(__name__)

    # 配置 CORS
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "*",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
    )

    # 加载配置
    app.config.from_object(Config)

    # 确保必要的目录存在
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(
        os.path.dirname(
            app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
        ),
        exist_ok=True,
    )

    # 初始化数据库
    db.init_app(app)

    # 在应用上下文中创建所有表
    with app.app_context():
        db.create_all()

    # 注册蓝图
    app.register_blueprint(api, url_prefix="/api")

    return app
