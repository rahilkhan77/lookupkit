from app.config import settings
from app.services.adapters.maxmind import maxmind_enabled
from app.services.adapters.millionverifier import millionverifier_enabled
from app.services.adapters.twilio_lookup import twilio_enabled


def adapter_status() -> dict:
    return {
        "email": {
            "syntax": True,
            "mx_dns": True,
            "disposable": True,
            "millionverifier": millionverifier_enabled(),
        },
        "phone": {
            "libphonenumber": True,
            "twilio": twilio_enabled(),
        },
        "ip": {
            "ip_api": True,
            "maxmind": maxmind_enabled(),
        },
        "billing": {
            "stripe_configured": bool(settings.stripe_secret_key.strip()),
            "stripe_live_enabled": settings.stripe_live.strip() == "1",
        },
        "unavailable": ["skip-trace", "people-search", "transcription"],
    }
