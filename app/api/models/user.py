from datetime import datetime

from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(Document):
    full_name: str
    email: EmailStr
    password: str
    mobile: Optional[str]

    class Settings:
        collection = "users"

class UserSignUp(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    mobile: Optional[str]
    gender: str
    dob: datetime
    address: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
