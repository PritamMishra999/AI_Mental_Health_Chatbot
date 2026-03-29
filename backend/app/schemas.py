from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    emotion: str
    stress_score: int
    recommendation: str


class ConversationMessageRead(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True


class ConversationRead(BaseModel):
    id: int
    title: Optional[str] = None
    created_at: datetime
    messages: List[ConversationMessageRead] = []

    class Config:
        orm_mode = True
