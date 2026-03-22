# Book Library API

Add EF Core persistence with Claude Code.

This project is a fully functional Book Library API using in-memory collections. Your task is to replace the in-memory repositories with Entity Framework Core backed by a real database.

## Current Architecture

- **Controllers** — BooksController and AuthorsController with full CRUD
- **Services** — BookService handles DTO mapping and business logic
- **Repositories** — In-memory implementations using List<T>
- **DTOs** — Request/response objects for the Books API

## Getting Started

1. Run `dotnet run` to start the API
2. Navigate to `/swagger` to explore the endpoints
3. Use Claude Code to add EF Core with SQLite or SQL Server
4. Replace the in-memory repositories with EF Core implementations
