import os

# 获取后端目录的绝对路径
BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """基础配置类"""

    # 从环境变量获取配置
    SECRET_KEY = os.getenv("SECRET_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "essay.db")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))

    # 数据库配置
    DATABASE_DIR = os.path.join(BACKEND_DIR, "database")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(DATABASE_DIR, DATABASE_NAME)}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(BACKEND_DIR, "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

    # 日志配置
    LOG_FOLDER = os.path.join(BACKEND_DIR, "logs")

    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        pass


class DevelopmentConfig(Config):
    """开发环境配置"""

    DEBUG = True
    SQLALCHEMY_ECHO = False
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """生产环境配置"""

    DEBUG = False
    LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING")


class TestingConfig(Config):
    """测试环境配置"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    LOG_LEVEL = "DEBUG"


# 环境配置映射
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
