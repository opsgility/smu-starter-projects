// FleetBoard Authentication — INTENTIONALLY VULNERABLE FOR RESPONSIBLE-AI TRAINING
// Five planted security vulnerabilities, each marked with // VULNERABILITY:
// Reviewed in Exercise 2 of the Copilot Foundations lab (lab 1595, exercise 2576).
// Do NOT ship this code to production.

const JWT_SECRET = 'northpeak-fleetboard-signing-key-2026'; // VULNERABILITY: hardcoded secret — load from process.env.JWT_SECRET and fail fast if missing

function registerFleetOperator(username, password) {
  // VULNERABILITY: Base64 encoding is NOT hashing — Buffer.from(encoded, 'base64').toString() recovers the password.
  // Replace with bcrypt (>=12 rounds), argon2id, or scrypt.
  const hashedPassword = Buffer.from(password).toString('base64');
  return { id: Date.now(), username, hashedPassword };
}

function loginFleetOperator(username, password) {
  // VULNERABILITY: SQL injection — string interpolation lets `' OR '1'='1` bypass authentication.
  // Replace with a parameterized query: db.query('SELECT ... WHERE username = ? AND password = ?', [username, password]).
  const query = `SELECT * FROM operators WHERE username = '${username}' AND password = '${password}'`;
  console.log('Executing query:', query);
  return { authenticated: true, username };
}

function renderOperatorProfile(operator) {
  // VULNERABILITY: XSS — operator.displayName flows straight into HTML.
  // An operator whose displayName is <script>alert('XSS')</script> executes arbitrary JS in the dispatcher dashboard.
  // Replace with an HTML-escape pass (or route through DOMPurify) before interpolation.
  return `<div class="operator-profile"><h1>${operator.displayName}</h1><p>${operator.bio}</p></div>`;
}

function generateDispatchToken() {
  // VULNERABILITY: Math.random() is not cryptographically secure — the output is predictable.
  // Replace with crypto.randomBytes(32).toString('hex') or crypto.randomUUID().
  return Math.random().toString(36).substring(2);
}

module.exports = { registerFleetOperator, loginFleetOperator, renderOperatorProfile, generateDispatchToken, JWT_SECRET };
