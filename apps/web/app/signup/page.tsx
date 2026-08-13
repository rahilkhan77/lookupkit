"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setErr("");
    const res = await fetch("/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, password }),
    });
    if (res.ok) {
      const data = await res.json();
      if (data.api_key) sessionStorage.setItem("lk_new_key", data.api_key);
      window.location.href = "/dashboard";
      return;
    }
    const data = await res.json().catch(() => ({}));
    setErr(typeof data.detail === "string" ? data.detail : "Could not sign up");
  }

  return (
    <main className="section">
      <p className="kicker">Account</p>
      <h1>Create an account</h1>
      <p className="lead">Email and password. We’ll hash it, set an httpOnly session cookie, and issue a test key.</p>
      <form className="form-box" onSubmit={onSubmit}>
        <div className="field">
          <label htmlFor="email">Email</label>
          <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div className="field">
          <label htmlFor="password">Password (8+)</label>
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
          Sign up
        </button>
        <p className="notice">{err}</p>
        <p className="small muted">
          Already have an account? <Link href="/login">Log in</Link>
        </p>
      </form>
    </main>
  );
}
