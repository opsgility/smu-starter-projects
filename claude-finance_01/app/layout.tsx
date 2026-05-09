import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'RetireScope',
  description: 'Build a retirement & portfolio app with Next.js and Claude Code.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
