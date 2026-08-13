from __future__ import annotations

from email_validator import EmailNotValidError, validate_email

from app.config import settings
from app.data.disposable import is_disposable_domain
from app.services.adapters.millionverifier import millionverifier_enabled, verify_millionverifier
from app.services.dns_mx import lookup_mx


def verify_email(address: str) -> dict:
    adapters: list[str] = ["syntax"]
    syntax_valid = False
    normalized = address.strip()
    domain = ""
    try:
        info = validate_email(address, check_deliverability=False)
        syntax_valid = True
        normalized = info.normalized
        domain = info.domain
    except EmailNotValidError:
        domain = address.split("@")[-1].lower() if "@" in address else ""

    mx_records: list[str] = []
    mx_found = False
    mx_error: str | None = None
    if syntax_valid and domain:
        adapters.append("mx")
        mx_found, mx_records, mx_error = lookup_mx(domain, timeout=settings.dns_timeout_seconds)

    disposable = bool(domain) and is_disposable_domain(domain)
    adapters.append("disposable")

    provider = "lookupkit.local"
    enrich: dict = {}
    if millionverifier_enabled():
        mv = verify_millionverifier(normalized)
        if mv is not None:
            adapters.append("millionverifier")
            provider = "millionverifier"
            enrich = mv

    result = {
        "email": normalized,
        "syntax_valid": syntax_valid,
        "mx_found": mx_found,
        "mx_records": mx_records,
        "disposable": disposable,
        "deliverable": enrich.get("deliverable", "unknown"),
        "credits_used": 0,
        "meta": {
            "provider": provider,
            "adapters": adapters,
            "notes": "MX uses live DNS. Deliverable is unknown unless an env-gated vendor adapter is on.",
        },
    }
    if mx_error:
        result["meta"]["mx_error"] = mx_error
    if enrich:
        result["vendor"] = {k: v for k, v in enrich.items() if k != "deliverable"}
    return result
