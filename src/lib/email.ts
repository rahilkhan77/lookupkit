export interface EmailVerificationResult {
  input: string;
  valid: boolean;
  reason?: string;
  normalized?: string;
  local?: string;
  domain?: string;
  disposable?: boolean;
}

// A small, offline list of well-known disposable email domains. This keeps
// verification deterministic and network-free for local development and tests.
const DISPOSABLE_DOMAINS = new Set<string>([
  "mailinator.com",
  "10minutemail.com",
  "guerrillamail.com",
  "tempmail.com",
  "trashmail.com",
  "yopmail.com",
  "throwawaymail.com",
]);

// RFC 5322-inspired pragmatic pattern: good enough to reject obvious garbage
// without pretending to be a full grammar parser.
const EMAIL_RE =
  /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;

export function verifyEmail(input: string): EmailVerificationResult {
  const trimmed = (input ?? "").trim();
  if (!trimmed) {
    return { input, valid: false, reason: "empty_input" };
  }

  const normalized = trimmed.toLowerCase();

  if (normalized.length > 254) {
    return { input: trimmed, valid: false, reason: "too_long" };
  }

  if (!EMAIL_RE.test(normalized)) {
    return { input: trimmed, valid: false, reason: "invalid_format" };
  }

  const atIndex = normalized.lastIndexOf("@");
  const local = normalized.slice(0, atIndex);
  const domain = normalized.slice(atIndex + 1);

  if (local.length > 64) {
    return { input: trimmed, valid: false, reason: "local_part_too_long" };
  }

  const disposable = DISPOSABLE_DOMAINS.has(domain);

  return {
    input: trimmed,
    valid: true,
    normalized,
    local,
    domain,
    disposable,
  };
}
