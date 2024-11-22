from app import create_app
from app.models import db, User
from app.utils.auth import AuthService
import os

def init_database():
    app = create_app()
    
    with app.app_context():
        # 确保数据库目录存在
        os.makedirs(os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')), exist_ok=True)
        
        # 创建所有表
        db.create_all()
        
        # 创建管理员账号
        try:
            # 检查管理员是否已存在
            if not User.query.filter_by(username='admin').first():
                auth_service = AuthService(app.config['SECRET_KEY'])
                admin_password = auth_service.hash_password('admin123')
                
                admin = User(
                    username='admin',
                    password=admin_password,
                    is_admin=True
                )
                
                db.session.add(admin)
                db.session.commit()
                print("管理员账号创建成功")
            else:
                print("管理员账号已存在")
        except Exception as e:
            print(f"创建管理员账号失败: {e}")

if __name__ == '__main__':
    init_database() 