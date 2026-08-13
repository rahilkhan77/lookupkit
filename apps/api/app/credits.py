from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import ApiKey, UsageEvent, User
from app.plans import LOOKUP_CREDIT_COST


def debit_credits(
    db: Session,
    user: User,
    api_key: ApiKey | None,
    endpoint: str,
    cost: int = LOOKUP_CREDIT_COST,
) -> int:
    if user.credits < cost:
        db.add(
            UsageEvent(
                user_id=user.id,
                api_key_id=api_key.id if api_key else None,
                endpoint=endpoint,
                credits_used=0,
                status_code=402,
            )
        )
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Insufficient credits",
        )
    user.credits -= cost
    db.add(
        UsageEvent(
            user_id=user.id,
            api_key_id=api_key.id if api_key else None,
            endpoint=endpoint,
            credits_used=cost,
            status_code=200,
        )
    )
    db.commit()
    db.refresh(user)
    return cost


def grant_credits(db: Session, user: User, amount: int) -> int:
    user.credits += amount
    db.commit()
    db.refresh(user)
    return user.credits
