from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List
from sqlalchemy.orm import Session

from ..utils.users import get_user, get_user_by_email, get_users, create_user, authenticate_user, update_user, delete_user,unanswered_question_db,conversation_db,read_unanswered_questions,update_status,get_history
from ..validations.user_schema import UserCreate, User, UserLogin, ChangePassword, InstertIntoJson,QuestionStatus
from ..utils.json_utils import insert_intent, read_json, read_specific_intent,update_specific_intent
from ..utils.train_chatbot_model import intents_migrate
from ..config.database import get_db
from ..utils.chatbot import user_msg

router = APIRouter()

@router.post("/login")
async def user_login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(user_credentials.user_email, user_credentials.password, db)
    return user



@router.get("/users", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.post("/create_user", status_code=201)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return create_user(db=db, user=user)

@router.get("/user/{user_id}", response_model=User)
def read_user(user_id, db: Session = Depends(get_db)):
    db_user = get_user(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}")
async def change_password(user_id, user:ChangePassword, db: Session = Depends(get_db)):
    db_user = update_user(user_id, user, db)
    return db_user

@router.delete("/user/{user_id}")
async def user_delete(user_id, db: Session = Depends(get_db)):
    db_user = delete_user(user_id, db)
    return db_user

@router.post("/chat/{message}")
async def chat(message: str, db: Session = Depends(get_db)):
    try:
        response, tag = user_msg(message)
        if response == "I'm still learning! Soon I will able to give answer related to this question":
            unanswered_question_db(db, 7, message)
        else:
            conversation_db(db, 7, message, tag, response)
        return {"Bot": response}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"Bot": "Sorry, I encountered an error. Please try again later."}

@router.post("/create_question_answer")
async def create_intent(data: InstertIntoJson):
    intent_db = insert_intent(data)
    if intent_db == "Intent tag already exists":
        raise HTTPException(status_code=409, detail="Intent tag already exists")
    # intents_migrate()
    return intent_db

@router.get("/chatbot_db")
async def get_chatbot_db():
    chatbot_db = read_json()
    return chatbot_db

@router.get("/json-data/{tag_name}")
async def get_specific_intent(tag_name: str):
    chatbot_intent = read_specific_intent(tag_name)
    return chatbot_intent

@router.put("/json-data/{tag_name}")
async def update_json_data(tag_name: str, update_data: dict = Body(None)):
    chatbot_intent = update_specific_intent(tag_name,update_data)
    return chatbot_intent

@router.get("/get_unanswered_questions")
async def get_unanswered_questions(db: Session = Depends(get_db)):
    chatbot_intent = read_unanswered_questions(db)
    return chatbot_intent

@router.put("/update_status_unanswered_questions/{question_id}")
async def update_unanswered_question_status(question_id, status:QuestionStatus, db: Session = Depends(get_db)):
    chatbot_intent = update_status(question_id, status, db)
    return chatbot_intent

@router.get("/history")
async def read_history(db: Session = Depends(get_db)):
    chat_history = get_history(db)
    return chat_history


