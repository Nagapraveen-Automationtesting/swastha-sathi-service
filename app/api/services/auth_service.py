from app.api.core.db import BaseRepository
from app.api.core.logger import logger
from app.api.models.user import User, UserSignUp
from app.api.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException
from datetime import timedelta

async def register_user(user_data: UserSignUp):
    """Register a new user"""
    existing_user = await BaseRepository.find_one(User, {"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)
    user_dict = user_data.dict()
    user_dict["password"] = hashed_password

    return await BaseRepository.insert_one(User, user_dict)

async def login_user(email: str, password: str):
    """Authenticate user and generate JWT"""
    user = await BaseRepository.find_one(User, {"email": email})
    if not user or not verify_password(password, user.password):
        logger.error(f"User credentials are invalid, username : {email}, password: {password}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    logger.info(f"User credentials are valid for user {email}")
    access_token = create_access_token({"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}
