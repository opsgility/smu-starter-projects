// URL Shortener Service
// Starting point for the code review lab
// Students will add JSDoc comments through a PR review cycle

const urlDatabase = {};

function shortenUrl(originalUrl) {
    if (!isValidUrl(originalUrl)) {
        return { error: 'Invalid URL. Must start with http:// or https://' };
    }
    const id = Math.random().toString(36).substring(2, 8);
    urlDatabase[id] = {
        url: originalUrl,
        createdAt: new Date().toISOString()
    };
    return { id, shortUrl: `http://short.url/${id}` };
}

function isValidUrl(url) {
    try {
        const parsed = new URL(url);
        return parsed.protocol === 'http:' || parsed.protocol === 'https:';
    } catch {
        return false;
    }
}

function resolveUrl(shortId) {
    const entry = urlDatabase[shortId];
    return entry ? entry.url : null;
}

// TODO (review): Add JSDoc comments to all three exported functions
// A reviewer will request this change before approving the PR

module.exports = { shortenUrl, resolveUrl, isValidUrl };
