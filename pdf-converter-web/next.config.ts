import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  
  // Puppeteer and other Node.js native modules should not be bundled
  // for the client side. They're only used in API routes (server-side).
  serverExternalPackages: ['puppeteer'],

  // Increase body parser limit for large HTML documents
  experimental: {
    serverActions: {
      bodySizeLimit: '10mb',
    },
  },
};

export default nextConfig;
