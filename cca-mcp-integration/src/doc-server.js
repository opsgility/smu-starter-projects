const { McpServer } = require("@modelcontextprotocol/sdk/server/mcp.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");

// In-memory document store (for the document management server)
const documentStore = new Map();
let nextId = 1;

const server = new McpServer({
  name: "docstream",
  version: "1.0.0"
});

// TODO: Task 2 — This is the document management server (from the previous lab)
// Register the standard DocStream document management tools:
//   - add_document: add a document with title, content, category, author
//   - search_documents: search by category, keyword, author
//   - get_document: retrieve full document by ID
// Include the docstream://stats resource for store statistics
//
// This server handles document content (full text, add, search)
// The db-server.js handles metadata queries and analytics

// TODO: implement server.tool() calls for add_document, search_documents, get_document
// TODO: implement server.resource() for docstream://stats

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("DocStream document MCP server running on stdio");
}

main().catch(console.error);
