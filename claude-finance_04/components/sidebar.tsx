'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Wallet,
  TrendingUp,
  Calculator,
  Bot,
} from 'lucide-react';
import { cn } from '@/lib/utils';

const items = [
  { href: '/', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/accounts', label: 'Accounts', icon: Wallet },
  { href: '/projection', label: 'Projection', icon: TrendingUp },
  { href: '/tax-planner', label: 'Tax Planner', icon: Calculator },
  { href: '/assistant', label: 'AI Assistant', icon: Bot },
];

export function Sidebar() {
  const pathname = usePathname();
  return (
    <nav className="w-60 bg-rs-surface border-r border-rs-border p-4 flex flex-col gap-1">
      <div className="text-rs-fg font-display font-bold text-lg px-3 mb-4">
        RetireScope
      </div>
      {items.map(({ href, label, icon: Icon }) => {
        const active =
          pathname === href || (href !== '/' && pathname.startsWith(href));
        return (
          <Link
            key={href}
            href={href}
            className={cn(
              'flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors',
              active
                ? 'bg-rs-card text-rs-fg'
                : 'text-rs-fg-muted hover:bg-rs-card hover:text-rs-fg'
            )}
          >
            <Icon className="size-4" />
            {label}
          </Link>
        );
      })}
    </nav>
  );
}
