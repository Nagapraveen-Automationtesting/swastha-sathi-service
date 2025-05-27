from fastapi import APIRouter, Depends
from app.api.models.user import UserSignUp, UserLogin
from app.api.services.auth_service import register_user, login_user

auth_router = APIRouter()

@auth_router.post("/signup")
async def signup(user: UserSignUp):
    return await register_user(user)

@auth_router.post("/login")
async def login(user: UserLogin):
    return await login_user(user.email, user.password)
