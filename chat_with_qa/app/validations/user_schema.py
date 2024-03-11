from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_type: Optional[str] = "normal_user"

class ChangePassword(BaseModel):
    password: str

class InstertIntoJson(BaseModel):
    tag: str
    patterns: list
    responses: list

class User(UserCreate):
    id: int
    is_active: bool
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    user_email: str
    password: str

class QuestionStatus(BaseModel):
    is_resolved: bool
