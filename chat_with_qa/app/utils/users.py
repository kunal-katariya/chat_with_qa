from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.app_models import CreateUser, UnansweredQuestion,Conversation
from ..validations.user_schema import UserCreate

def get_user(user_id,db):
    return db.query(CreateUser).filter(CreateUser.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(CreateUser).filter(CreateUser.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CreateUser).offset(skip).limit(limit).all()

def authenticate_user(user_email: str, password: str,db):
    check_user = db.query(CreateUser).filter(CreateUser.email == user_email).first()
    if not check_user:
        raise HTTPException(status_code=401, detail="Email Id is Incorrect")
    if check_user.password != password:
        raise HTTPException(status_code=401, detail="Password is Incorrect")
    if check_user.user_type == "admin":
        return {"msg": "Welcome Admin", "id": check_user.id}
    return {"msg": "User Login Successful", "id": check_user.id}

def update_user(user_id, user, db):
    db_user = db.query(CreateUser).filter(CreateUser.id == user_id).first()
    db_user.password=user.password

    db.add(db_user)
    db.commit()

    return "Password updated successfully"

def delete_user(user_id,db):
    db_user = db.query(CreateUser).filter(CreateUser.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return "User deleted successfully"
    else:
        raise HTTPException(status_code=404, detail="User not found")

def create_user(db: Session, user: UserCreate):
    # user_type = user.user_type or "normal_user"
    db_user = CreateUser(name=user.name,email=user.email,password=user.password,user_type=user.user_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def unanswered_question_db(db: Session, uid, question):
    db_user = UnansweredQuestion(user_id=uid, user_question=question)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def conversation_db(db: Session, uid, user_msg, tag, bot_response):
    db_user = Conversation(user_id=uid,intent=tag, user_question=user_msg,bot_response=bot_response)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def read_unanswered_questions(db):
    return db.query(UnansweredQuestion).all()

def update_status(question_id, status, db):
    db_question = db.query(UnansweredQuestion).filter(UnansweredQuestion.id == question_id).first()
    if db_question:
        db_question.is_resolved = status.is_resolved
        db_question.updated_at = datetime.now()
        db.add(db_question)
        db.commit()
        return "Status updated successfully"
    else:
        raise HTTPException(status_code=404, detail="Question not found")

def get_history(db):
    return db.query(Conversation).all()
