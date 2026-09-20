export default function Dashboard() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-rs-fg mb-6">Dashboard</h1>
      <div className="bg-rs-surface border border-rs-border rounded-2xl p-6 max-w-md">
        <div className="text-rs-fg-dim text-xs uppercase tracking-wide">Total Value</div>
        <div className="font-mono tabular text-3xl text-rs-fg mt-2">$1,247,390.42</div>
        <div className="font-mono tabular text-rs-accent text-sm mt-1">
          +$3,247.18 (+0.26%)
        </div>
        <p className="text-rs-fg-muted text-sm mt-6">
          This is a placeholder card. The real dashboard ships in Lesson 7 — it
          renders KPI tiles, allocation pies, and a live holdings table.
        </p>
      </div>
    </div>
  );
}
