from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta

from app.schemas.auth_schema import SignupRequest, LoginRequest, TokenResponse
from app.models.user_model import User
from app.dependencies import get_db
from app.services.token_service import create_access_token
from app.config.settings import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@router.post(
    "/signup",
    response_model=TokenResponse,
    summary="Yeni kullanıcı kaydı",
    description="Email ve şifre ile yeni kullanıcı oluşturur. Başarılı olursa access token döner."
)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(payload.password)
    new_user = User(email=payload.email, password=hashed_pw, role="user")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(
        data={"sub": str(new_user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Kullanıcı girişi",
    description="Kayıtlı bir kullanıcı email & şifre ile giriş yapar. Başarılı olursa access token döner."
)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
