from __future__ import annotations

import ipaddress

import httpx

from app.config import settings
from app.services.adapters.maxmind import maxmind_enabled, maxmind_lookup


def classify_ip(raw: str) -> tuple[ipaddress._BaseAddress | None, str]:
    try:
        ip = ipaddress.ip_address(raw.strip())
    except ValueError:
        return None, "invalid"
    if ip.is_loopback:
        return ip, "loopback"
    if ip.is_private:
        return ip, "private"
    if ip.is_reserved or ip.is_multicast or ip.is_unspecified or ip.is_link_local:
        return ip, "non_public"
    return ip, "public"


def lookup_ip(raw: str) -> dict:
    ip, classification = classify_ip(raw)
    if ip is None:
        return {
            "ip": raw,
            "valid": False,
            "is_public": False,
            "classification": "invalid",
            "credits_used": 0,
            "meta": {"provider": "lookupkit.local", "adapters": ["local"]},
        }

    base = {
        "ip": str(ip),
        "valid": True,
        "version": ip.version,
        "is_public": classification == "public",
        "classification": classification,
        "credits_used": 0,
    }

    if classification != "public":
        return {
            **base,
            "country": None,
            "city": None,
            "isp": None,
            "org": None,
            "proxy": None,
            "hosting": None,
            "meta": {
                "provider": "lookupkit.local",
                "adapters": ["local"],
                "notes": "Non-public addresses are classified locally. No geolocation is invented.",
            },
        }

    adapters = ["ip-api.com"]
    provider = "ip-api.com"
    geo = _ip_api(str(ip))

    mm = None
    if maxmind_enabled():
        mm = maxmind_lookup(str(ip))
        if mm is not None:
            adapters.append("maxmind")
            provider = "maxmind"

    merged = {**geo, **(mm or {})} if mm else geo
    return {
        **base,
        "country": merged.get("country"),
        "country_code": merged.get("country_code"),
        "region": merged.get("region"),
        "city": merged.get("city"),
        "lat": merged.get("lat"),
        "lon": merged.get("lon"),
        "isp": merged.get("isp"),
        "org": merged.get("org"),
        "as": merged.get("as"),
        "proxy": merged.get("proxy"),
        "hosting": merged.get("hosting"),
        "mobile": merged.get("mobile"),
        "timezone": merged.get("timezone"),
        "meta": {
            "provider": provider,
            "adapters": adapters,
            "notes": "Public IPs use ip-api.com unless MaxMind is configured. Provider names are the actual source.",
        },
        **({"vendor": mm} if mm else {}),
    }


def _ip_api(ip: str) -> dict:
    fields = "status,message,country,countryCode,region,regionName,city,lat,lon,timezone,isp,org,as,mobile,proxy,hosting,query"
    url = f"http://ip-api.com/json/{ip}"
    try:
        with httpx.Client(timeout=settings.http_timeout_seconds) as client:
            resp = client.get(url, params={"fields": fields})
            data = resp.json()
    except (httpx.HTTPError, ValueError) as exc:
        return {"error": str(exc)}
    if data.get("status") != "success":
        return {"error": data.get("message", "ip-api lookup failed")}
    return {
        "country": data.get("country"),
        "country_code": data.get("countryCode"),
        "region": data.get("regionName"),
        "city": data.get("city"),
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "timezone": data.get("timezone"),
        "isp": data.get("isp"),
        "org": data.get("org"),
        "as": data.get("as"),
        "mobile": data.get("mobile"),
        "proxy": data.get("proxy"),
        "hosting": data.get("hosting"),
    }
