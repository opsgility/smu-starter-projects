'use client';

import { AlertTriangle, RotateCw } from 'lucide-react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="bg-rs-surface border border-rs-border rounded-2xl p-12 text-center max-w-md mx-auto">
      <div className="inline-flex size-12 items-center justify-center rounded-2xl bg-rs-danger/10 mb-4">
        <AlertTriangle className="size-6 text-rs-danger" />
      </div>
      <h2 className="text-lg font-bold text-rs-fg mb-2">
        Couldn't load your dashboard
      </h2>
      <p className="text-rs-fg-muted text-sm">{error.message}</p>
      {error.digest && (
        <p className="text-rs-fg-dim text-xs mt-1">
          Reference: {error.digest}
        </p>
      )}
      <button
        onClick={reset}
        className="mt-6 inline-flex items-center gap-2 rounded-lg bg-rs-primary text-rs-primary-fg px-4 py-2 text-sm font-medium"
      >
        <RotateCw className="size-4" /> Try again
      </button>
    </div>
  );
}
