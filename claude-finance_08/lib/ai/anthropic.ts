import Anthropic from '@anthropic-ai/sdk';

let client: Anthropic | null = null;

export function getAnthropicClient(): Anthropic {
  if (!client) {
    client = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY ?? 'placeholder',
      baseURL: process.env.ANTHROPIC_BASE_URL,
    });
  }
  return client;
}

export const ASSISTANT_MODEL = 'claude-sonnet-4-6';
export const ASSISTANT_MAX_TOKENS = 4096;
