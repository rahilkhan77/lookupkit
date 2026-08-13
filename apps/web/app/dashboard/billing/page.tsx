"use client";

import { useEffect, useState } from "react";

type Plan = { id: string; name: string; usd: number; credits: number };

export default function BillingPage() {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [ready, setReady] = useState(false);
  const [note, setNote] = useState("");
  const [msg, setMsg] = useState("");

  useEffect(() => {
    fetch("/billing/plans")
      .then((r) => r.json())
      .then((d) => {
        setPlans(d.plans || []);
        setReady(Boolean(d.stripe_ready));
        setNote(d.note || "");
      });
  }, []);

  async function checkout(plan: string) {
    setMsg("");
    const res = await fetch("/billing/checkout", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ plan }),
    });
    const data = await res.json();
    if (res.ok && data.checkout_url) {
      window.location.href = data.checkout_url;
      return;
    }
    setMsg(data.detail || "Checkout is not available.");
  }

  return (
    <main>
      <p className="kicker">Billing</p>
      <h1>Credits</h1>
      <p className="muted">{note}</p>
      <p className="small">{ready ? "Stripe test checkout is configured." : "No Stripe key — you will not be charged."}</p>
      <div className="grid-2" style={{ marginTop: 20 }}>
        {plans.map((p) => (
          <article key={p.id} className="card">
            <h3>{p.name}</h3>
            <div className="price">
              ${p.usd} <span>/ {p.credits.toLocaleString()} credits</span>
            </div>
            <button className="btn btn-primary" type="button" onClick={() => checkout(p.id)}>
              Checkout
            </button>
          </article>
        ))}
      </div>
      {msg ? <p className="notice">{msg}</p> : null}
    </main>
  );
}
