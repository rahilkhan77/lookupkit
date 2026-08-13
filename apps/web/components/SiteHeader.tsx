"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { KeystoneMark } from "./KeystoneMark";

const links = [
  { href: "/pricing", label: "Pricing" },
  { href: "/catalog", label: "Catalog" },
  { href: "/docs", label: "Docs" },
  { href: "/playground", label: "Playground" },
  { href: "/compare", label: "Compare" },
];

export function SiteHeader() {
  const path = usePathname();
  const gated = path.startsWith("/dashboard");
  return (
    <header className="site-header">
      <Link href="/" className="brand">
        <KeystoneMark />
        Lookupkit
      </Link>
      <nav className="nav" aria-label="Primary">
        {links.map((l) => (
          <Link key={l.href} href={l.href} data-active={path === l.href}>
            {l.label}
          </Link>
        ))}
      </nav>
      <div className="header-actions">
        {gated ? (
          <Link className="btn" href="/dashboard">
            Dashboard
          </Link>
        ) : (
          <>
            <Link className="btn-ghost" href="/login">
              Log in
            </Link>
            <Link className="btn btn-primary" href="/signup">
              Get a key
            </Link>
          </>
        )}
      </div>
    </header>
  );
}
