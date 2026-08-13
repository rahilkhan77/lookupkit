import { isIP } from "node:net";

export interface IpVerificationResult {
  input: string;
  valid: boolean;
  reason?: string;
  version?: 4 | 6;
  scope?: "private" | "loopback" | "link-local" | "public" | "reserved";
}

function classifyIpv4(ip: string): IpVerificationResult["scope"] {
  const octets = ip.split(".").map((o) => Number(o));
  const [a, b] = octets;

  if (a === 127) return "loopback";
  if (a === 10) return "private";
  if (a === 172 && b >= 16 && b <= 31) return "private";
  if (a === 192 && b === 168) return "private";
  if (a === 169 && b === 254) return "link-local";
  if (a === 0 || a >= 240) return "reserved";
  return "public";
}

function classifyIpv6(ip: string): IpVerificationResult["scope"] {
  const lower = ip.toLowerCase();
  if (lower === "::1") return "loopback";
  if (lower.startsWith("fe80")) return "link-local";
  // Unique local addresses fc00::/7 (fc.. or fd..).
  if (lower.startsWith("fc") || lower.startsWith("fd")) return "private";
  return "public";
}

export function verifyIp(input: string): IpVerificationResult {
  const trimmed = (input ?? "").trim();
  if (!trimmed) {
    return { input, valid: false, reason: "empty_input" };
  }

  const version = isIP(trimmed);
  if (version === 0) {
    return { input: trimmed, valid: false, reason: "invalid_ip" };
  }

  if (version === 4) {
    return {
      input: trimmed,
      valid: true,
      version: 4,
      scope: classifyIpv4(trimmed),
    };
  }

  return {
    input: trimmed,
    valid: true,
    version: 6,
    scope: classifyIpv6(trimmed),
  };
}
