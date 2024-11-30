from datetime import datetime
from typing import Dict, Any
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import json

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # 修改关系定义
    essays = relationship(
        "Essay", back_populates="author", cascade="all, delete-orphan"
    )

    def __init__(self, username: str, password: str, is_admin: bool = False) -> None:
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "username": self.username,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "essay_count": len(list(self.essays)),
        }


class Essay(db.Model):
    __tablename__ = "essays"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    feedback: Mapped[str] = mapped_column(nullable=True)
    score: Mapped[int] = mapped_column(nullable=True)
    original_image: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # 修改关系定义
    author = relationship("User", back_populates="essays")

    def __init__(
        self,
        user_id: int,
        content: str,
        feedback: dict,
        score: int,
        original_image: str,
    ) -> None:
        self.user_id = user_id
        self.content = content
        # 确保 feedback 是有效的 JSON 字符串
        self.feedback = (
            json.dumps(feedback) if isinstance(feedback, dict) else str(feedback)
        )
        self.score = score
        self.original_image = original_image

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        try:
            # 尝试解析 JSON，如果失败则返回原始字符串
            feedback_data = json.loads(self.feedback) if self.feedback else None
        except json.JSONDecodeError:
            feedback_data = self.feedback

        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "feedback": feedback_data,
            "score": self.score,
            "original_image": self.original_image,
            "created_at": self.created_at.isoformat(),
            "username": self.author.username if self.author else None,
        }
