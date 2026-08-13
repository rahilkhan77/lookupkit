export const metadata = { title: "Privacy" };

export default function PrivacyPage() {
  return (
    <>
      <p className="kicker">Legal</p>
      <h1>Privacy policy</h1>
      <p>
        Lookupkit (Excentia) stores account emails, hashed passwords, API key hashes, and lookup
        usage metadata. Verification requests may be sent to env-gated vendors (MillionVerifier,
        Twilio, MaxMind, ip-api.com) only when those adapters are enabled. Do not send special
        category data or content you are not authorized to process.
      </p>
      <p>Contact: the form on /contact. Parent: Excentia (excentia.site). Founder: Rahil Khan.</p>
    </>
  );
}
