export const metadata = { title: "DPA" };

export default function DpaPage() {
  return (
    <>
      <p className="kicker">Legal</p>
      <h1>Data processing addendum</h1>
      <p>
        This draft DPA describes Excentia as processor for verification identifiers (email, phone,
        IP) submitted to Lookupkit. Subprocessors are listed in the dashboard status endpoint when
        adapters are enabled. A signed DPA will replace this draft before production processing of
        customer personal data at scale.
      </p>
    </>
  );
}
