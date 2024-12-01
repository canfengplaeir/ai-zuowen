from datetime import datetime
from typing import Dict, Any
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import json

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    remaining_corrections = Column(Integer, default=0)

    essays = relationship(
        "Essay", back_populates="author", cascade="all, delete-orphan"
    )

    def __init__(self, username: str, password: str, is_admin: bool = False) -> None:
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.remaining_corrections = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "essay_count": len(list(self.essays)),
            "remaining_corrections": self.remaining_corrections,
        }


class Essay(db.Model):
    __tablename__ = "essays"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    feedback = Column(String, nullable=True)
    score = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="essays")

    def __init__(
        self,
        user_id: int,
        content: str,
        feedback: dict,
        score: int,
    ) -> None:
        self.user_id = user_id
        self.content = content
        self.feedback = (
            json.dumps(feedback) if isinstance(feedback, dict) else str(feedback)
        )
        self.score = score

    def to_dict(self) -> Dict[str, Any]:
        try:
            feedback_data = json.loads(self.feedback) if self.feedback else None
        except json.JSONDecodeError:
            feedback_data = self.feedback

        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "feedback": feedback_data,
            "score": self.score,
            "created_at": self.created_at.isoformat(),
            "username": self.author.username if self.author else None,
        }


class ActivationCode(db.Model):
    __tablename__ = "activation_codes"

    id = Column(Integer, primary_key=True)
    code = Column(String(32), unique=True, nullable=False)
    correction_count = Column(Integer, nullable=False)
    is_used = Column(Boolean, default=False)
    used_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))

    def __init__(self, code: str, correction_count: int, created_by: int) -> None:
        self.code = code
        self.correction_count = correction_count
        self.created_by = created_by

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "code": self.code,
            "correction_count": self.correction_count,
            "is_used": self.is_used,
            "used_by": self.used_by,
            "used_at": self.used_at.isoformat() if self.used_at else None,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
        }
