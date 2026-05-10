'use client';

import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send, Wrench } from 'lucide-react';

interface ChatTurn {
  role: 'user' | 'assistant';
  content: string;
  toolCalls?: { name: string; input: Record<string, unknown> }[];
}

export function ChatPanel() {
  const [turns, setTurns] = useState<ChatTurn[]>([
    {
      role: 'assistant',
      content:
        "Hi! I'm RetireScope. Ask me about your portfolio, allocation, retirement projection, or tax-aware withdrawals.",
    },
  ]);
  const [input, setInput] = useState('');
  const [streaming, setStreaming] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo(0, scrollRef.current.scrollHeight);
  }, [turns, streaming]);

  async function send() {
    if (!input.trim() || streaming) return;
    const userTurn: ChatTurn = { role: 'user', content: input.trim() };
    const next: ChatTurn[] = [...turns, userTurn, { role: 'assistant', content: '', toolCalls: [] }];
    setTurns(next);
    setInput('');
    setStreaming(true);

    try {
      const res = await fetch('/api/assistant', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          // Drop turns with no payload (the empty placeholder assistant turn
          // we appended to stream into), then drop the first turn — it's a
          // UI-only welcome greeting, not a real Claude response. The API
          // requires the conversation to start AND end with a user message.
          messages: next
            .filter((t) => t.content || t.toolCalls?.length)
            .slice(1)
            .map((t) => ({ role: t.role, content: t.content })),
        }),
      });
      if (!res.body) throw new Error('No response body');

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const blocks = buffer.split('\n\n');
        buffer = blocks.pop() ?? '';
        for (const block of blocks) {
          const eventLine = block.split('\n').find((l) => l.startsWith('event: '));
          const dataLine = block.split('\n').find((l) => l.startsWith('data: '));
          if (!eventLine || !dataLine) continue;
          const event = eventLine.slice('event: '.length);
          const data = JSON.parse(dataLine.slice('data: '.length));

          setTurns((prev) => {
            const updated = [...prev];
            const last = { ...updated[updated.length - 1] };
            if (event === 'text') {
              last.content = (last.content ?? '') + data.text;
            } else if (event === 'tool_use') {
              last.toolCalls = [...(last.toolCalls ?? []), { name: data.name, input: data.input }];
            } else if (event === 'error') {
              last.content = `Error: ${data.message}`;
            }
            updated[updated.length - 1] = last;
            return updated;
          });
        }
      }
    } catch (e) {
      setTurns((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: 'assistant',
          content: `Error: ${(e as Error).message}`,
        };
        return updated;
      });
    } finally {
      setStreaming(false);
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] bg-rs-surface border border-rs-border rounded-2xl">
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-4">
        {turns.map((t, i) => (
          <div key={i} className={t.role === 'user' ? 'flex justify-end' : ''}>
            <div
              className={
                t.role === 'user'
                  ? 'bg-rs-primary/20 border border-rs-primary/40 text-rs-fg rounded-2xl px-4 py-2 max-w-[75%]'
                  : 'text-rs-fg max-w-[85%]'
              }
            >
              {t.toolCalls?.map((tc, j) => (
                <div
                  key={j}
                  className="flex items-center gap-2 text-rs-fg-dim text-xs mb-2 bg-rs-card border border-rs-border rounded-lg px-2 py-1 w-fit"
                >
                  <Wrench className="w-3 h-3" />
                  <span className="font-mono">{tc.name}</span>
                </div>
              ))}
              {t.content && (
                <div className="prose prose-invert prose-sm max-w-none">
                  <ReactMarkdown>{t.content}</ReactMarkdown>
                </div>
              )}
            </div>
          </div>
        ))}
        {streaming && (
          <div className="text-rs-fg-dim text-sm animate-pulse">Thinking...</div>
        )}
      </div>
      <div className="border-t border-rs-border p-4 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && send()}
          disabled={streaming}
          placeholder="Ask about your portfolio..."
          className="flex-1 bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg disabled:opacity-50"
        />
        <button
          onClick={send}
          disabled={streaming || !input.trim()}
          className="bg-rs-primary text-rs-primary-fg rounded-lg px-4 py-2 font-medium disabled:opacity-50"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
