import { File } from 'expo-file-system';
import { PhotoAnalysis } from '@/types';

// Default to Anthropic's public API. In a SkillMeUp lab, startup.sh injects
// EXPO_PUBLIC_CLAUDE_API_URL pointing at the lab's Claude proxy, and Metro
// inlines that into the bundle at build time — so the same code calls the
// proxy in the lab and Anthropic directly when run elsewhere.
const API_URL =
  process.env.EXPO_PUBLIC_CLAUDE_API_URL ?? 'https://api.anthropic.com/v1/messages';
const MODEL = 'claude-sonnet-4-6';

async function toBase64(uri: string): Promise<string> {
  return await new File(uri).base64();
}

function extractJson(text: string): any {
  // 1. Direct parse — Claude returned pure JSON.
  try { return JSON.parse(text); } catch {}

  // 2. Strip markdown code fence (```json ... ``` or ``` ... ```).
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)\s*```/i);
  if (fenced) {
    try { return JSON.parse(fenced[1]); } catch {}
  }

  // 3. Last resort — slice from first '{' to last '}'.
  const start = text.indexOf('{');
  const end = text.lastIndexOf('}');
  if (start !== -1 && end > start) {
    try { return JSON.parse(text.slice(start, end + 1)); } catch {}
  }

  throw new Error(
    `Failed to parse Claude response as JSON. Response was: ${text.slice(0, 500)}`
  );
}

export async function analyzeInspectionPhoto(
  photoUri: string,
  equipmentName: string,
  equipmentType: string,
  apiKey: string
): Promise<PhotoAnalysis> {
  const base64 = await toBase64(photoUri);

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'content-type': 'application/json',
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 1024,
      messages: [
        {
          role: 'user',
          content: [
            {
              type: 'image',
              source: { type: 'base64', media_type: 'image/jpeg', data: base64 },
            },
            {
              type: 'text',
              text: `You are an expert field inspector analyzing a photo of ${equipmentName} (type: ${equipmentType}).

Analyze this image and respond with a JSON object in this exact format:
{
  "condition": "good" | "fair" | "poor" | "critical",
  "summary": "One sentence summary of what you see",
  "defects": ["list", "of", "observed", "defects"],
  "recommendations": ["list", "of", "recommended", "actions"],
  "urgency": "routine" | "soon" | "immediate"
}

Only respond with the JSON object, no other text.`,
            },
          ],
        },
      ],
    }),
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`Claude API error ${response.status}: ${err}`);
  }

  const data = await response.json();
  const text = data.content[0].text.trim();

  // Claude often wraps JSON in markdown fences (```json ... ```) or adds a
  // sentence of preamble even when told not to. Try a strict parse first, then
  // strip fences, then fall back to the first balanced {...} block.
  const parsed = extractJson(text);

  return {
    condition: parsed.condition ?? 'fair',
    summary: parsed.summary ?? 'Analysis complete.',
    defects: Array.isArray(parsed.defects) ? parsed.defects : [],
    recommendations: Array.isArray(parsed.recommendations) ? parsed.recommendations : [],
    urgency: parsed.urgency ?? 'routine',
    analyzedAt: new Date().toISOString(),
  };
}
