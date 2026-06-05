# app/services/auth.py
import os
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

# Local layer imports
from app.models.user import Users
from app.repositories.user import UserRepository
from app.schemas.requests.user import LoginRequest, UserCreate

# ─── 1. CONFIGURATIONS & CRYPTO CONTEXT ──────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "your_super_secret_key_change_this_in_production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 🚀 Relative path ensures Swagger UI auth locks click open seamlessly
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")


# ─── 2. CORE SECURITY UTILITIES ──────────────────────────────────────

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ─── 3. ROUTE GUARD DEPENDENCY ────────────────────────────────────────

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Decodes and validates the incoming token. This is what your
    workspaces.py router imports to protect its endpoints!
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate security credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


# ─── 4. AUTH SERVICE CLASS ───────────────────────────────────────────

class AuthService:
    @staticmethod
    def register_user(db: Session, user_schema: UserCreate):
        existing_user = UserRepository.get_user_by_name(db, user_schema.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        db_user = Users(
            user_name=user_schema.username,
            password_hash=hash_password(user_schema.password)
        )
        UserRepository.create_user(db, db_user)
        return {"message": "User created successfully"}

    @staticmethod
    def login_user(db: Session, login_schema: LoginRequest):
        db_user = UserRepository.get_user_by_name(db, login_schema.username)

        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        if not verify_password(login_schema.password, db_user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        token = create_access_token({"sub": db_user.user_name})
        return {
            "access_token": token,
            "token_type": "bearer"
        }