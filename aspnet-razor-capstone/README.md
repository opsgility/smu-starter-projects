# BrightShelf Capstone Project

## Brief

Build a complete **BrightShelf** product management web application that demonstrates
all skills covered in the ASP.NET Core Razor Pages course.

## Requirements

### Core Features
- **Data Layer**: Product model with EF Core + PostgreSQL (`brightshelf_capstone` database)
- **Authentication**: ASP.NET Core Identity with registration, login, and page-level authorization
- **CRUD Operations**: Full product management (Create, Read, Update, Delete)
- **File Uploads**: Product image upload stored in `wwwroot/uploads/`

### Advanced Features
- **API Integration**: Typed HttpClient consuming an internal or external API
- **AJAX**: Client-side search/filter and AJAX delete with anti-forgery tokens
- **Caching**: IMemoryCache and/or OutputCache for performance
- **Security**: Security headers, custom error pages, CSP, HSTS

### Testing
- xUnit test project with Moq
- Minimum 3 unit tests for page models
- Minimum 1 integration test using `WebApplicationFactory`

## Getting Started

1. Create your models, DbContext, and pages in the appropriate folders
2. Configure services in `Program.cs` (see comments for full requirements list)
3. Run `dotnet build` to verify your project compiles
4. Run `dotnet ef migrations add InitialCreate` to create your first migration
5. Run `dotnet ef database update` to apply migrations

## Evaluation Criteria

- All CRUD operations work correctly
- Authentication and authorization are properly configured
- File uploads are handled securely
- At least one API integration is functional
- AJAX interactions work without full page reloads
- Caching improves performance measurably
- Security headers are present in responses
- Tests pass and provide meaningful coverage
