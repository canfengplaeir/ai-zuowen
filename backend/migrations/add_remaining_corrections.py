import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db
from sqlalchemy import text


def upgrade():
    """添加 remaining_corrections 字段"""
    app = create_app()
    with app.app_context():
        # 添加新字段
        with db.engine.connect() as conn:
            conn.execute(
                text(
                    "ALTER TABLE users ADD COLUMN remaining_corrections INTEGER DEFAULT 0"
                )
            )
            conn.commit()


if __name__ == "__main__":
    upgrade()
