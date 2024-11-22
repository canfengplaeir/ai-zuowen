from datetime import datetime
from typing import Dict, Any, List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, relationship

db: SQLAlchemy = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    username: Mapped[str] = db.Column(db.String(80), unique=True, nullable=False)
    password: Mapped[str] = db.Column(db.String(120), nullable=False)
    is_admin: Mapped[bool] = db.Column(db.Boolean, default=False)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    essays: Mapped[List["Essay"]] = relationship('Essay', backref='author', lazy=True, cascade='all, delete-orphan')

    def __init__(self, username: str, password: str, is_admin: bool = False) -> None:
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'username': self.username,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'essay_count': len(list(self.essays))
        }

class Essay(db.Model):
    __tablename__ = 'essays'
    
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    user_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content: Mapped[str] = db.Column(db.Text, nullable=False)
    original_image: Mapped[str] = db.Column(db.String(255))
    score: Mapped[int] = db.Column(db.Integer)
    feedback: Mapped[str] = db.Column(db.Text)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id: int, content: str, original_image: str, feedback: str, score: int = None) -> None:
        self.user_id = user_id
        self.content = content
        self.original_image = original_image
        self.feedback = feedback
        self.score = score

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'content': self.content,
            'feedback': self.feedback,
            'score': self.score,
            'created_at': self.created_at.isoformat()
        } 