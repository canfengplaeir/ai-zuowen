import os
from typing import Optional, Union
from dotenv import load_dotenv


class EnvManager:
    """环境变量管理类"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._load_env()
            self._initialized = True

    def _load_env(self):
        """加载环境变量"""
        # 获取后端目录的绝对路径
        backend_dir = os.path.abspath(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        env_path = os.path.join(backend_dir, ".env")

        # 加载环境变量前先打印当前工作目录和环境文件路径
        print(f"当前工作目录: {os.getcwd()}")
        print(f"尝试加载环境文件: {env_path}")

        # 检查环境文件是否存在
        if not os.path.exists(env_path):
            raise FileNotFoundError(f"环境文件不存在: {env_path}")

        # 加载环境变量，不覆盖已存在的环境变量
        load_dotenv(env_path, override=True)

        # 打印加载后的 FLASK_ENV 值
        flask_env = os.getenv("FLASK_ENV")
        print(f"加载的 FLASK_ENV 值: {flask_env}")

    @property
    def flask_env(self) -> str:
        """获取Flask环境"""
        env = os.getenv("FLASK_ENV")
        if not env:
            print("警告: FLASK_ENV 未设置，使用默认值 'development'")
            return "development"

        valid_envs = ["development", "production", "testing"]
        if env not in valid_envs:
            print(f"警告: FLASK_ENV={env} 无效，使用默认值 'development'")
            return "development"

        print(f"使用环境: {env}")  # 添加调试输出
        return env

    @property
    def is_development(self) -> bool:
        """是否为开发环境"""
        return self.flask_env == "development"

    @property
    def is_production(self) -> bool:
        """是否为生产环境"""
        return self.flask_env == "production"

    @property
    def is_testing(self) -> bool:
        """是否为测试环境"""
        return self.flask_env == "testing"

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """获取环境变量值"""
        value = os.getenv(key, default)
        if value is None:
            return default
        return value


# 创建全局实例
env_manager = EnvManager()
