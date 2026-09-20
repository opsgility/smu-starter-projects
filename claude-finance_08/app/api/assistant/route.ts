import { NextRequest } from 'next/server';
import {
  getAnthropicClient,
  ASSISTANT_MODEL,
  ASSISTANT_MAX_TOKENS,
} from '@/lib/ai/anthropic';
import { SYSTEM_PROMPT } from '@/lib/ai/system-prompt';
import { TOOLS } from '@/lib/ai/tools';
import { handleToolCall } from '@/lib/ai/tool-handlers';
import type Anthropic from '@anthropic-ai/sdk';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string | Anthropic.MessageParam['content'];
}

function sseEvent(event: string, data: unknown): string {
  return `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;
}

export async function POST(req: NextRequest) {
  const { messages } = (await req.json()) as { messages: ChatMessage[] };
  const client = getAnthropicClient();

  const stream = new ReadableStream({
    async start(controller) {
      const enc = new TextEncoder();
      const send = (event: string, data: unknown) =>
        controller.enqueue(enc.encode(sseEvent(event, data)));

      const conversation: Anthropic.MessageParam[] = messages.map((m) => ({
        role: m.role,
        content: m.content as Anthropic.MessageParam['content'],
      }));

      try {
        let iterations = 0;
        while (iterations < 10) {
          iterations += 1;

          const response = await client.messages.create({
            model: ASSISTANT_MODEL,
            max_tokens: ASSISTANT_MAX_TOKENS,
            system: SYSTEM_PROMPT,
            tools: TOOLS,
            messages: conversation,
          });

          for (const block of response.content) {
            if (block.type === 'text') {
              send('text', { text: block.text });
            } else if (block.type === 'tool_use') {
              send('tool_use', { name: block.name, input: block.input });
            }
          }

          if (response.stop_reason !== 'tool_use') {
            send('done', { stop_reason: response.stop_reason });
            break;
          }

          conversation.push({ role: 'assistant', content: response.content });

          const toolResults: Anthropic.ToolResultBlockParam[] = [];
          for (const block of response.content) {
            if (block.type === 'tool_use') {
              const result = await handleToolCall(
                block.name,
                block.input as Record<string, unknown>
              );
              send('tool_result', { name: block.name, result });
              toolResults.push({
                type: 'tool_result',
                tool_use_id: block.id,
                content: result,
              });
            }
          }
          conversation.push({ role: 'user', content: toolResults });
        }
      } catch (e) {
        const err = e as Error;
        // Log to the dev terminal so the failure isn't invisible — the SSE
        // error event handles client-side surfacing.
        console.error('[assistant] error:', err.message, err.stack);
        send('error', { message: err.message });
      } finally {
        controller.close();
      }
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache, no-transform',
      Connection: 'keep-alive',
    },
  });
}
