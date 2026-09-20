import { eq } from 'drizzle-orm';
import { db } from '@/lib/db/client';
import { quoteCache } from '@/lib/db/schema';

const FINNHUB_BASE = 'https://finnhub.io/api/v1';
const TTL_MS = 60_000;

export type QuoteErrorCode =
  | 'NO_KEY'
  | 'RATE_LIMITED'
  | 'UNKNOWN_SYMBOL'
  | 'NETWORK';

export class QuoteError extends Error {
  constructor(public code: QuoteErrorCode, message: string) {
    super(message);
    this.name = 'QuoteError';
  }
}

export interface Quote {
  symbol: string;
  price: number;
  changePct: number | null;
  fetchedAt: Date;
}

export type QuoteOrError = Quote | { symbol: string; error: QuoteErrorCode };

export async function fetchQuote(symbol: string): Promise<Quote> {
  const apiKey = process.env.FINNHUB_API_KEY;
  if (!apiKey) {
    throw new QuoteError('NO_KEY', 'FINNHUB_API_KEY env var is not set');
  }

  let res: Response;
  try {
    res = await fetch(
      `${FINNHUB_BASE}/quote?symbol=${encodeURIComponent(symbol)}&token=${apiKey}`,
      { cache: 'no-store' }
    );
  } catch (e) {
    throw new QuoteError(
      'NETWORK',
      `Network error fetching ${symbol}: ${(e as Error).message}`
    );
  }

  if (res.status === 429) {
    throw new QuoteError('RATE_LIMITED', `Finnhub rate limit hit for ${symbol}`);
  }
  if (!res.ok) {
    throw new QuoteError(
      'NETWORK',
      `Finnhub returned ${res.status} for ${symbol}`
    );
  }

  const data = (await res.json()) as {
    c: number;
    dp: number | null;
    t: number;
  };
  if (data.c === 0 && data.t === 0) {
    throw new QuoteError(
      'UNKNOWN_SYMBOL',
      `Finnhub doesn't recognize symbol ${symbol}`
    );
  }

  return {
    symbol,
    price: data.c,
    changePct: data.dp != null ? data.dp / 100 : null,
    fetchedAt: new Date(),
  };
}

export async function getQuote(symbol: string): Promise<QuoteOrError> {
  const sym = symbol.trim().toUpperCase();

  const [cached] = await db
    .select()
    .from(quoteCache)
    .where(eq(quoteCache.symbol, sym))
    .limit(1);

  const cachedFresh =
    cached && Date.now() - cached.fetchedAt.getTime() < TTL_MS;

  if (cachedFresh) {
    return cachedToQuote(cached);
  }

  try {
    const fresh = await fetchQuote(sym);
    await db
      .insert(quoteCache)
      .values({
        symbol: fresh.symbol,
        price: fresh.price.toString(),
        changePct: fresh.changePct?.toString() ?? null,
        fetchedAt: fresh.fetchedAt,
      })
      .onConflictDoUpdate({
        target: quoteCache.symbol,
        set: {
          price: fresh.price.toString(),
          changePct: fresh.changePct?.toString() ?? null,
          fetchedAt: fresh.fetchedAt,
        },
      });
    return fresh;
  } catch (e) {
    if (cached) {
      // Stale cache better than nothing
      console.warn(
        `[quotes] using stale cache for ${sym}: ${(e as Error).message}`
      );
      return cachedToQuote(cached);
    }
    return {
      symbol: sym,
      error: e instanceof QuoteError ? e.code : 'NETWORK',
    };
  }
}

export async function getQuotes(symbols: string[]): Promise<QuoteOrError[]> {
  return Promise.all(symbols.map(getQuote));
}

function cachedToQuote(cached: {
  symbol: string;
  price: string;
  changePct: string | null;
  fetchedAt: Date;
}): Quote {
  return {
    symbol: cached.symbol,
    price: parseFloat(cached.price),
    changePct: cached.changePct ? parseFloat(cached.changePct) : null,
    fetchedAt: cached.fetchedAt,
  };
}
