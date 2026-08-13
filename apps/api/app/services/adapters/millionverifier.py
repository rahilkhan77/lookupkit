from app.config import settings


def millionverifier_enabled() -> bool:
    return bool(settings.millionverifier_api_key.strip())


def verify_millionverifier(email: str) -> dict | None:
    if not millionverifier_enabled():
        return None
    import httpx

    url = "https://api.millionverifier.com/api/v3/"
    try:
        with httpx.Client(timeout=settings.http_timeout_seconds) as client:
            resp = client.get(
                url,
                params={"api": settings.millionverifier_api_key, "email": email, "timeout": 10},
            )
            data = resp.json()
    except (httpx.HTTPError, ValueError):
        return None
    result = str(data.get("result") or data.get("quality") or "").lower()
    if result in {"ok", "good", "valid"}:
        deliverable = "yes"
    elif result in {"invalid", "bad", "error", "disposable"}:
        deliverable = "no"
    else:
        deliverable = "unknown"
    return {
        "deliverable": deliverable,
        "result": data.get("result"),
        "quality": data.get("quality"),
        "subresult": data.get("subresult"),
    }
