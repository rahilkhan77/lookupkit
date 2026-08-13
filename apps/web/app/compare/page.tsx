export const metadata = { title: "Compare" };

export default function ComparePage() {
  return (
    <main className="section">
      <p className="kicker">Compare</p>
      <h1>Honest sources beat a longer catalog.</h1>
      <p className="lead">
        Lookupkit is not a 1Lookup clone. We publish what actually runs in this repo.
      </p>
      <div className="table-wrap" style={{ marginTop: 28 }}>
        <table>
          <thead>
            <tr>
              <th></th>
              <th>Lookupkit</th>
              <th>Typical multi-product APIs</th>
              <th>Twilio Lookup</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Email</td>
              <td>Syntax + live MX + disposable. Vendor SMTP only with MILLIONVERIFIER_API_KEY.</td>
              <td>Often bundled SMTP claims</td>
              <td>Not the core product</td>
            </tr>
            <tr>
              <td>Phone</td>
              <td>libphonenumber. Carrier unknown unless TWILIO_* is set.</td>
              <td>Often a placeholder carrier</td>
              <td>Live line-type / carrier when you pay Twilio</td>
            </tr>
            <tr>
              <td>IP</td>
              <td>ip-api.com; MaxMind optional. meta.provider is the real source.</td>
              <td>Mixed / unnamed aggregators</td>
              <td>—</td>
            </tr>
            <tr>
              <td>Skip-trace / people / audio</td>
              <td>HTTP 501. No fake person data.</td>
              <td>Often listed as live</td>
              <td>—</td>
            </tr>
            <tr>
              <td>Brand</td>
              <td>Keystone / Excentia</td>
              <td>Varies</td>
              <td>Twilio</td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  );
}
