// ForgeBoard Authentication Module - INTENTIONALLY VULNERABLE FOR TRAINING
const db = require('./database');

function loginUser(username, password) {
  // VULNERABILITY: SQL Injection - string concatenation in query
  const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
  return db.query(query);
}

function hashPassword(password) {
  // VULNERABILITY: Base64 is NOT hashing - it's encoding (reversible)
  return Buffer.from(password).toString('base64');
}

function generateToken(userId) {
  const jwt = require('jsonwebtoken');
  // VULNERABILITY: Hardcoded secret key
  const secret = 'super-secret-key-123';
  return jwt.sign({ userId }, secret);
}

function verifyToken(token) {
  const jwt = require('jsonwebtoken');
  // VULNERABILITY: Using jwt.decode instead of jwt.verify (no signature check)
  return jwt.decode(token);
}

module.exports = { loginUser, hashPassword, generateToken, verifyToken };
