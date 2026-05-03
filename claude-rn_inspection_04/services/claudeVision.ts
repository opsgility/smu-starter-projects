import * as FileSystem from 'expo-file-system';
import { PhotoAnalysis } from '@/types';

const API_URL = 'https://api.anthropic.com/v1/messages';

async function toBase64(uri: string): Promise<string> {
  return await FileSystem.readAsStringAsync(uri, { encoding: FileSystem.EncodingType.Base64 });
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
      model: 'claude-sonnet-4-6',
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
