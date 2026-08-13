export const metadata = { title: "Catalog" };

export default function CatalogPage() {
  return (
    <main className="section">
      <p className="kicker">Catalog</p>
      <h1>Three live products. Nothing fabricated around them.</h1>
      <div className="grid-3" style={{ marginTop: 28 }}>
        <article className="card">
          <p className="kicker">Live</p>
          <h3>Email verification</h3>
          <p>POST /v1/email — syntax, MX via DNS, disposable list.</p>
        </article>
        <article className="card">
          <p className="kicker">Live</p>
          <h3>Phone verification</h3>
          <p>POST /v1/phone — libphonenumber. Twilio Lookup if TWILIO_* is set.</p>
        </article>
        <article className="card">
          <p className="kicker">Live</p>
          <h3>IP intelligence</h3>
          <p>POST /v1/ip — ip-api.com for public IPs. MaxMind if licensed.</p>
        </article>
        <article className="card">
          <p className="kicker">Unavailable</p>
          <h3>Skip-trace</h3>
          <p>POST /v1/skip-trace returns 501. We do not invent person records.</p>
        </article>
        <article className="card">
          <p className="kicker">Unavailable</p>
          <h3>People search</h3>
          <p>POST /v1/people returns 501.</p>
        </article>
        <article className="card">
          <p className="kicker">Unavailable</p>
          <h3>Transcription</h3>
          <p>POST /v1/transcription returns 501.</p>
        </article>
      </div>
    </main>
  );
}
