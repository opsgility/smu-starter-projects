import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Lab containers expose the dev server through ngrok at lab-<session>.skillmeup.ngrok.app.
  // Without this allowlist Next.js's dev-mode same-origin guard rejects Server Actions,
  // fonts (/_next/static/media/*.woff2), and the HMR WebSocket as cross-origin.
  allowedDevOrigins: [
    '*.ngrok.app',
    '*.ngrok-free.app',
    '*.ngrok.io',
    '*.skillmeup.ngrok.app',
  ],
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
};

export default nextConfig;
