import Link from "next/link";

export function SiteFooter() {
  return (
    <footer className="footer">
      <div className="footer-grid">
        <div>
          <strong>Lookupkit</strong>
          <p>A Keystone product by Excentia. Phone, email, and IP verification without invented data.</p>
        </div>
        <div>
          <div>Product</div>
          <p>
            <Link href="/pricing">Pricing</Link>
            <br />
            <Link href="/catalog">Catalog</Link>
            <br />
            <Link href="/docs">Docs</Link>
            <br />
            <Link href="/playground">Playground</Link>
          </p>
        </div>
        <div>
          <div>Company</div>
          <p>
            <Link href="/about">About</Link>
            <br />
            <Link href="/contact">Contact</Link>
            <br />
            <Link href="/compare">Compare</Link>
            <br />
            <a href="https://excentia.site">Excentia</a>
          </p>
        </div>
        <div>
          <div>Legal</div>
          <p>
            <Link href="/legal/terms">Terms</Link>
            <br />
            <Link href="/legal/privacy">Privacy</Link>
            <br />
            <Link href="/legal/dpa">DPA</Link>
          </p>
        </div>
      </div>
      <p style={{ marginTop: 28 }}>© {new Date().getFullYear()} Excentia. Lookupkit is a Keystone brand. Founder: Rahil Khan.</p>
    </footer>
  );
}
