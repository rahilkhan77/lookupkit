"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const items = [
  { href: "/dashboard", label: "Overview" },
  { href: "/dashboard/keys", label: "API keys" },
  { href: "/dashboard/usage", label: "Usage" },
  { href: "/dashboard/billing", label: "Billing" },
];

export function DashboardShell({ children }: { children: React.ReactNode }) {
  const path = usePathname();
  return (
    <div className="dash">
      <nav className="side" aria-label="Dashboard">
        {items.map((i) => (
          <Link key={i.href} href={i.href} data-active={path === i.href}>
            {i.label}
          </Link>
        ))}
        <button
          className="btn"
          style={{ marginTop: 24 }}
          type="button"
          onClick={async () => {
            await fetch("/auth/logout", { method: "POST", credentials: "include" });
            window.location.href = "/";
          }}
        >
          Log out
        </button>
      </nav>
      <div>{children}</div>
    </div>
  );
}
