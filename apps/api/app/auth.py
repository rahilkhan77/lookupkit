import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Cookie, Depends, Header, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.models import ApiKey, SessionToken, User

COOKIE_NAME = "lk_session"
SESSION_DAYS = 14


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def new_session_token() -> str:
    return secrets.token_urlsafe(32)


def new_api_key(live: bool = False) -> str:
    prefix = "lk_live_" if live else "lk_test_"
    return prefix + secrets.token_urlsafe(32)


def set_session_cookie(response: Response, raw_token: str) -> None:
    response.set_cookie(
        key=COOKIE_NAME,
        value=raw_token,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        max_age=SESSION_DAYS * 24 * 60 * 60,
        path="/",
    )


def clear_session_cookie(response: Response) -> None:
    response.delete_cookie(key=COOKIE_NAME, path="/")


def create_session(db: Session, user: User) -> str:
    raw = new_session_token()
    expires = datetime.now(timezone.utc) + timedelta(days=SESSION_DAYS)
    db.add(SessionToken(user_id=user.id, token_hash=sha256(raw), expires_at=expires))
    db.commit()
    return raw


def user_from_session(db: Session, raw_token: str | None) -> User | None:
    if not raw_token:
        return None
    row = db.query(SessionToken).filter(SessionToken.token_hash == sha256(raw_token)).first()
    if not row:
        return None
    expires = row.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    if expires < datetime.now(timezone.utc):
        return None
    return db.query(User).filter(User.id == row.user_id).first()


def require_user(
    lk_session: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    user = user_from_session(db, lk_session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user


def optional_user(
    lk_session: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User | None:
    return user_from_session(db, lk_session)


def parse_bearer(authorization: str | None) -> str | None:
    if not authorization:
        return None
    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1].strip()


def require_api_key(
    authorization: str | None = Header(default=None),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    db: Session = Depends(get_db),
) -> tuple[User, ApiKey]:
    raw = x_api_key or parse_bearer(authorization)
    if not raw or not (raw.startswith("lk_live_") or raw.startswith("lk_test_")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key required")
    key = db.query(ApiKey).filter(ApiKey.key_hash == sha256(raw), ApiKey.revoked.is_(False)).first()
    if not key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    user = db.query(User).filter(User.id == key.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return user, key
