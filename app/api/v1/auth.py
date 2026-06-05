# app/api/v1/auth.py
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.requests.user import UserCreate, LoginRequest
from app.schemas.response.user import UserResponse

from app.services.auth import AuthService  # 🧠 Points to your service brain file

# 🚨 This is what main.py is looking for!
router = APIRouter(tags=["Authentication"])

@router.post("/register",response_model=UserResponse)
def register(user_schema: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register_user(db, user_schema)

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Maps OAuth2 form inputs to your internal LoginRequest schema format
    login_schema = LoginRequest(username=form_data.username, password=form_data.password)
    return AuthService.login_user(db, login_schema)