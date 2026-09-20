export default function Loading() {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[0, 1, 2, 3].map((i) => (
          <div
            key={i}
            className="h-28 bg-rs-surface border border-rs-border rounded-2xl"
          />
        ))}
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="h-72 bg-rs-surface border border-rs-border rounded-2xl" />
        <div className="h-72 bg-rs-surface border border-rs-border rounded-2xl" />
      </div>
      <div className="h-96 bg-rs-surface border border-rs-border rounded-2xl" />
    </div>
  );
}
