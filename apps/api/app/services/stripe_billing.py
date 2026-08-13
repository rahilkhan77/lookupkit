from __future__ import annotations

import stripe
from fastapi import HTTPException, status

from app.config import settings, stripe_key_allowed
from app.plans import PLANS


def configure_stripe() -> None:
    ok, reason = stripe_key_allowed()
    if not ok:
        raise RuntimeError(f"Unsafe Stripe configuration: {reason}")
    if settings.stripe_secret_key.strip():
        stripe.api_key = settings.stripe_secret_key.strip()


def stripe_ready() -> bool:
    ok, reason = stripe_key_allowed()
    return ok and bool(settings.stripe_secret_key.strip()) and reason in {"test", "live"}


def create_checkout_session(user_id: str, plan_id: str) -> dict:
    ok, reason = stripe_key_allowed()
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Stripe key refused ({reason}). Use sk_test_ keys unless STRIPE_LIVE=1.",
        )
    if not settings.stripe_secret_key.strip():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Billing is not configured. No charges will be made without STRIPE_SECRET_KEY.",
        )
    plan = PLANS.get(plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown plan")

    configure_stripe()
    session = stripe.checkout.Session.create(
        mode="payment",
        success_url=settings.stripe_success_url,
        cancel_url=settings.stripe_cancel_url,
        line_items=[
            {
                "quantity": 1,
                "price_data": {
                    "currency": "usd",
                    "unit_amount": plan["usd"] * 100,
                    "product_data": {
                        "name": f"Lookupkit {plan['name']}",
                        "description": f"{plan['credits']:,} verification credits",
                    },
                },
            }
        ],
        metadata={"user_id": user_id, "plan": plan_id, "credits": str(plan["credits"])},
    )
    return {"checkout_url": session.url, "id": session.id, "mode": reason}


def parse_webhook(request_body: bytes, signature: str | None) -> dict:
    if not settings.stripe_webhook_secret.strip():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Webhook secret is not configured",
        )
    if not signature:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(
            payload=request_body,
            sig_header=signature,
            secret=settings.stripe_webhook_secret.strip(),
        )
    except Exception as exc:  # noqa: BLE001 — Stripe raises several types
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook") from exc
    return event
