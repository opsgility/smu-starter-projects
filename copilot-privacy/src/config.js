// ForgeBoard Configuration - Contains sensitive values that should be excluded from Copilot
module.exports = {
  port: process.env.PORT || 3000,
  database: { host: process.env.DB_HOST || 'localhost', password: process.env.DB_PASSWORD || 'dev-password-123' },
  jwt: { secret: process.env.JWT_SECRET || 'my-super-secret-jwt-key-change-in-production' },
  stripe: { apiKey: process.env.STRIPE_KEY || 'sk_test_fake_key_for_development' }
};
