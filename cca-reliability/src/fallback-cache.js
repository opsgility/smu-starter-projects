// TODO: Step 3 — Implement the FallbackCache class
// A simple LRU-style in-memory cache for storing recent successful API responses
//
// constructor(maxSize): default 100 entries
// store(key, value): add to cache, evict oldest if at capacity
// get(key): return cached value with _fromCache: true and _cachedAt timestamp, or null
// generateKey(documentText): hash the first 200 chars of text to produce a string key

class FallbackCache {
  constructor(maxSize = 100) {
    this.cache = new Map();
    this.maxSize = maxSize;
    // TODO: initialize additional state as needed
  }

  store(key, value) {
    // TODO: implement — evict oldest entry if at capacity, then store
  }

  get(key) {
    // TODO: implement — return { ...value, _fromCache: true, _cachedAt: ISO string } or null
  }

  generateKey(documentText) {
    // TODO: implement — simple hash of first 200 chars, return "doc_XXXXXXXX"
  }
}

module.exports = { FallbackCache };
