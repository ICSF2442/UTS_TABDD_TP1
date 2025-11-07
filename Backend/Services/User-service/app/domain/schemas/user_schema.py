from wsgiref.validate import validator
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "user"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Nome não pode estar vazio')
        return v.strip()
    
    @validator('password')
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError('Password deve ter pelo menos 6 caracteres')
        return v

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserOut(UserBase):
    user_id: int
    created_at: datetime
