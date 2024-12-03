from functools import wraps
from flask import request, jsonify, current_app, g
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Tuple, Callable
from ..models import User, db


class AuthService:
    def __init__(self, secret_key: str):
        self.secret_key = str(secret_key) if secret_key else "default-secret-key"

    def generate_token(self, user_id: int) -> str:
        """生成JWT令牌"""
        payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(days=1)}
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def verify_token(self, token: str) -> Optional[int]:
        """验证JWT令牌"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            raise Exception("令牌已过期")
        except jwt.InvalidTokenError:
            raise Exception("无效的令牌")

    def verify_password(self, password: str, hashed_password: bytes) -> bool:
        """验证密码"""
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
        except Exception as e:
            print(f"密码验证错误: {str(e)}")
            return False

    def hash_password(self, password: str) -> bytes:
        """对密码进行哈希处理"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)


def login_required(f: Callable) -> Callable:
    """验证登录的装饰器"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")

        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"error": "无效的认证头部"}), 401

        if not token:
            return jsonify({"error": "缺少令牌"}), 401

        try:
            auth_service = AuthService(current_app.config["SECRET_KEY"])
            user_id = auth_service.verify_token(token)
            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": "用户不存在"}), 401
            g.user = user
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        return f(*args, **kwargs)

    return decorated


def admin_required(f: Callable) -> Callable:
    """验证管理员权限的装饰器"""

    @wraps(f)
    @login_required  # 先验证登录
    def decorated(*args, **kwargs):
        if not g.user.is_admin:
            return jsonify({"error": "需要管理员权限"}), 403
        return f(*args, **kwargs)

    return decorated
