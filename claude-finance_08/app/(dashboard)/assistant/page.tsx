import { ChatPanel } from '@/components/assistant/chat-panel';

export default function AssistantPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-rs-fg mb-6">AI Assistant</h1>
      <ChatPanel />
    </div>
  );
}
