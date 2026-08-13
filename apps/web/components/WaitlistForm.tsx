"use client";

import { FormEvent, useState } from "react";

export function WaitlistForm({ compact = false }: { compact?: boolean }) {
  const [email, setEmail] = useState("");
  const [msg, setMsg] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setMsg("");
    const res = await fetch("/waitlist", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });
    if (res.ok) {
      setMsg("You’re on the list. We’ll write when keys open more widely.");
      setEmail("");
    } else {
      setMsg("Could not save that email. Try again.");
    }
  }

  return (
    <form onSubmit={onSubmit} className={compact ? "" : "form-box"}>
      <div className="field">
        <label htmlFor="waitlist-email">Work email</label>
        <input
          id="waitlist-email"
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@company.com"
        />
      </div>
      <button className="btn btn-primary" type="submit">
        Join the waitlist
      </button>
      {msg ? <p className="small ok">{msg}</p> : null}
    </form>
  );
}
