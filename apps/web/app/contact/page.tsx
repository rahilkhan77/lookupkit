"use client";

import { FormEvent, useState } from "react";

export default function ContactPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [msg, setMsg] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    const res = await fetch("/public/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, message }),
    });
    setMsg(res.ok ? "Received. We’ll reply from Excentia." : "Could not send. Try again.");
    if (res.ok) {
      setName("");
      setEmail("");
      setMessage("");
    }
  }

  return (
    <main className="section">
      <p className="kicker">Contact</p>
      <h1>Write to Excentia.</h1>
      <p className="lead">Founder: Rahil Khan. Product questions, enterprise credits, or vendor keys.</p>
      <form className="form-box" onSubmit={onSubmit} style={{ marginTop: 28 }}>
        <div className="field">
          <label htmlFor="name">Name</label>
          <input id="name" value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        <div className="field">
          <label htmlFor="email">Email</label>
          <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div className="field">
          <label htmlFor="message">Message</label>
          <textarea id="message" value={message} onChange={(e) => setMessage(e.target.value)} required />
        </div>
        <button className="btn btn-primary" type="submit">
          Send
        </button>
        {msg ? <p className="small">{msg}</p> : null}
      </form>
    </main>
  );
}
