import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Reverse proxies in lab containers and ngrok tunnels need to forward
  // headers cleanly. Trust them.
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
};

export default nextConfig;
