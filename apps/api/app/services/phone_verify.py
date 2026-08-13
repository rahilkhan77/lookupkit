from __future__ import annotations

import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat, PhoneNumberType, carrier, geocoder

from app.services.adapters.twilio_lookup import twilio_enabled, twilio_lookup

LINE_TYPE_MAP = {
    PhoneNumberType.FIXED_LINE: "fixed_line",
    PhoneNumberType.MOBILE: "mobile",
    PhoneNumberType.FIXED_LINE_OR_MOBILE: "fixed_line_or_mobile",
    PhoneNumberType.TOLL_FREE: "toll_free",
    PhoneNumberType.PREMIUM_RATE: "premium_rate",
    PhoneNumberType.SHARED_COST: "shared_cost",
    PhoneNumberType.VOIP: "voip",
    PhoneNumberType.PERSONAL_NUMBER: "personal_number",
    PhoneNumberType.PAGER: "pager",
    PhoneNumberType.UAN: "uan",
    PhoneNumberType.VOICEMAIL: "voicemail",
    PhoneNumberType.UNKNOWN: "unknown",
}


def verify_phone(raw: str, default_region: str | None = None) -> dict:
    adapters = ["libphonenumber"]
    parsed = None
    parse_error = None
    try:
        parsed = phonenumbers.parse(raw, default_region)
    except NumberParseException as exc:
        parse_error = exc.error_type

    if parsed is None:
        return {
            "phone": raw,
            "e164": None,
            "valid": False,
            "possible": False,
            "region": None,
            "country_code": None,
            "line_type": "unknown",
            "carrier": None,
            "carrier_status": "unknown",
            "credits_used": 0,
            "meta": {
                "provider": "libphonenumber",
                "adapters": adapters,
                "parse_error": parse_error,
                "notes": "Carrier is unknown unless a live lookup adapter (Twilio) is enabled. Lookupkit never invents a carrier name.",
            },
        }

    valid = phonenumbers.is_valid_number(parsed)
    possible = phonenumbers.is_possible_number(parsed)
    e164 = phonenumbers.format_number(parsed, PhoneNumberFormat.E164) if possible else None
    region = phonenumbers.region_code_for_number(parsed)
    line = LINE_TYPE_MAP.get(phonenumbers.number_type(parsed), "unknown")

    # Offline prefix metadata only — empty means unknown. Never substitute a fake brand.
    prefix_carrier = (carrier.name_for_number(parsed, "en") or "").strip()
    carrier_name = prefix_carrier or None
    carrier_status = "prefix_metadata" if carrier_name else "unknown"
    provider = "libphonenumber"

    geo = (geocoder.description_for_number(parsed, "en") or "").strip() or None

    twilio_data = None
    if twilio_enabled() and e164:
        twilio_data = twilio_lookup(e164)
        if twilio_data is not None:
            adapters.append("twilio")
            provider = "twilio"
            live_carrier = (twilio_data.get("carrier") or "").strip()
            if live_carrier:
                carrier_name = live_carrier
                carrier_status = "live"
            else:
                carrier_status = "unknown"
            if twilio_data.get("line_type"):
                line = twilio_data["line_type"]

    return {
        "phone": raw,
        "e164": e164,
        "valid": valid,
        "possible": possible,
        "region": region,
        "country_code": parsed.country_code,
        "national_format": phonenumbers.format_number(parsed, PhoneNumberFormat.NATIONAL) if possible else None,
        "line_type": line,
        "carrier": carrier_name,
        "carrier_status": carrier_status,
        "location": geo,
        "credits_used": 0,
        "meta": {
            "provider": provider,
            "adapters": adapters,
            "notes": "libphonenumber carrier values are prefix metadata, not live HLR. Missing carrier stays unknown — never a placeholder like Example Wireless.",
        },
        **({"vendor": twilio_data} if twilio_data else {}),
    }
