const Database = require('better-sqlite3');
const db = new Database(':memory:');
db.exec(`CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT, status TEXT DEFAULT 'todo', priority TEXT DEFAULT 'medium', assignee_id INTEGER, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)`);
db.exec(`INSERT INTO tasks (title, description, status, priority) VALUES ('Set up CI/CD', 'Configure GitHub Actions pipeline', 'done', 'high'), ('Database schema', 'Design initial data model', 'in-progress', 'high'), ('User auth', 'Implement JWT authentication', 'todo', 'critical')`);
module.exports = db;
