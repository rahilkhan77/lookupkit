from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.auth import require_user
from app.credits import grant_credits
from app.db import get_db
from app.models import User, WaitlistEntry, ContactMessage
from app.plans import PLANS
from app.services.stripe_billing import create_checkout_session, parse_webhook, stripe_ready

router = APIRouter(tags=["billing"])


class CheckoutIn(BaseModel):
    plan: str


class WaitlistIn(BaseModel):
    email: EmailStr


class ContactIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    message: str = Field(min_length=1, max_length=4000)


@router.get("/billing/plans")
def plans():
    return {
        "plans": list(PLANS.values()),
        "stripe_ready": stripe_ready(),
        "note": "No live charges without a configured Stripe key. Test keys only unless STRIPE_LIVE=1.",
    }


@router.post("/billing/checkout")
def checkout(payload: CheckoutIn, user: User = Depends(require_user)):
    return create_checkout_session(user.id, payload.plan)


@router.post("/billing/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db),
    stripe_signature: str | None = Header(default=None, alias="Stripe-Signature"),
):
    body = await request.body()
    event = parse_webhook(body, stripe_signature)
    if event.get("type") == "checkout.session.completed":
        obj = event.get("data", {}).get("object", {})
        metadata = obj.get("metadata") or {}
        user_id = metadata.get("user_id")
        credits = int(metadata.get("credits") or 0)
        user = db.query(User).filter(User.id == user_id).first()
        if user and credits > 0:
            grant_credits(db, user, credits)
    return {"received": True}


@router.post("/waitlist", status_code=201)
def waitlist(payload: WaitlistIn, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    existing = db.query(WaitlistEntry).filter(WaitlistEntry.email == email).first()
    if existing:
        return {"ok": True, "already": True}
    db.add(WaitlistEntry(email=email))
    db.commit()
    return {"ok": True, "already": False}


@router.post("/public/contact", status_code=201)
def contact(payload: ContactIn, db: Session = Depends(get_db)):
    db.add(ContactMessage(name=payload.name.strip(), email=payload.email.lower().strip(), message=payload.message.strip()))
    db.commit()
    return {"ok": True}
