import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
// DocStream MCP Server - Basic tools and resources
const server = new McpServer({ name: "docstream", version: "1.0.0" });
// TODO: Register tools, resources, and prompts
const transport = new StdioServerTransport();
await server.connect(transport);
