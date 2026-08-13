import Link from "next/link";

const plans = [
  { id: "starter", name: "Starter", usd: 99, credits: "20,000", note: "For a single product surface." },
  { id: "growth", name: "Growth", usd: 299, credits: "85,000", note: "Most teams start here.", featured: true },
  { id: "pro", name: "Pro", usd: 799, credits: "250,000", note: "Higher volume, same endpoints." },
  { id: "enterprise", name: "Enterprise", usd: 1999, credits: "1,000,000", note: "Contract and invoicing via Excentia." },
];

export const metadata = { title: "Pricing" };

export default function PricingPage() {
  return (
    <main className="section">
      <p className="kicker">Pricing</p>
      <h1>Credits, not a maze of SKUs.</h1>
      <p className="lead">
        One pool of credits across email, phone, and IP. Checkout uses Stripe test keys only unless
        you explicitly enable live mode. No charges happen without keys.
      </p>
      <div className="grid-4" style={{ marginTop: 36 }}>
        {plans.map((p) => (
          <article key={p.id} className={`card ${p.featured ? "featured" : ""}`}>
            <p className="kicker">{p.name}</p>
            <div className="price">
              ${p.usd} <span>/ mo</span>
            </div>
            <p>
              <strong>{p.credits}</strong> credits
            </p>
            <p className="muted small">{p.note}</p>
            <Link className="btn btn-primary" href="/dashboard/billing">
              Choose {p.name}
            </Link>
          </article>
        ))}
      </div>
      <p className="small muted" style={{ marginTop: 28 }}>
        Lookups cost 1 credit. Signup includes trial credits. Skip-trace, people search, and
        transcription are not sold — they return HTTP 501.
      </p>
    </main>
  );
}
