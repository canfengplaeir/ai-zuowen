from flask import Blueprint, jsonify, current_app
from ..models import User, db
from ..utils.auth import admin_required

bp = Blueprint("admin", __name__)


@bp.route("/users", methods=["GET"])
@admin_required
def get_users():
    """获取所有用户（管理员）"""
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        current_app.logger.error(f"获取用户列表失败: {str(e)}")
        return jsonify({"error": "获取用户列表失败"}), 500


@bp.route("/users/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id):
    """删除用户（管理员）"""
    try:
        user = User.query.get_or_404(user_id)

        # 不允许删除管理员
        if user.is_admin:
            return jsonify({"error": "不能删除管理员账号"}), 403

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "用户删除成功"})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除用户失败: {str(e)}")
        return jsonify({"error": "删除用户失败"}), 500
