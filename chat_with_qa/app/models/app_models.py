import enum
from ..config.database import Base
from sqlalchemy import (
    Column, String, Integer, DateTime, Boolean, Enum, ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime

class Role(enum.StrEnum):
    admin = "admin"
    normal_user = "normal_user"

class CreateUser(Base):
    __tablename__ = "user"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(30), nullable=False)
    user_type = Column(Enum(Role), default='normal_user')
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    user_unanswered_question = relationship("UnansweredQuestion", back_populates="unanswered_question")
    user_conversation = relationship("Conversation", back_populates="conversation")

class Conversation(Base):
    __tablename__ = "conversation"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    conversation = relationship("CreateUser", back_populates="user_conversation")
    intent = Column(String(30), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    user_question = Column(String(500), nullable=False)
    bot_response = Column(String(500), nullable=False)

class UnansweredQuestion(Base):
    __tablename__ = "unanswered_question"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    unanswered_question = relationship("CreateUser", back_populates="user_unanswered_question")
    user_question = Column(String(30), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    is_resolved = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)
