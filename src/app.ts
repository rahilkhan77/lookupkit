import express, { type Express, type Request, type Response } from "express";
import { verifyRouter } from "./routes/verify.js";

export function createApp(): Express {
  const app = express();

  app.use(express.json());

  app.get("/health", (_req: Request, res: Response) => {
    res.json({ status: "ok", service: "lookupkit", uptime: process.uptime() });
  });

  app.get("/", (_req: Request, res: Response) => {
    res.json({
      service: "lookupkit",
      description: "Phone, email, and IP verification API (Excentia)",
      endpoints: [
        "GET  /health",
        "POST /v1/verify/phone",
        "POST /v1/verify/email",
        "POST /v1/verify/ip",
      ],
    });
  });

  app.use("/v1/verify", verifyRouter);

  app.use((_req: Request, res: Response) => {
    res.status(404).json({ error: "not_found" });
  });

  return app;
}
