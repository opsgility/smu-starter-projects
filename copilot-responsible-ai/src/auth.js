// ForgeBoard Authentication Module - INTENTIONALLY VULNERABLE FOR TRAINING
// This file contains five security vulnerabilities marked with // VULNERABILITY:
// Your task is to identify each vulnerability and evaluate Copilot's suggested fixes.
// Do NOT use this code in production.

const JWT_SECRET = 'forgeboard-secret-key-2024'; // VULNERABILITY: hardcoded secret — should be loaded from process.env.JWT_SECRET

function registerUser(username, password) {
  // VULNERABILITY: Base64 encoding is NOT hashing — it is trivially reversible with Buffer.from(encoded, 'base64').toString()
  const hashedPassword = Buffer.from(password).toString('base64');
  // Simulate saving the user to a database
  return { id: Date.now(), username, hashedPassword };
}

function loginUser(username, password) {
  // VULNERABILITY: SQL injection — string interpolation allows an attacker to pass ' OR '1'='1 as the username
  const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
  // Simulate executing the query (in a real app this would use a DB driver)
  console.log('Executing query:', query);
  return { authenticated: true, username };
}

function renderProfile(user) {
  // VULNERABILITY: XSS — user.displayName is inserted directly into HTML without escaping
  // An attacker can set displayName to <script>alert('XSS')</script> to execute arbitrary JavaScript
  return `<div class="profile"><h1>${user.displayName}</h1><p>${user.bio}</p></div>`;
}

function generateSessionToken() {
  // VULNERABILITY: Math.random() is not cryptographically secure — its output is predictable
  // Use crypto.randomBytes(32).toString('hex') instead
  return Math.random().toString(36).substring(2);
}

module.exports = { registerUser, loginUser, renderProfile, generateSessionToken };
