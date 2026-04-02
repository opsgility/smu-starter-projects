const { McpServer } = require("@modelcontextprotocol/sdk/server/mcp.js");

// TODO: Task 1 — Implement registerDocumentTools(server, store)
// Register 6 MCP tools covering the full document lifecycle.
// Pay close attention to tool descriptions — they guide Claude's routing decisions.
//
// Tool 1: ingest_document
//   - For NEW documents entering the system for the first time
//   - Description must clarify: "Do NOT use for already-ingested documents — use update_document"
//   - Params: title, content, source (enum: email/upload/api/scan), priority (enum: urgent/normal/low)
//
// Tool 2: classify_document
//   - For MANUAL reclassification of already-ingested documents
//   - Description must clarify: "Do NOT use for new documents — use ingest_document first"
//   - Params: document_id (number), category (enum), reason (string, required for audit)
//   - Error if document_id not found: { error: "DOCUMENT_NOT_FOUND", message, recovery }
//
// Tool 3: search_documents
//   - Returns metadata only (not full content)
//   - Description must clarify: "For full content, use get_document with ID from results"
//   - Params: query (optional), category (optional), status (enum, optional), limit (default 20)
//
// Tool 4: get_document
//   - Returns full content by ID
//   - Description must clarify: "Use search_documents first to find relevant IDs"
//   - Error if not found: { error: "DOCUMENT_NOT_FOUND", message, recovery }
//
// Tool 5: route_document
//   - Description must clarify: "ONLY for documents with status 'classified'"
//   - Error if not classified: { error: "INVALID_STATUS", message, recovery }
//   - Params: document_id, destination (enum), urgency (enum), notes (optional)
//
// Tool 6: get_pipeline_status
//   - Read-only overview — counts by status/category
//   - No parameters needed

function registerDocumentTools(server, store) {
  // TODO: implement all 6 tools using server.tool(name, description, schema, handler)
  // Each handler should return { content: [{ type: "text", text: JSON.stringify(...) }] }
  // Error responses should include isError: true
}

module.exports = { registerDocumentTools };
