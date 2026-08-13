import { describe, it, expect } from "vitest";
import request from "supertest";
import { createApp } from "./app";

const app = createApp();

describe("HTTP API", () => {
  it("GET /health returns ok", async () => {
    const res = await request(app).get("/health");
    expect(res.status).toBe(200);
    expect(res.body.status).toBe("ok");
  });

  it("POST /v1/verify/phone validates a number", async () => {
    const res = await request(app)
      .post("/v1/verify/phone")
      .send({ phone: "+14155552671" });
    expect(res.status).toBe(200);
    expect(res.body.valid).toBe(true);
    expect(res.body.country).toBe("US");
  });

  it("POST /v1/verify/email flags disposable domains", async () => {
    const res = await request(app)
      .post("/v1/verify/email")
      .send({ email: "spam@mailinator.com" });
    expect(res.status).toBe(200);
    expect(res.body.disposable).toBe(true);
  });

  it("POST /v1/verify/ip classifies a public address", async () => {
    const res = await request(app)
      .post("/v1/verify/ip")
      .send({ ip: "8.8.8.8" });
    expect(res.status).toBe(200);
    expect(res.body.scope).toBe("public");
  });

  it("returns 400 when a field is missing", async () => {
    const res = await request(app).post("/v1/verify/email").send({});
    expect(res.status).toBe(400);
  });
});
