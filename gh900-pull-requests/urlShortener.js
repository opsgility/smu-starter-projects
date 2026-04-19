// URL Shortener Service
const urlDatabase = {};

function shorten(originalUrl) {
    const id = Math.random().toString(36).substring(2, 8);
    urlDatabase[id] = originalUrl;
    return { id, shortUrl: `http://short.url/${id}` };
}

function resolve(shortId) {
    return urlDatabase[shortId] || null;
}

module.exports = { shorten, resolve };
