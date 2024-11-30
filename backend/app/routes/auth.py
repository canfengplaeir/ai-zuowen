from flask import Blueprint, request, jsonify, current_app, g
from ..models import User, Essay, db
from ..utils.auth import login_required, admin_required, AuthService
from datetime import datetime

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
def register():
    """用户注册"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "无效的请求数据"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "用户名已存在"}), 400

    auth_service = AuthService(current_app.config["SECRET_KEY"])
    hashed_password = auth_service.hash_password(password)

    user = User(username=username, password=hashed_password.decode("utf-8"))
    db.session.add(user)

    try:
        db.session.commit()
        return jsonify({"message": "注册成功"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bp.route("/login", methods=["POST"])
def login():
    """用户登录"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "无效的请求数据"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "用户名或密码错误"}), 401

    auth_service = AuthService(current_app.config["SECRET_KEY"])
    if not auth_service.verify_password(password, user.password.encode("utf-8")):
        return jsonify({"error": "用户名或密码错误"}), 401

    token = auth_service.generate_token(user.id)
    return jsonify(
        {
            "token": token,
            "user_id": user.id,
            "username": user.username,
            "is_admin": user.is_admin,
        }
    )


@bp.route("/user/profile", methods=["GET"])
@login_required
def get_profile():
    """获取用户个人信息"""
    user = g.user
    essay_count = Essay.query.filter_by(user_id=user.id).count()

    return jsonify(
        {
            "id": user.id,
            "username": user.username,
            "is_admin": user.is_admin,
            "essay_count": essay_count,
            "created_at": user.created_at.isoformat(),
        }
    )


@bp.route("/user/password", methods=["PUT"])
@login_required
def change_password():
    """修改密码"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "无效的请求数据"}), 400

    current_password = data.get("currentPassword")
    new_password = data.get("newPassword")

    if not current_password or not new_password:
        return jsonify({"error": "当前密码和新密码不能为空"}), 400

    user = g.user
    auth_service = AuthService(current_app.config["SECRET_KEY"])

    if not auth_service.verify_password(
        current_password, user.password.encode("utf-8")
    ):
        return jsonify({"error": "当前密码错误"}), 401

    try:
        hashed_password = auth_service.hash_password(new_password)
        user.password = hashed_password.decode("utf-8")
        db.session.commit()
        return jsonify({"message": "密码修改成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
