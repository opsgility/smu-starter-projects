import { NextRequest, NextResponse } from 'next/server';
import { getQuotes } from '@/lib/quotes/finnhub';

export const dynamic = 'force-dynamic';

export async function GET(req: NextRequest) {
  const symbolsParam = req.nextUrl.searchParams.get('symbols');
  if (!symbolsParam) {
    return NextResponse.json(
      { error: 'symbols query param required' },
      { status: 400 }
    );
  }
  const symbols = symbolsParam
    .split(',')
    .map((s) => s.trim().toUpperCase())
    .filter(Boolean);
  const quotes = await getQuotes(symbols);
  return NextResponse.json({ quotes });
}
