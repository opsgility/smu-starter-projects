# BookShelf API - Capstone Project

Build a library management REST API from scratch using everything you've learned in this course.

## Requirements

### Models
- **Book**: Id, Title, ISBN, PublishedDate, Summary, AuthorId
- **Author**: Id, FirstName, LastName, Bio, Books (collection)

### Features to Implement
1. **EF Core with SQLite** - Set up DbContext, models, and seed data
2. **Repository + Service pattern** - Clean separation of concerns
3. **DTOs + AutoMapper** - Request/response DTOs with proper mapping
4. **FluentValidation** - Validate all inputs (ISBN format, required fields, etc.)
5. **JWT Authentication** - Register/login endpoints with token generation
6. **Role-based Authorization** - Admin vs. Reader roles
7. **Pagination** - Support page/pageSize query parameters on list endpoints
8. **Swagger Documentation** - XML comments and OpenAPI metadata
9. **Custom Middleware** - Request logging and error handling
10. **Unit Tests** - Test service layer with mocked repositories

### API Endpoints
| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| POST | /api/auth/register | None | Register a new user |
| POST | /api/auth/login | None | Login and get JWT |
| GET | /api/books | None | List books (paginated) |
| GET | /api/books/{id} | None | Get book details |
| POST | /api/books | Admin | Create a book |
| PUT | /api/books/{id} | Admin | Update a book |
| DELETE | /api/books/{id} | Admin | Delete a book |
| GET | /api/authors | None | List authors |
| GET | /api/authors/{id} | None | Get author with books |
| POST | /api/authors | Admin | Create an author |

### Getting Started
1. Open this project in your development environment
2. Run `dotnet build` to verify the project compiles
3. Run `dotnet run` and visit http://localhost:5000 to see the welcome message
4. Start building your API following the requirements above
