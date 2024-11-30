from flask import Blueprint, request, jsonify, current_app, send_from_directory, g
from werkzeug.utils import secure_filename
import os
from sqlalchemy import desc
from ..models import Essay, db
from ..utils.auth import login_required, admin_required
from ..utils.ai_correction import AIService
from datetime import datetime
import jwt
from ..models import User

bp = Blueprint("essay", __name__)


def get_ai_service():
    """获取 AI 服务实例"""
    return AIService(
        api_key=current_app.config["OPENAI_API_KEY"],
        base_url=current_app.config["OPENAI_BASE_URL"],
    )


@bp.route("/upload", methods=["POST"])
@login_required
def upload_essay():
    """上传并处理作文"""
    try:
        # 兼容前端的两种字段名
        file = request.files.get("file") or request.files.get("image")
        if not file:
            return jsonify({"error": "没有文件"}), 400

        if not file.filename:
            return jsonify({"error": "没有选择文件"}), 400

        # 检查文件类型
        if not allowed_file(file.filename):
            return jsonify({"error": "不支持的文件类型"}), 400

        # 保存文件
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        user_id = g.user.id
        save_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], str(user_id))
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, filename)
        file.save(file_path)

        # 使用 AI 服务处理作文
        ai_service = get_ai_service()
        content, feedback_dict, score = ai_service.process_essay(file_path)

        if not content:
            return jsonify({"error": feedback_dict}), 400

        # 保存到数据库
        essay = Essay(
            user_id=user_id,
            content=content,
            feedback=feedback_dict,
            score=score,
            original_image=filename,
        )
        db.session.add(essay)
        db.session.commit()

        return jsonify(
            {
                "content": content,
                "feedback": feedback_dict,
                "score": score,
                "essay_id": essay.id,
                "image_path": f"/api/essay/image/{user_id}/{filename}",
            }
        )

    except Exception as e:
        current_app.logger.error(f"处理作文时出错: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "服务器错误"}), 500


@bp.route("/image/<int:user_id>/<path:filename>")
@login_required
def get_image(user_id, filename):
    """获取作文图片"""
    try:
        # 检查权限
        if g.user.id != user_id and not g.user.is_admin:
            return jsonify({"error": "无权访问"}), 403

        upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], str(user_id))
        file_path = os.path.join(upload_dir, filename)

        # 检查文件是否存在
        if not os.path.exists(file_path):
            return jsonify({"error": "文件不存在"}), 404

        # 设置缓存控制
        response = send_from_directory(
            upload_dir, filename, as_attachment=False, max_age=31536000
        )
        return response

    except Exception as e:
        current_app.logger.error(f"获取图片失败: {str(e)}")
        return jsonify({"error": "获取图片失败"}), 500


@bp.route("/list/<int:user_id>")
@login_required
def get_essays(user_id):
    """获取用户的作文列表"""
    if g.user.id != user_id and not g.user.is_admin:
        return jsonify({"error": "无权访问"}), 403

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    essays_query = Essay.query.filter_by(user_id=user_id).order_by(
        desc(Essay.created_at)
    )
    pagination = essays_query.paginate(page=page, per_page=per_page)

    essays = [
        {
            **essay.to_dict(),
            "image_url": f"/api/essay/image/{user_id}/{essay.original_image}",
        }
        for essay in pagination.items
    ]

    return jsonify(
        {
            "essays": essays,
            "total": pagination.total,
            "page": page,
            "per_page": per_page,
            "total_pages": pagination.pages,
        }
    )


@bp.route("/<int:essay_id>", methods=["DELETE"])
@login_required
def delete_essay(essay_id):
    """删除作文"""
    essay = Essay.query.get_or_404(essay_id)

    if g.user.id != essay.user_id and not g.user.is_admin:
        return jsonify({"error": "无权操作"}), 403

    try:
        # 删除图片文件
        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            str(essay.user_id),
            essay.original_image,
        )
        if os.path.exists(file_path):
            os.remove(file_path)

        # 删除数据库记录
        db.session.delete(essay)
        db.session.commit()
        return jsonify({"message": "删除成功"})

    except Exception as e:
        current_app.logger.error(f"删除作文时出错: {str(e)}")
        return jsonify({"error": "删除失败"}), 500


def allowed_file(filename):
    """检查文件类型是否允许"""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )
