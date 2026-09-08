import path from "node:path";
import { fileURLToPath } from "node:url";

import type { NextConfig } from "next";

const applicationDirectory = path.dirname(fileURLToPath(import.meta.url));
const repositoryRoot = path.resolve(applicationDirectory, "../..");

const securityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Referrer-Policy", value: "no-referrer" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
];

const nextConfig: NextConfig = {
  output: "standalone",
  outputFileTracingRoot: repositoryRoot,
  poweredByHeader: false,
  reactStrictMode: true,
  // ========================================================
  // PREVENT DEVELOPMENT REQUEST AND BROWSER LOG FORWARDING.
  // APPLICATION AUTH EVENTS USE A SEPARATE FIXED-FIELD LOGGER.
  // ========================================================
  logging: false,
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: securityHeaders,
      },
    ];
  },
};

export default nextConfig;
