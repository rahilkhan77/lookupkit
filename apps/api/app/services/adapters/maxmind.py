from app.config import settings


def maxmind_enabled() -> bool:
    return bool(settings.maxmind_license_key.strip() and settings.maxmind_account_id.strip())


def maxmind_lookup(ip: str) -> dict | None:
    """GeoIP2 Precision web service. Off unless account id + license key are set.
    Does not download GeoLite databases (that requires accepting MaxMind ToS).
    """
    if not maxmind_enabled():
        return None
    import httpx

    url = f"https://geoip.maxmind.com/geoip/v2.1/city/{ip}"
    try:
        with httpx.Client(timeout=settings.http_timeout_seconds) as client:
            resp = client.get(
                url,
                auth=(settings.maxmind_account_id.strip(), settings.maxmind_license_key.strip()),
            )
            if resp.status_code >= 400:
                return None
            data = resp.json()
    except (httpx.HTTPError, ValueError):
        return None

    country = (data.get("country") or {}).get("names", {}).get("en")
    country_code = (data.get("country") or {}).get("iso_code")
    city = (data.get("city") or {}).get("names", {}).get("en")
    loc = data.get("location") or {}
    traits = data.get("traits") or {}
    return {
        "country": country,
        "country_code": country_code,
        "city": city,
        "lat": loc.get("latitude"),
        "lon": loc.get("longitude"),
        "timezone": loc.get("time_zone"),
        "isp": traits.get("isp"),
        "org": traits.get("organization"),
        "as": traits.get("autonomous_system_number"),
        "proxy": traits.get("is_anonymous_proxy"),
        "hosting": traits.get("is_hosting_provider"),
    }
