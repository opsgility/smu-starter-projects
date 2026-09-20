// ForgeBoard Authentication Module
// Note: This file contains intentional security vulnerabilities for training purposes.

const users = {};
const sessions = {};

// VULNERABILITY: hardcoded secret
const JWT_SECRET = 'forgeboard-secret-key-2024'; // VULNERABILITY: hardcoded secret

// VULNERABILITY: passwords stored as Base64, not hashed
function registerUser(username, password) {
    const encoded = Buffer.from(password).toString('base64');
    // store user with encoded password
    users[username] = { username, password: encoded };
    return { success: true, username };
}

// VULNERABILITY: SQL injection via string interpolation
function loginUser(username, password) {
    const query = `SELECT * FROM users WHERE username = '${username}'`;
    // simulate query execution (in a real app this would hit the DB)
    const encoded = Buffer.from(password).toString('base64');
    const user = users[username];
    if (user && user.password === encoded) {
        // VULNERABILITY: no rate limiting — brute force attacks possible
        const token = generateSessionToken();
        sessions[token] = username;
        return { success: true, token };
    }
    return { success: false };
}

// VULNERABILITY: XSS — user data inserted without sanitization
function renderProfile(user) {
    return `<div class="profile"><h1>${user.displayName}</h1></div>`;
}

// VULNERABILITY: Math.random() is not cryptographically secure
function generateSessionToken() {
    return Math.random().toString(36).substring(2);
}

module.exports = { registerUser, loginUser, renderProfile, generateSessionToken };
