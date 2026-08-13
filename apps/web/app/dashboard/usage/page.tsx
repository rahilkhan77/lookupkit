"use client";

import { useEffect, useState } from "react";

type Row = {
  id: string;
  endpoint: string;
  credits_used: number;
  status_code: number;
  created_at: string;
};

export default function UsagePage() {
  const [rows, setRows] = useState<Row[]>([]);

  useEffect(() => {
    fetch("/account/usage", { credentials: "include" })
      .then((r) => {
        if (r.status === 401) window.location.href = "/login";
        return r.json();
      })
      .then(setRows);
  }, []);

  return (
    <main>
      <p className="kicker">Usage</p>
      <h1>Recent lookups</h1>
      <div className="table-wrap" style={{ marginTop: 20 }}>
        <table>
          <thead>
            <tr>
              <th>When</th>
              <th>Endpoint</th>
              <th>Credits</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id}>
                <td>{r.created_at}</td>
                <td className="mono">{r.endpoint}</td>
                <td>{r.credits_used}</td>
                <td>{r.status_code}</td>
              </tr>
            ))}
            {rows.length === 0 ? (
              <tr>
                <td colSpan={4}>No usage yet. Try the playground.</td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </main>
  );
}
