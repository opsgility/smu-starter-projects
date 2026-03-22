# MCP Starter

Run `dotnet run` to create the SQLite database, then connect via MCP.

## Project Structure

- **Project.csproj / Program.cs** — Console app that creates and seeds a `library.db` SQLite database with Authors, Books, and Genres tables
- **mcp-server/** — Skeleton MCP server project to build with Claude Code's help

## Getting Started

1. Run `dotnet run` in the root directory to create the SQLite database
2. Verify `library.db` was created with 5 authors, 10 books, and 6 genres
3. Use Claude Code to build the MCP server in the `mcp-server/` directory
4. Configure Claude Code to connect to your MCP server
