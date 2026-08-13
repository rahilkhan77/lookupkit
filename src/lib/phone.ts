import {
  parsePhoneNumberFromString,
  type CountryCode,
} from "libphonenumber-js";

export interface PhoneVerificationResult {
  input: string;
  valid: boolean;
  reason?: string;
  e164?: string;
  country?: string;
  type?: string;
  nationalNumber?: string;
}

/**
 * Verify a phone number. An optional ISO country code helps interpret
 * numbers that are not written in international (+CC) format.
 */
export function verifyPhone(
  input: string,
  country?: string,
): PhoneVerificationResult {
  const trimmed = (input ?? "").trim();
  if (!trimmed) {
    return { input, valid: false, reason: "empty_input" };
  }

  const parsed = parsePhoneNumberFromString(
    trimmed,
    country ? (country.toUpperCase() as CountryCode) : undefined,
  );

  if (!parsed) {
    return { input: trimmed, valid: false, reason: "unparseable" };
  }

  if (!parsed.isValid()) {
    return {
      input: trimmed,
      valid: false,
      reason: "invalid_number",
      e164: parsed.number,
      country: parsed.country,
    };
  }

  return {
    input: trimmed,
    valid: true,
    e164: parsed.number,
    country: parsed.country,
    type: parsed.getType(),
    nationalNumber: parsed.nationalNumber,
  };
}
