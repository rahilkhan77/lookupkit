import { WaitlistForm } from "@/components/WaitlistForm";
import Link from "next/link";

export default function HomePage() {
  return (
    <main>
      <section className="hero">
        <div>
          <p className="kicker">Keystone · Excentia</p>
          <h1>Phone, email, IP. That’s the kit.</h1>
          <p className="lead">
            Lookupkit is a focused verification API for developers. Syntax, live DNS, and honest
            metadata — not a 41-product catalog of invented people.
          </p>
          <div style={{ marginTop: 28 }}>
            <WaitlistForm />
          </div>
          <p className="small muted" style={{ marginTop: 12 }}>
            Already building? <Link href="/signup">Create an account</Link> for a test key, or read the{" "}
            <Link href="/docs">docs</Link>.
          </p>
        </div>
        <aside className="hero-panel">
          <p className="kicker" style={{ color: "#d9d0c1" }}>
            POST /v1/email
          </p>
          <h3>What you get back</h3>
          <pre className="code">{`{
  "syntax_valid": true,
  "mx_found": true,
  "disposable": false,
  "deliverable": "unknown",
  "meta": {
    "provider": "lookupkit.local"
  }
}`}</pre>
          <p className="small">
            Deliverable stays <em>unknown</em> until you attach a vendor key. We will not pretend we
            SMTP-probed the mailbox.
          </p>
        </aside>
      </section>

      <section className="section" style={{ paddingTop: 0 }}>
        <div className="grid-3">
          <article className="card">
            <h3>Email</h3>
            <p className="muted">Syntax, live MX, disposable domains. MillionVerifier only if you set the env key.</p>
          </article>
          <article className="card">
            <h3>Phone</h3>
            <p className="muted">libphonenumber parse, region, line type. Carrier is unknown unless Twilio is on — never “Example Wireless”.</p>
          </article>
          <article className="card">
            <h3>IP</h3>
            <p className="muted">ip-api.com for public addresses. Private ranges stay local. <code>meta.provider</code> names the real source.</p>
          </article>
        </div>
      </section>
    </main>
  );
}
