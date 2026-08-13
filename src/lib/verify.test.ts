import { describe, it, expect } from "vitest";
import { verifyPhone } from "./phone";
import { verifyEmail } from "./email";
import { verifyIp } from "./ip";

describe("verifyPhone", () => {
  it("accepts a valid E.164 number", () => {
    const r = verifyPhone("+14155552671");
    expect(r.valid).toBe(true);
    expect(r.e164).toBe("+14155552671");
    expect(r.country).toBe("US");
  });

  it("interprets a national number with a country hint", () => {
    const r = verifyPhone("020 7946 0958", "GB");
    expect(r.valid).toBe(true);
    expect(r.country).toBe("GB");
  });

  it("rejects garbage", () => {
    expect(verifyPhone("not-a-phone").valid).toBe(false);
    expect(verifyPhone("").valid).toBe(false);
  });
});

describe("verifyEmail", () => {
  it("accepts a normal address and normalizes case", () => {
    const r = verifyEmail("Alice@Example.com");
    expect(r.valid).toBe(true);
    expect(r.normalized).toBe("alice@example.com");
    expect(r.domain).toBe("example.com");
    expect(r.disposable).toBe(false);
  });

  it("flags disposable domains", () => {
    const r = verifyEmail("spam@mailinator.com");
    expect(r.valid).toBe(true);
    expect(r.disposable).toBe(true);
  });

  it("rejects malformed addresses", () => {
    expect(verifyEmail("nope").valid).toBe(false);
    expect(verifyEmail("a@b").valid).toBe(false);
    expect(verifyEmail("").valid).toBe(false);
  });
});

describe("verifyIp", () => {
  it("classifies a public IPv4", () => {
    const r = verifyIp("8.8.8.8");
    expect(r.valid).toBe(true);
    expect(r.version).toBe(4);
    expect(r.scope).toBe("public");
  });

  it("classifies private and loopback IPv4", () => {
    expect(verifyIp("10.0.0.1").scope).toBe("private");
    expect(verifyIp("192.168.1.1").scope).toBe("private");
    expect(verifyIp("127.0.0.1").scope).toBe("loopback");
  });

  it("handles IPv6", () => {
    expect(verifyIp("::1").scope).toBe("loopback");
    expect(verifyIp("2001:4860:4860::8888").version).toBe(6);
  });

  it("rejects invalid IPs", () => {
    expect(verifyIp("999.999.999.999").valid).toBe(false);
    expect(verifyIp("").valid).toBe(false);
  });
});
