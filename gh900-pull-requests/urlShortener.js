// URL Shortener Service
// Starter: has basic shorten and resolve — you will add validation via a pull request

const urlDatabase = {};

function shortenUrl(originalUrl) {
    // Note: currently accepts any string — no validation yet
    // TODO (feature/url-validation): validate that the URL starts with http:// or https://
    const id = Math.random().toString(36).substring(2, 8);
    urlDatabase[id] = originalUrl;
    return id;
}

function resolveUrl(shortId) {
    return urlDatabase[shortId] || null;
}

module.exports = { shortenUrl, resolveUrl };
