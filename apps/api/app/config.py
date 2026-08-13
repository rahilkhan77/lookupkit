from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./lookupkit.db"
    redis_url: str = ""
    session_secret: str = "dev-only-change-me"
    cookie_secure: bool = False
    api_public_url: str = "http://localhost:8000"
    web_origin: str = "http://localhost:3000"
    signup_credits: int = 100

    millionverifier_api_key: str = ""
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    maxmind_license_key: str = ""
    maxmind_account_id: str = ""

    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_live: str = "0"
    stripe_success_url: str = "http://localhost:3000/dashboard/billing?status=success"
    stripe_cancel_url: str = "http://localhost:3000/dashboard/billing?status=cancel"

    dns_timeout_seconds: float = 2.5
    http_timeout_seconds: float = 6.0


settings = Settings()


def stripe_key_allowed(secret_key: str | None = None, live_flag: str | None = None) -> tuple[bool, str]:
    """Return (ok, reason). Live keys are refused unless STRIPE_LIVE=1."""
    key = (secret_key if secret_key is not None else settings.stripe_secret_key).strip()
    live = (live_flag if live_flag is not None else settings.stripe_live).strip()
    if not key:
        return True, "stripe_unconfigured"
    if key.startswith("sk_live_") and live != "1":
        return False, "live_key_refused"
    if key.startswith("sk_test_"):
        return True, "test"
    if key.startswith("sk_live_") and live == "1":
        return True, "live"
    return False, "unrecognized_stripe_key"


def assert_stripe_safe() -> None:
    ok, reason = stripe_key_allowed()
    if not ok:
        raise RuntimeError(
            "Refusing to start with a live or unrecognized Stripe key. "
            "Use STRIPE_SECRET_KEY=sk_test_... or set STRIPE_LIVE=1 for sk_live_ keys. "
            f"reason={reason}"
        )
