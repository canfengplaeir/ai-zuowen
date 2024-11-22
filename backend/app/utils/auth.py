from functools import wraps
from flask import request, jsonify
import jwt
import bcrypt
import os
from datetime import datetime, timedelta

class AuthService:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def hash_password(self, password):
        """对密码进行加密"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def check_password(self, password, hashed):
        """验证密码"""
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    def generate_token(self, user_id):
        """生成JWT令牌"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def verify_token(self, token):
        """验证JWT令牌"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

def login_required(f):
    """验证登录状态的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': '未登录'}), 401
        
        auth_service = AuthService(os.getenv('SECRET_KEY'))
        user_id = auth_service.verify_token(token.split(' ')[1])
        if not user_id:
            return jsonify({'error': '登录已过期'}), 401
            
        return f(*args, **kwargs)
    return decorated_function 