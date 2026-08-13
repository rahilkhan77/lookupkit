export default function LegalLayout({ children }: { children: React.ReactNode }) {
  return (
    <main className="section">
      <div className="banner banner-draft" role="status">
        <strong>DRAFT.</strong> This document is a working draft for the Lookupkit MVP. It is not
        legal advice and is not a fully executed policy.
      </div>
      {children}
    </main>
  );
}
