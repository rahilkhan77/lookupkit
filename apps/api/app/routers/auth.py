from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.auth import (
    create_session,
    hash_password,
    new_api_key,
    require_user,
    set_session_cookie,
    clear_session_cookie,
    sha256,
    verify_password,
)
from app.config import settings
from app.db import get_db
from app.models import ApiKey, User

router = APIRouter(prefix="/auth", tags=["auth"])


class Credentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


@router.post("/signup", status_code=201)
def signup(payload: Credentials, response: Response, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(
        email=email,
        password_hash=hash_password(payload.password),
        credits=settings.signup_credits,
    )
    db.add(user)
    db.flush()
    raw_key = new_api_key(live=False)
    db.add(
        ApiKey(
            user_id=user.id,
            name="Default test key",
            prefix="lk_test_",
            key_hash=sha256(raw_key),
            last4=raw_key[-4:],
        )
    )
    db.commit()
    db.refresh(user)
    token = create_session(db, user)
    set_session_cookie(response, token)
    return {
        "id": user.id,
        "email": user.email,
        "credits": user.credits,
        "api_key": raw_key,
        "api_key_notice": "Shown once. Store it now. Test keys start with lk_test_.",
    }


@router.post("/login")
def login(payload: Credentials, response: Response, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_session(db, user)
    set_session_cookie(response, token)
    return {"id": user.id, "email": user.email, "credits": user.credits}


@router.post("/logout")
def logout(response: Response):
    clear_session_cookie(response)
    return {"ok": True}


@router.get("/me")
def me(user: User = Depends(require_user)):
    return {"id": user.id, "email": user.email, "credits": user.credits}
