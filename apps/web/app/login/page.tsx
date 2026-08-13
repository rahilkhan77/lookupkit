"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setErr("");
    const res = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, password }),
    });
    if (res.ok) {
      window.location.href = "/dashboard";
      return;
    }
    const data = await res.json().catch(() => ({}));
    setErr(data.detail || "Could not log in");
  }

  return (
    <main className="section">
      <p className="kicker">Account</p>
      <h1>Log in</h1>
      <form className="form-box" onSubmit={onSubmit}>
        <div className="field">
          <label htmlFor="email">Email</label>
          <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div className="field">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            minLength={8}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button className="btn btn-primary" type="submit">
          Log in
        </button>
        <p className="notice">{err}</p>
        <p className="small muted">
          No account? <Link href="/signup">Sign up</Link>
        </p>
      </form>
    </main>
  );
}
