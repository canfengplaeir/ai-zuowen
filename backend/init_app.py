import os
import logging
from app import create_app
from app.models import db, User
from app.utils.auth import AuthService
from config import Config
from app.utils.env_manager import env_manager


def ensure_directories_exist():
    """确保必要的目录存在"""
    directories = [
        Config.DATABASE_DIR,
        Config.UPLOAD_FOLDER,
        Config.LOG_FOLDER,
    ]

    for directory in directories:
        if os.path.exists(directory):
            print(f"目录已存在: {directory}")
        else:
            os.makedirs(directory)
            print(f"创建目录: {directory}")
        # 设置目录权限
        os.chmod(directory, 0o777)


def init_application():
    """统一的应用初始化函数"""
    print("开始初始化应用...")

    # 配置日志级别
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    # 1. 检查环境变量
    required_vars = ["SECRET_KEY", "OPENAI_API_KEY", "OPENAI_BASE_URL"]
    missing_vars = [var for var in required_vars if not env_manager.get(var)]
    if missing_vars:
        print(f"错误: 环境变量未正确配置。缺少: {', '.join(missing_vars)}")
        return False

    # 2. 创建必要的目录
    try:
        ensure_directories_exist()
    except Exception as e:
        print(f"创建目录失败: {str(e)}")
        return False

    # 3. 创建应用实例
    app = create_app()

    with app.app_context():
        try:
            # 4. 检查数据库文件是否存在
            db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
            db_exists = os.path.exists(db_path)

            if not db_exists:
                # 5. 创建数据库表
                print("创建数据库表...")
                db.create_all()

                # 6. 创建管理员账号
                if not User.query.filter_by(username="admin").first():
                    print("创建管理员账号...")
                    auth_service = AuthService(app.config["SECRET_KEY"])
                    admin_password = auth_service.hash_password("admin123")

                    # 确保密码是字符串类型
                    if isinstance(admin_password, bytes):
                        admin_password = admin_password.decode("utf-8")

                    admin = User(
                        username="admin",
                        password=admin_password,  # 现在是字符串类型
                        is_admin=True,
                    )

                    db.session.add(admin)
                    db.session.commit()
                    print("管理员账号创建成功")
            else:
                print("检测到已存在的数据库，跳过初始化步骤。")

            print("应用初始化完成！")
            return True

        except Exception as e:
            print(f"初始化过程中出错: {str(e)}")
            return False


if __name__ == "__main__":
    init_application()
