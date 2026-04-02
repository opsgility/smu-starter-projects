const { McpServer } = require("@modelcontextprotocol/sdk/server/mcp.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { z } = require("zod");
// DocStream MCP Server - Basic tools and resources
const server = new McpServer({ name: "docstream", version: "1.0.0" });
// TODO: Register tools, resources, and prompts
const transport = new StdioServerTransport();
(async () => { await server.connect(transport); })();
