import type { NextConfig } from "next";

const api = process.env.API_URL || "http://localhost:8000";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      { source: "/v1/:path*", destination: `${api}/v1/:path*` },
      { source: "/auth/:path*", destination: `${api}/auth/:path*` },
      { source: "/account/:path*", destination: `${api}/account/:path*` },
      { source: "/billing/:path*", destination: `${api}/billing/:path*` },
      { source: "/waitlist", destination: `${api}/waitlist` },
      { source: "/public/:path*", destination: `${api}/public/:path*` },
    ];
  },
};

export default nextConfig;
