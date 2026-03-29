from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from ..config import settings
from ..db import get_session
from ..models import User
from ..schemas import Token, UserCreate, UserRead

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


def get_password_hash(password: str) -> str:
    """Hash password with bcrypt (truncate to 72 bytes due to bcrypt limitation)"""
    # Bcrypt can only handle passwords up to 72 bytes
    password_truncated = password[:72] if isinstance(password, str) else str(password)[:72]
    return pwd_context.hash(password_truncated)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash (truncate to 72 bytes)"""
    password_truncated = plain_password[:72] if isinstance(plain_password, str) else str(plain_password)[:72]
    return pwd_context.verify(password_truncated, hashed_password)


def get_current_user(token: str, session: Session = Depends(get_session)) -> Optional[User]:
    if not token:
        return None
    from jose import JWTError, jwt
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


@router.post("/register", response_model=UserRead)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    """Register a new user"""
    try:
        # Check if user exists
        statement = select(User).where(User.email == user_data.email.lower())
        existing_user = session.exec(statement).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user with hashed password
        user = User(
            email=user_data.email.lower(),
            full_name=user_data.full_name or "",
            hashed_password=get_password_hash(user_data.password),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login", response_model=Token)
def login(credentials: UserCreate, session: Session = Depends(get_session)):
    """Login and get access token"""
    try:
        statement = select(User).where(User.email == credentials.email.lower())
        user = session.exec(statement).first()
        
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        access_token = create_access_token(subject=user.email)
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    from jose import jwt
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "sub": subject}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
