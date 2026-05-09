import type { NextConfig } from 'next';

// Lab containers serve the dev server through code-server's proxy at /proxy/3000.
// .env sets BASE_PATH and NEXT_PUBLIC_BASE_PATH to /proxy/3000 by default.
// Set them to "" when running through ngrok / web-tunnel which serves at root.
const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? process.env.BASE_PATH ?? '';

const nextConfig: NextConfig = {
  basePath: basePath || undefined,
  assetPrefix: basePath || undefined,
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
};

export default nextConfig;
