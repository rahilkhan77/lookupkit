import { Router, type Request, type Response } from "express";
import { verifyPhone } from "../lib/phone.js";
import { verifyEmail } from "../lib/email.js";
import { verifyIp } from "../lib/ip.js";

export const verifyRouter = Router();

function readValue(req: Request, key: string): string | undefined {
  const fromBody = req.body?.[key];
  if (typeof fromBody === "string") return fromBody;
  const fromQuery = req.query?.[key];
  if (typeof fromQuery === "string") return fromQuery;
  return undefined;
}

verifyRouter.post("/phone", (req: Request, res: Response) => {
  const value = readValue(req, "phone") ?? readValue(req, "number");
  if (value === undefined) {
    return res.status(400).json({ error: "missing 'phone' field" });
  }
  const country = readValue(req, "country");
  return res.json(verifyPhone(value, country));
});

verifyRouter.post("/email", (req: Request, res: Response) => {
  const value = readValue(req, "email");
  if (value === undefined) {
    return res.status(400).json({ error: "missing 'email' field" });
  }
  return res.json(verifyEmail(value));
});

verifyRouter.post("/ip", (req: Request, res: Response) => {
  const value = readValue(req, "ip");
  if (value === undefined) {
    return res.status(400).json({ error: "missing 'ip' field" });
  }
  return res.json(verifyIp(value));
});
