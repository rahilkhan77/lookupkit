export const metadata = { title: "About" };

export default function AboutPage() {
  return (
    <main className="section">
      <p className="kicker">About</p>
      <h1>A small kit from Excentia.</h1>
      <p className="lead">
        Lookupkit is a Keystone-branded developer API for verifying phones, emails, and IPs. It is
        built by Excentia, founded by Rahil Khan.
      </p>
      <div className="split" style={{ marginTop: 36 }}>
        <article className="card">
          <h3>Why Keystone, not a clone</h3>
          <p className="muted">
            The market is full of dark-mode catalogs that promise skip-tracing, social graphs, and
            FCC-direct carrier feeds. Lookupkit ships what it can prove: libraries, live DNS, and
            env-gated vendors. The keystone is the piece that actually holds the arch.
          </p>
        </article>
        <article className="card">
          <h3>Parent company</h3>
          <p className="muted">
            Excentia builds focused software products. Parent site:{" "}
            <a href="https://excentia.site">excentia.site</a>. Lookupkit.ai is the verification
            surface — not a visual copy of 1Lookup.
          </p>
        </article>
      </div>
    </main>
  );
}
