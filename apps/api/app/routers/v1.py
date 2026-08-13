from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth import require_api_key
from app.credits import debit_credits
from app.db import get_db
from app.models import ApiKey, User
from app.services.email_verify import verify_email
from app.services.ip_lookup import lookup_ip
from app.services.phone_verify import verify_phone
from app.services.status import adapter_status

router = APIRouter(prefix="/v1", tags=["v1"])

UNAVAILABLE_DETAIL = {
    "error": "unavailable",
    "code": "not_implemented",
    "message": "This product is not available in the Lookupkit MVP. Lookupkit does not return fabricated person or transcript data.",
}


class EmailIn(BaseModel):
    email: str = Field(min_length=3, max_length=320)


class PhoneIn(BaseModel):
    phone: str | None = None
    phone_number: str | None = None
    default_region: str | None = Field(default=None, max_length=8)


class IpIn(BaseModel):
    ip: str = Field(min_length=3, max_length=64)


@router.get("/health")
def health():
    return {"ok": True, "product": "lookupkit"}


@router.get("/status")
def status():
    return adapter_status()


@router.post("/email")
def email_lookup(
    payload: EmailIn,
    db: Session = Depends(get_db),
    creds: tuple[User, ApiKey] = Depends(require_api_key),
):
    user, key = creds
    result = verify_email(payload.email)
    result["credits_used"] = debit_credits(db, user, key, "/v1/email")
    result["credits_remaining"] = user.credits
    return result


@router.post("/phone")
def phone_lookup(
    payload: PhoneIn,
    db: Session = Depends(get_db),
    creds: tuple[User, ApiKey] = Depends(require_api_key),
):
    user, key = creds
    number = payload.phone or payload.phone_number
    if not number:
        return JSONResponse(status_code=400, content={"detail": "phone is required"})
    result = verify_phone(number, payload.default_region)
    result["credits_used"] = debit_credits(db, user, key, "/v1/phone")
    result["credits_remaining"] = user.credits
    return result


@router.post("/ip")
def ip_lookup(
    payload: IpIn,
    db: Session = Depends(get_db),
    creds: tuple[User, ApiKey] = Depends(require_api_key),
):
    user, key = creds
    result = lookup_ip(payload.ip)
    result["credits_used"] = debit_credits(db, user, key, "/v1/ip")
    result["credits_remaining"] = user.credits
    return result


def _unavailable():
    return JSONResponse(status_code=501, content=UNAVAILABLE_DETAIL)


@router.post("/skip-trace")
@router.post("/skiptrace")
@router.post("/people")
@router.post("/people-search")
@router.post("/transcription")
@router.post("/audio-transcription")
def unavailable_products():
    return _unavailable()
