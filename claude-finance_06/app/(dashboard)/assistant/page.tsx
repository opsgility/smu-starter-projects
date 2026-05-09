export default function AssistantPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-rs-fg mb-6">AI Assistant</h1>
      <div className="bg-rs-surface border border-rs-border rounded-2xl p-6">
        <h2 className="text-lg font-semibold text-rs-fg">Coming in Module 7</h2>
        <p className="text-rs-fg-muted text-sm mt-2 max-w-prose">
          Claude tool use + streaming chat. Ask "Should I rebalance?" — Claude
          calls your portfolio tools and answers grounded in real data.
        </p>
      </div>
    </div>
  );
}
