import Link from 'next/link';
import { Wallet } from 'lucide-react';

export function EmptyDashboard() {
  return (
    <div className="bg-rs-surface border border-rs-border rounded-2xl p-16 text-center max-w-md mx-auto">
      <div className="inline-flex size-16 items-center justify-center rounded-2xl bg-rs-card mb-4">
        <Wallet className="size-8 text-rs-fg-muted" />
      </div>
      <h2 className="text-xl font-bold text-rs-fg mb-2">
        Welcome to RetireScope
      </h2>
      <p className="text-rs-fg-muted text-sm mb-6 max-w-prose mx-auto">
        Add your first account to start tracking your portfolio. We'll fetch
        live prices and build your dashboard from there.
      </p>
      <Link
        href="/accounts/new"
        className="inline-flex items-center gap-2 rounded-lg bg-rs-primary text-rs-primary-fg px-4 py-2 text-sm font-medium"
      >
        Add an account
      </Link>
    </div>
  );
}
