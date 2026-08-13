export const metadata = { title: "Docs" };

export default function DocsPage() {
  return (
    <main className="section">
      <p className="kicker">Docs</p>
      <h1>One key. Three lookups.</h1>
      <p className="lead">
        Authenticate with <code>Authorization: Bearer lk_test_…</code> or <code>X-API-Key</code>.
        Each successful lookup costs 1 credit.
      </p>

      <h2 style={{ marginTop: 40 }}>Email</h2>
      <pre className="code">{`curl -X POST $API/v1/email \\
  -H "Authorization: Bearer lk_test_…" \\
  -H "Content-Type: application/json" \\
  -d '{"email": "hello@example.com"}'`}</pre>
      <p className="muted">Returns syntax_valid, mx_found (live DNS), mx_records, disposable, deliverable.</p>

      <h2>Phone</h2>
      <pre className="code">{`curl -X POST $API/v1/phone \\
  -H "Authorization: Bearer lk_test_…" \\
  -H "Content-Type: application/json" \\
  -d '{"phone": "+16502530000"}'`}</pre>
      <p className="muted">
        carrier is null / carrier_status unknown when libphonenumber has no prefix metadata. Twilio
        Lookup is used only if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN are set.
      </p>

      <h2>IP</h2>
      <pre className="code">{`curl -X POST $API/v1/ip \\
  -H "Authorization: Bearer lk_test_…" \\
  -H "Content-Type: application/json" \\
  -d '{"ip": "8.8.8.8"}'`}</pre>
      <p className="muted">
        Public IPs query ip-api.com and set meta.provider to &quot;ip-api.com&quot;. Private, loopback, and
        reserved addresses are classified locally.
      </p>

      <h2>Unavailable</h2>
      <p>
        <code>POST /v1/skip-trace</code>, <code>/v1/people</code>, <code>/v1/transcription</code>{" "}
        return <strong>501</strong> with an explicit unavailable payload.
      </p>
    </main>
  );
}
