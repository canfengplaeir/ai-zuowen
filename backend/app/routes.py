from flask import Blueprint, jsonify

bp = Blueprint("api", __name__)


@bp.route("/health", methods=["GET"])
def health_check():
    """健康检查"""
    return jsonify({"status": "healthy"}), 200
