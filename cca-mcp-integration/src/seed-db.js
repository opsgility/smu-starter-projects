const Database = require("better-sqlite3");
const db = new Database("docstream.db");

// TODO: Task 3 — Seed the database with realistic test documents
// Insert at least 10 documents covering all categories and statuses
// This data is used by db-server.js for analytics and query testing

// Ensure table exists
db.exec(`
  CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT CHECK(category IN ('invoice','contract','report','correspondence','technical_spec')),
    status TEXT DEFAULT 'queued',
    author TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    word_count INTEGER,
    confidence REAL
  );
`);

const documents = [
  { title: "Q1 Cloud Hosting Invoice", category: "invoice", status: "routed", author: "CloudServe Inc.", word_count: 245, confidence: 0.96 },
  { title: "Master Services Agreement", category: "contract", status: "classified", author: "Legal Dept", word_count: 4200, confidence: 0.91 },
  { title: "Sprint Velocity Report - March", category: "report", status: "routed", author: "Engineering", word_count: 890, confidence: 0.88 },
  { title: "GPU Quota Increase Request", category: "correspondence", status: "classified", author: "DevOps Team", word_count: 156, confidence: 0.74 },
  { title: "DocStream API v3 Specification", category: "technical_spec", status: "routed", author: "Platform Team", word_count: 3100, confidence: 0.95 },
  { title: "Annual Software License Invoice", category: "invoice", status: "queued", author: "SoftCo Inc.", word_count: 312, confidence: 0.93 },
  { title: "NDA - TechVentures Partnership", category: "contract", status: "classified", author: "Legal Dept", word_count: 1800, confidence: 0.89 },
  { title: "Security Incident Postmortem", category: "report", status: "routed", author: "Security Team", word_count: 1100, confidence: 0.85 },
  { title: "Team Offsite Planning Email", category: "correspondence", status: "queued", author: "HR Dept", word_count: 220, confidence: 0.81 },
  { title: "Infrastructure Architecture Doc", category: "technical_spec", status: "classified", author: "Platform Team", word_count: 4500, confidence: 0.94 },
  // TODO: add more documents for better analytics coverage
];

const insert = db.prepare(
  `INSERT INTO documents (title, category, status, author, word_count, confidence)
   VALUES (@title, @category, @status, @author, @word_count, @confidence)`
);

for (const doc of documents) {
  insert.run(doc);
}

console.log(`Seeded ${documents.length} documents into docstream.db`);
db.close();
