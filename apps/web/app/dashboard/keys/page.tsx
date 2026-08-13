"use client";

import { FormEvent, useEffect, useState } from "react";

type KeyRow = {
  id: string;
  name: string;
  prefix: string;
  hint: string;
  revoked: boolean;
  created_at: string;
};

export default function KeysPage() {
  const [keys, setKeys] = useState<KeyRow[]>([]);
  const [created, setCreated] = useState<string | null>(null);
  const [name, setName] = useState("playground");
  const [live, setLive] = useState(false);

  async function load() {
    const res = await fetch("/account/keys", { credentials: "include" });
    if (res.status === 401) window.location.href = "/login";
    setKeys(await res.json());
  }

  useEffect(() => {
    load();
  }, []);

  async function onCreate(e: FormEvent) {
    e.preventDefault();
    const res = await fetch("/account/keys", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, live }),
    });
    const data = await res.json();
    setCreated(data.key);
    load();
  }

  async function revoke(id: string) {
    await fetch(`/account/keys/${id}`, { method: "DELETE", credentials: "include" });
    load();
  }

  return (
    <main>
      <p className="kicker">Keys</p>
      <h1>API keys</h1>
      <p className="muted">Prefixes: lk_test_ and lk_live_. Only the hash is stored.</p>
      <form onSubmit={onCreate} className="card" style={{ margin: "20px 0" }}>
        <div className="field">
          <label>Name</label>
          <input value={name} onChange={(e) => setName(e.target.value)} />
        </div>
        <div className="field">
          <label>
            <input type="checkbox" checked={live} onChange={(e) => setLive(e.target.checked)} /> lk_live_
          </label>
        </div>
        <button className="btn btn-primary" type="submit">
          Create key
        </button>
      </form>
      {created ? (
        <div className="banner">
          Full key (once): <span className="mono">{created}</span>
        </div>
      ) : null}
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Hint</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {keys.map((k) => (
              <tr key={k.id}>
                <td>{k.name}</td>
                <td className="mono">{k.hint}</td>
                <td>{k.revoked ? "revoked" : "active"}</td>
                <td>
                  {!k.revoked ? (
                    <button className="btn" type="button" onClick={() => revoke(k.id)}>
                      Revoke
                    </button>
                  ) : null}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
