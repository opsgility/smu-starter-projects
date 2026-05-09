import './globals.css';
import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import { Providers } from './providers';

const geist = Geist({ subsets: ['latin'], variable: '--font-display' });
const geistMono = Geist_Mono({ subsets: ['latin'], variable: '--font-mono' });

export const metadata: Metadata = {
  title: 'RetireScope',
  description: 'Build a retirement & portfolio app with Next.js and Claude Code.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`dark ${geist.variable} ${geistMono.variable}`}>
      <body className="bg-rs-bg text-rs-fg antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
