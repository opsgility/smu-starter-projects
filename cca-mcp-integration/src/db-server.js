const { McpServer } = require("@modelcontextprotocol/sdk/server/mcp.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const Database = require("better-sqlite3");

// Initialize SQLite database
const db = new Database("docstream.db");

// TODO: Task 1 — Initialize the database schema
// Create two tables if they don't exist:
//   documents: id, title, category (CHECK enum), status, author, created_at, word_count, confidence
//   routing_history: id, document_id (FK), destination, urgency, routed_at, routed_by
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

  CREATE TABLE IF NOT EXISTS routing_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER REFERENCES documents(id),
    destination TEXT,
    urgency TEXT,
    routed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    routed_by TEXT
  );
`);

const server = new McpServer({
  name: "docstream-db",
  version: "1.0.0"
});

// TODO: Task 1 — Register three MCP tools for database access
//
// Tool 1: query_documents
//   - Structured query by category, status, author, min_confidence
//   - Params: category, status, author, min_confidence, order_by (enum), order_dir (enum), limit
//   - Use parameterized queries (@param) to prevent SQL injection
//   - Cap limit at 100
//
// Tool 2: document_analytics
//   - Aggregate counts grouped by a dimension (category/status/author)
//   - Params: group_by (enum), date_from, date_to
//   - Returns: { dimension, groups: [{ group_by_value, count, avg_confidence }] }
//
// Tool 3: routing_history
//   - Join routing_history with documents for context
//   - Params: document_id (optional), destination (optional), limit
//   - Returns: routing entries with document title and category

// TODO: implement server.tool() calls for all three tools

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("DocStream DB MCP server running on stdio");
}

main().catch(console.error);
