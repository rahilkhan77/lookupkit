from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth import new_api_key, require_user, sha256
from app.db import get_db
from app.models import ApiKey, UsageEvent, User

router = APIRouter(prefix="/account", tags=["account"])


class KeyCreate(BaseModel):
    name: str = Field(default="key", max_length=80)
    live: bool = False


@router.get("/me")
def account_me(user: User = Depends(require_user)):
    return {"id": user.id, "email": user.email, "credits": user.credits}


@router.get("/keys")
def list_keys(user: User = Depends(require_user), db: Session = Depends(get_db)):
    rows = (
        db.query(ApiKey)
        .filter(ApiKey.user_id == user.id)
        .order_by(ApiKey.created_at.desc())
        .all()
    )
    return [
        {
            "id": k.id,
            "name": k.name,
            "prefix": k.prefix,
            "hint": f"{k.prefix}…{k.last4}",
            "revoked": k.revoked,
            "created_at": k.created_at.isoformat(),
        }
        for k in rows
    ]


@router.post("/keys", status_code=201)
def create_key(payload: KeyCreate, user: User = Depends(require_user), db: Session = Depends(get_db)):
    raw = new_api_key(live=payload.live)
    prefix = "lk_live_" if payload.live else "lk_test_"
    row = ApiKey(
        user_id=user.id,
        name=payload.name,
        prefix=prefix,
        key_hash=sha256(raw),
        last4=raw[-4:],
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return {
        "id": row.id,
        "name": row.name,
        "prefix": row.prefix,
        "key": raw,
        "notice": "Full key is shown once.",
    }


@router.delete("/keys/{key_id}")
def revoke_key(key_id: str, user: User = Depends(require_user), db: Session = Depends(get_db)):
    row = db.query(ApiKey).filter(ApiKey.id == key_id, ApiKey.user_id == user.id).first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
    row.revoked = True
    db.commit()
    return {"ok": True}


@router.get("/usage")
def usage(user: User = Depends(require_user), db: Session = Depends(get_db)):
    rows = (
        db.query(UsageEvent)
        .filter(UsageEvent.user_id == user.id)
        .order_by(UsageEvent.created_at.desc())
        .limit(100)
        .all()
    )
    return [
        {
            "id": e.id,
            "endpoint": e.endpoint,
            "credits_used": e.credits_used,
            "status_code": e.status_code,
            "created_at": e.created_at.isoformat(),
        }
        for e in rows
    ]
