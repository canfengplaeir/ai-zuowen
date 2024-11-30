from flask import Blueprint

bp = Blueprint("api", __name__)

from . import auth, essay

bp.register_blueprint(essay.bp, url_prefix="/essay")
