"use client";

import { useEffect, useState } from "react";

type Me = { email: string; credits: number };

export default function DashboardPage() {
  const [me, setMe] = useState<Me | null>(null);
  const [freshKey, setFreshKey] = useState<string | null>(null);

  useEffect(() => {
    const stored = sessionStorage.getItem("lk_new_key");
    if (stored) {
      setFreshKey(stored);
      sessionStorage.removeItem("lk_new_key");
    }
    fetch("/account/me", { credentials: "include" })
      .then((r) => {
        if (r.status === 401) window.location.href = "/login";
        return r.json();
      })
      .then(setMe)
      .catch(() => undefined);
  }, []);

  return (
    <main>
      <p className="kicker">Dashboard</p>
      <h1>Overview</h1>
      <p className="muted">{me ? me.email : "Loading…"}</p>
      <div className="grid-2" style={{ marginTop: 24 }}>
        <article className="card">
          <p className="kicker">Credits</p>
          <div className="price">{me ? me.credits.toLocaleString() : "—"}</div>
          <p className="small muted">Trial credits on signup. Top up from Billing.</p>
        </article>
        <article className="card">
          <p className="kicker">Sources</p>
          <p>Email: syntax + DNS MX. Phone: libphonenumber. IP: ip-api.com for public addresses.</p>
        </article>
      </div>
      {freshKey ? (
        <div className="banner" style={{ marginTop: 24 }}>
          <strong>Your test key (shown once):</strong>
          <p className="mono">{freshKey}</p>
        </div>
      ) : null}
    </main>
  );
}
