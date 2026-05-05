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

  let parsed: any;
  try {
    parsed = JSON.parse(text);
  } catch {
    throw new Error('Failed to parse Claude response as JSON');
  }

  return {
    condition: parsed.condition ?? 'fair',
    summary: parsed.summary ?? 'Analysis complete.',
    defects: Array.isArray(parsed.defects) ? parsed.defects : [],
    recommendations: Array.isArray(parsed.recommendations) ? parsed.recommendations : [],
    urgency: parsed.urgency ?? 'routine',
    analyzedAt: new Date().toISOString(),
  };
}
