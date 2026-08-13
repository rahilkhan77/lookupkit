export const metadata = { title: "Terms" };

export default function TermsPage() {
  return (
    <>
      <p className="kicker">Legal</p>
      <h1>Terms of use</h1>
      <p>
        Lookupkit is provided as an MVP. Credits are a metering unit, not a stored-value balance
        with cash redemption. Skip-trace, people search, and transcription are unavailable. You
        must not use the API to harass individuals, bypass consent, or fabricate downstream
        identity records.
      </p>
      <p>Stripe charges occur only when a valid key is configured. Live keys require STRIPE_LIVE=1.</p>
    </>
  );
}
