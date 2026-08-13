"use client";

import { FormEvent, useState } from "react";

type Kind = "email" | "phone" | "ip";

export default function PlaygroundPage() {
  const [kind, setKind] = useState<Kind>("email");
  const [key, setKey] = useState("");
  const [value, setValue] = useState("");
  const [out, setOut] = useState("Run a lookup to see JSON here.");
  const [status, setStatus] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    const body =
      kind === "email" ? { email: value } : kind === "phone" ? { phone: value } : { ip: value };
    const res = await fetch(`/v1/${kind}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${key}`,
      },
      body: JSON.stringify(body),
    });
    setStatus(`${res.status}`);
    const data = await res.json();
    setOut(JSON.stringify(data, null, 2));
  }

  return (
    <main className="section">
      <p className="kicker">Playground</p>
      <h1>Try the kit.</h1>
      <p className="lead">Paste a test key from the dashboard. Requests stay on this origin.</p>
      <form onSubmit={onSubmit} className="split" style={{ marginTop: 28 }}>
        <div>
          <div className="field">
            <label>Endpoint</label>
            <select value={kind} onChange={(e) => setKind(e.target.value as Kind)}>
              <option value="email">POST /v1/email</option>
              <option value="phone">POST /v1/phone</option>
              <option value="ip">POST /v1/ip</option>
            </select>
          </div>
          <div className="field">
            <label>API key</label>
            <input
              value={key}
              onChange={(e) => setKey(e.target.value)}
              placeholder="lk_test_…"
              required
              autoComplete="off"
            />
          </div>
          <div className="field">
            <label>{kind === "email" ? "Email" : kind === "phone" ? "Phone" : "IP"}</label>
            <input
              value={value}
              onChange={(e) => setValue(e.target.value)}
              placeholder={kind === "email" ? "hello@example.com" : kind === "phone" ? "+16502530000" : "8.8.8.8"}
              required
            />
          </div>
          <button className="btn btn-primary" type="submit">
            Run lookup
          </button>
          {status ? <p className="small muted">HTTP {status}</p> : null}
        </div>
        <pre className="code">{out}</pre>
      </form>
    </main>
  );
}
