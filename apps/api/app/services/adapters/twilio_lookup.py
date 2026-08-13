from app.config import settings


def twilio_enabled() -> bool:
    return bool(settings.twilio_account_sid.strip() and settings.twilio_auth_token.strip())


def twilio_lookup(e164: str) -> dict | None:
    if not twilio_enabled():
        return None
    import httpx

    sid = settings.twilio_account_sid.strip()
    token = settings.twilio_auth_token.strip()
    url = f"https://lookups.twilio.com/v2/PhoneNumbers/{e164}"
    try:
        with httpx.Client(timeout=settings.http_timeout_seconds) as client:
            resp = client.get(
                url,
                params={"Fields": "line_type_intelligence"},
                auth=(sid, token),
            )
            if resp.status_code >= 400:
                return None
            data = resp.json()
    except (httpx.HTTPError, ValueError):
        return None

    intel = data.get("line_type_intelligence") or {}
    carrier_name = intel.get("carrier_name") or data.get("carrier", {}).get("name") if isinstance(data.get("carrier"), dict) else intel.get("carrier_name")
    line = intel.get("type")
    return {
        "carrier": (carrier_name or "").strip() or None,
        "line_type": line,
        "mobile_country_code": intel.get("mobile_country_code"),
        "mobile_network_code": intel.get("mobile_network_code"),
        "error_code": intel.get("error_code"),
    }
