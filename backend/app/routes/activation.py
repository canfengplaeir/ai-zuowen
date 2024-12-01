from flask import Blueprint, request, jsonify, g
from ..models import ActivationCode, User, db
from ..utils.auth import login_required, admin_required
import random
import string
from datetime import datetime

bp = Blueprint("activation", __name__)


def generate_code(length=16):
    """生成随机激活码"""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


@bp.route("/generate", methods=["POST"])
@admin_required
def generate_activation_code():
    """生成激活码（管理员）"""
    data = request.get_json()
    count = data.get("count", 1)  # 生成数量
    correction_count = data.get("correction_count", 10)  # 每个激活码对应的批改次数

    codes = []
    for _ in range(count):
        code = generate_code()
        activation_code = ActivationCode(
            code=code, correction_count=correction_count, created_by=g.user.id
        )
        db.session.add(activation_code)
        codes.append(code)

    try:
        db.session.commit()
        return jsonify({"message": f"成功生成 {count} 个激活码", "codes": codes})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bp.route("/activate", methods=["POST"])
@login_required
def activate_code():
    """使用激活码"""
    data = request.get_json()
    code = data.get("code")

    if not code:
        return jsonify({"error": "请输入激活码"}), 400

    activation_code = ActivationCode.query.filter_by(code=code, is_used=False).first()
    if not activation_code:
        return jsonify({"error": "无效的激活码"}), 400

    try:
        # 更新激活码状态
        activation_code.is_used = True
        activation_code.used_by = g.user.id
        activation_code.used_at = datetime.utcnow()

        # 增加用户的剩余批改次数
        g.user.remaining_corrections += activation_code.correction_count

        db.session.commit()
        return jsonify(
            {
                "message": "激活成功",
                "correction_count": activation_code.correction_count,
                "remaining_corrections": g.user.remaining_corrections,
            }
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bp.route("/list", methods=["GET"])
@admin_required
def list_codes():
    """获取激活码列表（管理员）"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    query = ActivationCode.query.order_by(ActivationCode.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page)

    codes = []
    for code in pagination.items:
        code_dict = code.to_dict()
        # 添加用户信息
        if code.used_by:
            user = User.query.get(code.used_by)
            code_dict["used_by_username"] = user.username if user else None
        codes.append(code_dict)

    return jsonify(
        {
            "codes": codes,
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page,
        }
    )


@bp.route("/<int:code_id>", methods=["DELETE"])
@admin_required
def delete_code(code_id):
    """删除激活码（管理员）"""
    code = ActivationCode.query.get_or_404(code_id)

    if code.is_used:
        return jsonify({"error": "已使用的激活码不能删除"}), 400

    try:
        db.session.delete(code)
        db.session.commit()
        return jsonify({"message": "删除成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
